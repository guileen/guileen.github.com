---
title: TiDB源码阅读记录
tags: 
categories: 分布式
---

tidb-server服务启动过程大致如下：

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

我们关注一下tikv.KVStore。代码主要集中在 tikv/kv.go  tikv/split_region.go 。按启动顺序view代码没有什么思路，通过测试用例找一下突破口。通过 ticlient_test.go发现tikv的操作都是在一个个的KVTxn事务中执行的，代码在 store/tikv/txn.go 中,核心代码在Commit。所有的测试用例都值得好好看看。代码中有些`failpoint.Inject("mockXXXError", fn) `是测试用例模拟异常用的。

阅读了最新的5.0版的代码之后，感觉现在的代码非常的冗杂，各种设计模式加上去之后，根本无法弄清楚关键步骤。为了更容易理解，checkout 了 1.0.0的代码顿时感觉清爽了很多。

```go
func (txn *tikvTxn) Commit() error {
	defer txn.close()
	start := time.Now()
  // 比较 us.lazyConditionPairs 的 value 与 us.snapshot.BatchGet 的结果是否相同
  // 不同则表示事务条件检查立即失败。是一个乐观锁
	if err := txn.us.CheckLazyConditionPairs(); err != nil {return err}
  // 构造两阶段提交
	committer, err := newTwoPhaseCommitter(txn)
  if err != nil || committer == nil { return err }
  // 执行提交
	err = committer.execute()
	if err != nil {
    // 【失败】写入rollback binlog。
		committer.writeFinishBinlog(binlog.BinlogType_Rollback, 0)
		return errors.Trace(err)
	}
  // 【成功】写入commit binlog。
	committer.writeFinishBinlog(binlog.BinlogType_Commit, int64(committer.commitTS))
	txn.commitTS = committer.commitTS
}

```

这里有个问题，如果binlog写入失败怎么办？tikv重试20次写入binlog，感觉还不够严谨。binlog写入是请求一个grpc。不知后续版本是如何优化binlog写入失败的问题。然后是2PC commit的代码。5.0的代码有250行左右，1.0的代码只有70行，清爽。

```go
// execute executes the two-phase commit protocol.
func (c *twoPhaseCommitter) execute() error {
   defer func() {
      // Always clean up all written keys if the txn does not commit.
      c.mu.RLock()
      writtenKeys := c.mu.writtenKeys
      committed := c.mu.committed
      undetermined := c.mu.undetermined
      c.mu.RUnlock()
      if !committed && !undetermined {
         twoPhaseCommitGP.Go(func() {
            err := c.cleanupKeys(NewBackoffer(cleanupMaxBackoff, goctx.Background()), writtenKeys)
            if err != nil {
               log.Infof("2PC cleanup err: %v, tid: %d", err, c.startTS)
            } else {
               log.Infof("2PC clean up done, tid: %d", c.startTS)
            }
         })
      }
   }()
   
   // 将store的clusterID写入binlog， c.txn.us#binInfo.Data.StartTS = c.startTS
   if err:=c.prewriteBinlog(); err!=nil {return err}

   // doActionsOnKeys 将key分组为主批和次批，如果主批存在key，先在主批写入状态，后在次批。如果动作已提交，此批在后台协程中完成。
   // key所在分区，通过pdClient获取(GRPC)。	meta, leader, err := c.pdClient.GetRegion(bo.ctx, key)
   // Refer: https://github.com/facebook/mysql-5.6/wiki/MyRocks-record-format#memcomparable-format
   err := c.prewriteKeys(NewBackoffer(prewriteMaxBackoff, ctx), c.keys)
   if err != nil {
      log.Debugf("2PC failed on prewrite: %v, tid: %d", err, c.startTS)
      return errors.Trace(err)
   }

   // 不断尝试获取时间戳 s.oracle.GetTimestamp(bo.ctx)。 oracle是一个获得升序时间的模块。
   commitTS, err := c.store.getTimestampWithRetry(NewBackoffer(tsoMaxBackoff, ctx))
   if err != nil {
      log.Warnf("2PC get commitTS failed: %v, tid: %d", err, c.startTS)
      return errors.Trace(err)
   }

   // check commitTS
   if commitTS <= c.startTS {
      err = errors.Errorf("Invalid transaction tso with start_ts=%v while commit_ts=%v",
         c.startTS,
         commitTS)
      log.Error(err)
      return errors.Trace(err)
   }
   c.commitTS = commitTS
   // 检查数据库是否变更
   // SchemaLeaseChecker.Check(commitTS)
   // result := s.SchemaValidator.Check(txnTS, s.schemaVer, s.relatedTableIDs)
   if err = c.checkSchemaValid(); err != nil {
      return errors.Trace(err)
   }
   // 任务超时
   if c.store.oracle.IsExpired(c.startTS, maxTxnTimeUse) {
      err = errors.Errorf("txn takes too much time, start: %d, commit: %d", c.startTS, c.commitTS)
      return errors.Annotate(err, txnRetryableMark)
   }
   // 提交key
   // resp, err := c.store.SendReq(bo, req, batch.region, readTimeoutShort)
   err = c.commitKeys(NewBackoffer(commitMaxBackoff, ctx), c.keys)
   if err != nil {
      if errors.Cause(err) == terror.ErrResultUndetermined {
         c.mu.undetermined = true
      }
      if !c.mu.committed {
         log.Debugf("2PC failed on commit: %v, tid: %d", err, c.startTS)
         return errors.Trace(err)
      }
      log.Debugf("2PC succeed with error: %v, tid: %d", err, c.startTS)
   }
   return nil
}
```

简而言之，就是一个2pc。tidb-server的代码的最终落地，都是通过grpc调用其他服务组件完成。我们看看tikv的localstore部分。kv.go 的 dbStore.Begin, local_region.go 的 localRegion.Handle。