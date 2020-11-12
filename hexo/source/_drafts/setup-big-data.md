---
title: 基于AWS的大数据架构
tags:
---

大数据系统不同于传统信息系统的是，大数据系统致力于充分压榨信息的价值，而传统信息系统只关注那些唾手可得的数据价值。因此成本与效果是大数据系统最为关心的问题。

成本主要影响因素是存储成本、计算成本、维护成本。效果的主要衡量指标是吞吐量、运行延时、转化效果。但是这二者是相互矛盾的，我们必须在这两者之间寻找一个平衡，这就是大数据架构的基本目标。在工程之中，因为人力成本占比极大，因此如何更方便的进行维护、开发，也是非常重要的目标。

大数据架构经常接触两个概念：数据湖（Data lake）与数据仓库（Data warehouse）。数据湖是原始的、未处理的、使用目的尚不确定的数据，而数据仓库则是已经过处理的，有明确使用目的的数据。

在分层上可粗略划分为四个层次：采集层、存储层、计算层、应用层。

大数据工具、服务组件非常之多，**过于关注这些技术会陷入文档的冲击之中，且不能建立起大局观。**

大数据项目流程：解读目标，明确需求场景，明确数据标签和规则，特征选取，建立模型，验收测试上线。


三要素：
1. 数据的提取——转换——加载（ETL）

2. 数据仓库设计：
- 事实表
- 维表
- 事实表与一组维表组成星形结构
- 与维表相联系的数据表簇（雪花型结构或链接表组合）

![星形结构](img/dw/star-schema-example1.png)
*星形结构*

![雪花结构](img/dw/ifx_snowflake1.gif)
*雪花结构*


## 实时数仓（Lambda架构 vs Kappa架构）


## 实时计算引擎（Flink）

## 实时存储（ClickHouse）


1. Athna 每天扫一次，保存结果，。
2. 设备、区域、性别、年龄。某个时间段，iOS，湖南，女性，活跃总量曲线。改指标下的该API请求总量/该指标下的日活跃用户数， 按服务、API汇总。
3. 看每个服务级别分类汇总。
4. 点的粒度。5分钟，小时，天，周。
5. 价格成本。
5. 消息相关的统计缺失，需要增加。

某时间范围，以某时间粒度汇总，根据某组合条件筛选，得出某些指标的统计和对比。
1. 组合条件有：设备、区域、性别、年龄
2. 指标对比有：人（总、活跃），API（总，各服务，各API），人均API。



3. OLAP

选型特点：
- Date，user， 标签

os=IOS
1
/im/group/batch_get_group_info
7200
2
/user/ubs/user/batchGetTaBasicInfoMap
6658
3
/im/messageapi/offline/message
2131
4
/space/moment/follow
2036
5
/user/ubs/user/getTaBasicInfo
1374
6
/space/friend/sync
1361
7
/system/notice/summary
1262

os=Android
1
/user/ubs/user/getProfile
2751
2
/space/sync/count
1930
3
/user/ubs/user/batchGetTaBasicInfo
1882
4
/system/notice/summary
1589
5
/space/friend/friend_apply_list
1481
6
/im/messageapi/offline/message
1285
7
/space/moment/follow
1221
8
/im/conv/settings/list
1165
9
/space/moment/index
1124
10
/space/friend/sync
1051
11
/user/ubs/userSetting/get
1037




-----

Stream，Data Sources and Sinks(数据源和接收器)，and Stream processor。

用户行为的常规数据字段：

Stream Processing: 
1. Apache Flink
2. Apache Flumn 
3. Apache Storm
4. Fluent

Kafka:

计算框架：
1. Apache Spark


ClickHouse


数据收集：
1. 
数据流：
Kafka，filebeat
数据格式：
Parquet
存储方案：
HDFS, S3
数据分析：
MR
BI：
Hive
hello
1222333444555666



一体化解决方案： Druid  vs  ClickHouse

ClickHouse: 高性能100~1000x一体化列式存储解决方案

Apache Druid: 高性能100x 

Pinot: real-time distributed OLAP datastore,can ingest from batch data sources (such as Hadoop HDFS, Amazon S3, Azure ADLS, Google Cloud Storage) as well as stream data sources (such as Apache Kafka).  built by Linkedin and Uber.

Apache Flink : Stateful Programming Computaions
 over data Streams

Samza:

Spark:

Storm:

TDEngine: 一体化大数据方案，时序数据库。

S3 作为数据湖。

收集器：
filebeat: elastic 生态
fluent: for unified loggine layer
flumn: 
