---
title: TiDB源码阅读记录
tags: 
categories: 分布式
---

服务启动过程大致如下：

```go
storage, err = driver.TiKVDriver{}.Open(path)
// Bootstrap a session to load information schema.
dom, err = session.BootstrapSession(storage)
driver := server.NewTiDBDriver(storage)
svr, err = server.NewServer(cfg, driver)
svr.SetDomain(dom)
```

Storage是存储的核心组件, store/driver/TiKVDriver 的 Open过程大致如下：

```go
  pdCli, err := pd.NewClient(etcdAddrs, ...)
  pdCli = execdetails.InterceptedPDClient{Client: pdCli}
  uuid := fmt.Sprintf("tikv-%v", pdCli.GetClusterID(context.TODO()))
	spkv, err := tikv.NewEtcdSafePointKV(etcdAddrs, tlsConfig)
	pdClient := tikv.CodecPDClient{Client: pdCli}
	s, err := tikv.NewKVStore(uuid, &pdClient, spkv, tikv.NewRPCClient(d.security))
	coprStore, err := copr.NewStore(s, coprCacheConfig)
	store := &tikvStore{
		KVStore:   s,
		memCache:  kv.NewCacheDB(),
		pdClient:  &pdClient,
		coprStore: coprStore,
	}
	return store, nil
```

可以看出，Storage依赖于etcd来解决一些分布式的问题，对etcd的操作封装在tikv.CodecPDClient  和 tikv/pd/baseClient 中。其余几个组件主要是 store/tikv/kv.go 里的 KVStore,  kv/cachedb.go 里的cacheDB （使用的是freecache），还有一个 copr.Store 主要代码在 store/copr/ 来处理 coprocessor 和 MMP。

我们关注一下tikv.KVStore。代码主要集中在 tikv/kv.go  tikv/split_region.go 。按启动顺序view代码没有什么思路，通过测试用例找一下突破口。通过 ticlient_test.go发现tikv的操作都是在一个个的KVTxn事务中执行的，代码在 store/tikv/txn.go 中,核心代码在Commit。所有的测试用例都值得好好看看。

```go
// Commit commits the transaction operations to KV store.
func (txn *KVTxn) Commit(ctx context.Context) error {
   // ...
   // 如果使用了悲观锁，那么committer被初始化了。否则构造一个TwoPhaseCommitter
   committer, err = newTwoPhaseCommitter(txn, sessionID)
   defer func() {
      // For async commit transactions, the ttl manager will be closed in the asynchronous commit goroutine.
      // 也就是说，如果是异步模式，ttlManager将会工作
      if !committer.isAsyncCommit() {
         committer.ttlManager.close()
      }
   }()

   initRegion := trace.StartRegion(ctx, "InitKeys")
   committer.initKeysAndMutations()
   initRegion.End()
  
   // latches disabled
   // pessimistic transaction should also bypass latch.
   // 这里出现了一个术语 Latch，门闩，字面意思类似于锁。源于电路中的Flip-Flop，触发器，振荡器，产生0-1信号
   // 这里的由 LatchsScheduler 产生，代码位于 tikv/scheduler.go
   if txn.store.txnLatches == nil || txn.IsPessimistic() {
      err = committer.execute(ctx)
   }

   // latches enabled
   // for transactions which need to acquire latches
   start = time.Now()
   // TODO: 研究 txnLatches.Lock 与mutex具体的区别。
   lock := txn.store.txnLatches.Lock(committer.startTS, committer.mutations.GetKeys())
   defer txn.store.txnLatches.UnLock(lock)
   if lock.IsStale() {
      return kv.ErrWriteConflictInTiDB.FastGenByArgs(txn.startTS)
   }
   err = committer.execute(ctx)
}
```

整体来看，Txn 中只做了不同事务的Latch Lock隔离，防止事务的冲突，事务具体的执行动作在 twoPhaseCommitter.execute 中进行。这个函数有200多行，比较复杂。我们分段来看：

```go
	// Check if 1PC is enabled.
	if c.checkOnePC() {
		commitTSMayBeCalculated = true
		c.setOnePC(true)
	}
	// If we want to use async commit or 1PC and also want linearizability across
	// all nodes, we have to make sure the commit TS of this transaction is greater
	// than the snapshot TS of all existent readers. So we get a new timestamp
	// from PD as our MinCommitTS.
	if commitTSMayBeCalculated && c.needLinearizability() {
		failpoint.Inject("getMinCommitTSFromTSO", nil)
		minCommitTS, err := c.store.oracle.GetTimestamp(ctx, &oracle.Option{TxnScope: oracle.GlobalTxnScope})
		// If we fail to get a timestamp from PD, we just propagate the failure
		// instead of falling back to the normal 2PC because a normal 2PC will
		// also be likely to fail due to the same timestamp issue.
		if err != nil {
			return errors.Trace(err)
		}
		c.minCommitTS = minCommitTS
	}
	// Calculate maxCommitTS if necessary
	if commitTSMayBeCalculated {
		if err = c.calculateMaxCommitTS(ctx); err != nil {
			return errors.Trace(err)
		}
	}

	failpoint.Inject("beforePrewrite", nil)
```

这时2pc还没开始，

```go
c.prewriteStarted = true
var binlogChan <-chan BinlogWriteResult
if c.shouldWriteBinlog() {
   binlogChan = c.binlog.Prewrite(ctx, c.primary())
}
prewriteBo := NewBackofferWithVars(ctx, PrewriteMaxBackoff, c.txn.vars)
start := time.Now()
err = c.prewriteMutations(prewriteBo, c.mutations)

if err != nil {
   // TODO: Now we return an undetermined error as long as one of the prewrite
   // RPCs fails. However, if there are multiple errors and some of the errors
   // are not RPC failures, we can return the actual error instead of undetermined.
   if undeterminedErr := c.getUndeterminedErr(); undeterminedErr != nil {
      logutil.Logger(ctx).Error("2PC commit result undetermined",
         zap.Error(err),
         zap.NamedError("rpcErr", undeterminedErr),
         zap.Uint64("txnStartTS", c.startTS))
      return errors.Trace(terror.ErrResultUndetermined)
   }
}

commitDetail := c.getDetail()
commitDetail.PrewriteTime = time.Since(start)
if prewriteBo.totalSleep > 0 {
   atomic.AddInt64(&commitDetail.CommitBackoffTime, int64(prewriteBo.totalSleep)*int64(time.Millisecond))
   commitDetail.Mu.Lock()
   commitDetail.Mu.BackoffTypes = append(commitDetail.Mu.BackoffTypes, prewriteBo.types...)
   commitDetail.Mu.Unlock()
}
if binlogChan != nil {
   startWaitBinlog := time.Now()
   binlogWriteResult := <-binlogChan
   commitDetail.WaitPrewriteBinlogTime = time.Since(startWaitBinlog)
   if binlogWriteResult != nil {
      binlogSkipped = binlogWriteResult.Skipped()
      binlogErr := binlogWriteResult.GetError()
      if binlogErr != nil {
         return binlogErr
      }
   }
}
if err != nil {
   logutil.Logger(ctx).Debug("2PC failed on prewrite",
      zap.Error(err),
      zap.Uint64("txnStartTS", c.startTS))
   return errors.Trace(err)
}
```

上面这一段开始了2pc的 prewrite阶段。

```go
// strip check_not_exists keys that no need to commit.
c.stripNoNeedCommitKeys()

var commitTS uint64

if c.isOnePC() {
   if c.onePCCommitTS == 0 {
      err = errors.Errorf("session %d invalid onePCCommitTS for 1PC protocol after prewrite, startTS=%v", c.sessionID, c.startTS)
      return errors.Trace(err)
   }
   c.commitTS = c.onePCCommitTS
   c.txn.commitTS = c.commitTS
   logutil.Logger(ctx).Debug("1PC protocol is used to commit this txn",
      zap.Uint64("startTS", c.startTS), zap.Uint64("commitTS", c.commitTS),
      zap.Uint64("session", c.sessionID))
   return nil
}
```

如果是OnePC，那么就到此结束了。



最后一段在defer中：

```go
if c.isOnePC() {
   // The error means the 1PC transaction failed.
   if err != nil {
      metrics.OnePCTxnCounterError.Inc()
   } else {
      metrics.OnePCTxnCounterOk.Inc()
   }
} else if c.isAsyncCommit() {
   // The error means the async commit should not succeed.
   if err != nil {
      if c.getUndeterminedErr() == nil {
         c.cleanup(ctx)
      }
      metrics.AsyncCommitTxnCounterError.Inc()
   } else {
      metrics.AsyncCommitTxnCounterOk.Inc()
   }
} else {
   // Always clean up all written keys if the txn does not commit.
   c.mu.RLock()
   committed := c.mu.committed
   undetermined := c.mu.undeterminedErr != nil
   c.mu.RUnlock()
   if !committed && !undetermined {
      c.cleanup(ctx)
   }
   c.txn.commitTS = c.commitTS
   if binlogSkipped {
      c.binlog.Skip()
      return
   }
   if !c.shouldWriteBinlog() {
      return
   }
   if err != nil {
      c.binlog.Commit(ctx, 0)
   } else {
      c.binlog.Commit(ctx, int64(c.commitTS))
   }
}
```

