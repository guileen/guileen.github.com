---
title: 云原生架构要点
tags:
---

[TOC]

## 云原生

云原生架构是一个比较新的概念，是分布式的。CNCF定义：容器、微服务、服务网格、不可变基础设施、声明式API。云原生架构包含了微服务架构、虚拟化、IaaS、FaaS、PaaS、DevOps、AIOps、按量付费、持续部署、服务网格、弹性可伸缩等许多的内容。无法一篇文章说完。

### 十二要素

* 一份基准代码，多份部署
* 显式地**声明依赖**关系并隔离依赖
  * npm/maven/go mod/Dockerfile/Chef、Puppet、Ansible、Terraform
* **在环境中存储配置**
* 把后端服务当作附加资源
* **严格分离构建和运行阶段**
* 用一个或多个**无状态的进程**来运行应用（状态外部性）
* **数据隔离**：每个服务管理自己的数据
* 并发：通过进程模型进行扩展
* 易处理：通过**快速启动和优雅退出**来最大化应用的健壮性
* **开发环境与线上环境等价**
* **把日志当作事件流**
* *把后台任务当作一次性进程来运行*

从理论上来说，云原生的一大特点是：状态外部性。理论基础是CAP理论、最终一致性。

从服务组件上来说，有网关、出口网关、服务网格、RPC、MQ、容器构建、容器编排、数据存储、注册中心、日志系统、监控系统、告警系统、链路追踪、混乱测试、持续集成等

日志架构，filebeat -> Kafka-> flume -> ES...

Tracing, OpenTracing/Jaeger/Zipkin

服务网格，sidecar，代理，主机模式，更复杂。Istio/Linkerd/Consul connect。重试、断路器。

MQ来实现请求削峰，请求和返回都通过MQ来传递，可以使请求方、消费方都按照自己的节奏来处理请求，可以最大化系统性能。

将非功能性需求采用放到基础平台中。

KSQL、KStream v

## K8s

### 资源

![img](https://res.weread.qq.com/wrepub/epub_36511877_41)

#### 工作负载

- Pod承载容器化应用
  - 无状态
    - ~~ReplicationController~~上一代应用控制器
    - ReplicSet，支持选择器
    - Deployment，基于ReplicSet，声明式更新
  - 有状态
    - StatefulSet，如数据库，独有的持久性标志符，确保Pod间的顺序性
    - DaemonSet，运行于每个**节点**的Pod，如Kube-proxy/Fannel/日志Agent（fluentd、logstash、prometheus）
    - Job，用完即终止的应用
      - CronJob

#### 发现与负载均衡

* Service（Endpoint=IP+Port）
* Ingress，HTTP/HTTPS

#### 配置与存储

* Pod 挂载Volume
* 存储系统
  * GlusterFS
  * Ceph RBD
  * Flocker
* 存储接口
  * FlexVolume
  * CSI
* ConfigMap。支持环境变量/存储卷。不适合敏感数据
* Secret。敏感数据共享

#### 集群型资源

- Namespace 名称空间，逻辑隔离
  - Role 角色，隶属于名称空间
  - RoleBinding 隶属于且仅能作用于名称空间级别
- Node 工作节点
- ClusterRole 隶属于集群，可被RoleBinding/CLusterRoleBinding引用
- ClusterRoleBinding

#### 元数据

- HPA 可用于控制自动伸缩规模
- Pod模版
- LimitRange CPU/内存限制

## 资源API

* 格式 GROUP/VERSION/RESOURCE 如 apps/v1/deployments
* Kind 表示类型，如Namespace，Deployment，Service，Pod

```shell
~$ kubectl api-versions
apps/v1
coordination.k8s.io/v1
coordination.k8s.io/v1beta1
events.k8s.io/v1beta1
networking.k8s.io/v1
node.k8s.io/v1beta1
storage.k8s.io/v1
storage.k8s.io/v1beta1
v1
```

- 路径

  - /api/v1
  - /apis/$GROUP_NAME/$VERSION  如  /apis/apps/v1
  - /apis/GROUP/VERSION/namespaces/NAMESPACE/KIND-PLURAL 如 /apis/apps/v1/namespaces/default/deployments

- 自定义资源类型

  - 修改K8s源码！？
  - 创建一个自定义API SERER，并聚合到集群中
  - 使用CRD（Custom Resource Definition）

  ![img](https://res.weread.qq.com/wrepub/epub_36511877_43)

### 名称空间

### 节点资源

### 标签与标签选择器 Label。selctor

### 资源注解 Annotation

资源注解可手动添加，也可以**由工具程序自动添加**

* 由声明式配置（如apply）管理的字段
* 构建、发行或镜像相关的信息
* 指向日志、监控、分析或审计仓库的指针
* 调试目的的信息：名称、版本、构建信息等
* 轻量化滚动升级工具的元数据，如config、checkpoints

## 应用部署、运行、管理

### 容器间共享

* 容器是单进程的，Pod可以多容器共享系统资源
  * 容器运行时（Docker）创建基础容器
  * 首先创建一个基础容器作为父容器，而后使用必要的命令选项来创建与父容器共享指定环境的新容器，并管理好这些容器的生命周期即可。
  * ![img](https://res.weread.qq.com/wrepub/epub_36511877_46)
  * 共享资源：PID、IPC、UTS、Network、共享卷
    * UTS：简而言之，UTS名称空间是关于隔离主机名的。

### 容器设计模式

* 单容器模式，仅暴露 run pause stop 3个接口

* 单节点多容器模式

  * Sidecar（边车）最常见的Sidecar容器是日志记录服务、数据同步服务、配置服务和代理服务等

  * Ambassador（大使）大使模式的最佳用例之一是提供对数据库的访问。需要以智能客户端连接至外部的分布式数据库时（例如Redis Cluster等），也可以使用大使来扮演此类的客户端程序。![img](https://res.weread.qq.com/wrepub/epub_36511877_48)

  * Adapter（适配器）大使模式为内部容器提供了简化统一的外部服务视图，适配器模式则刚好反过来，它通过标准化容器的输出和接口，为外界展示了一个简化的应用视图。一个实际的例子就是借助于适配器容器确保系统内的所有容器提供统一的监控接口。![img](https://res.weread.qq.com/wrepub/epub_36511877_49)

  * Initializer（初始化）1. 无法包含，2. 安全原因，3 等待外部环境。

    ![img](https://res.weread.qq.com/wrepub/epub_36511877_50)

    * k8s支持其他初始化方法：admission controllers、admissionwebhooks和PodPresets等。

* 多节点模式

  * 领导者选举模式
    * ![img](https://res.weread.qq.com/wrepub/epub_36511877_51)
  * 工作队列模式
    * ![img](https://res.weread.qq.com/wrepub/epub_36511877_52)
  * 分散/聚集。容器会立即将响应返回给用户，一个很好的例子是MapReduce算法

### Pod生命周期

* Pending/Running/Succeeded/Failed/Unknown
* postStart/preStop 钩子
* 生命周期：
  1. 先创建Pause基础容器，并为后续提供共享的名称空间
  2. 串行运行初始化容器，失败将按resartPolicy处理。
  3. 容器启动会运行主容器上定义的PostStart钩子事件，该步骤失败则重启容器
  4. 运行健康监测（staupProbe，运行容器启动健康状态监测（startupProbe），判定容器是否启动成功；该步骤失败，同样参照restartPolicy定义的策略进行处理；未定义时，默认状态为Success。
  5. 定期进行存活状态监测（liveness）和就绪状态监测（readiness）；存活状态监测失败将导致容器重启，而就绪状态监测失败会使得该容器从其所属的Service对象的可用端点列表中移除。
  6. 终止Pod对象时，会先运行preStop钩子事件，并在宽限期（terminationGrace-PeriodSeconds）结束后终止主容器，宽限期默认为30秒。

![img](https://res.weread.qq.com/wrepub/epub_36511877_53)

## 存储卷与持久化

### 网络存储卷

### 持久存储卷

* PV（PersistentVolumn）PVC（PersistentVolumnClaim）是一个解耦中间层。是全局预先挂载的一段空间。如：Ceph的一个存储映像，一个文件系统或其子目录
* ![img](https://res.weread.qq.com/wrepub/epub_36511877_68)

### CSI

可被Mesos和CloudFoundry等编排系统共同支持，而且能够以容器化形式部署，更加符合云原生的要义。

Node-driver-registrar/external-attacher/external-provisioner 由 k8s 提供的sidecar，以降低CSI开发的复杂度。

![img](https://res.weread.qq.com/wrepub/epub_36511877_73)

#### Longhorn

3个Pod分别使用了一个Longhorn存储卷，每个卷有一个专用的控制器（Engine）资源和两个副本（Replica）资源，它们都是为了便于描述其应用而由Longhorn引入的自定义资源类型。

![img](https://res.weread.qq.com/wrepub/epub_36511877_74)

* Engine容器生命周期与存储卷相同，负责单个存储卷管理。
* 每个节点上运行一个Longhorn Manager（node-driver-registrar）受DaemonSet控制器编排。k8s API使LM创建Engine资源，并在副本节点创建Replica资源
* Longhorn存储插件则基于Longhorn API与Longhorn Manager进行通信。基于iSCSI，

##### 安装步骤

节点要部署 open-iscsi、curl、findmnt、grep、awk、blkid和lsblk

```shell
~$ kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/master/deploy/longhorn.yaml
```

会在默认的longhorn-system名称空间下部署csi-attacher、csi-provisioner、csi-resizer、engine-image-ei、longhorn-csi-plugin和longhorn-manager等应用相关的Pod对象。会默认创建如下面资源清单中定义的名为longhorn的StorageClass资源。

创建PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-dyn-longhorn-demo
  namespace: default
spec:
  accessModes: ["ReadWriteOnce"]
  volumeMode: Filesystem
  resources:
    requests:
      storage: 2Gi
  storageClassName: longhorn
```

```shell
~$ kubectl apply -f pvc-dyn-longhorn-demo.yaml 
persistentvolumeclaim/pvc-dyn-longhorn-demo created
~$ kubectl get pvc/pvc-dyn-longhorn-demo
NAME                    STATUS  VOLUME                                 CAPACITY…
pvc-dyn-longhorn-demo   Bound   pvc-c67415ae-560b-49c7-8515-3467f4160794   2Gi…
```

```shell
~$ kubectl get volumes -n longhorn-system
NAME                                  AGE
pvc-c67415ae-560b-49c7-8515-3467f4160794   90s
~$ kubectl get engines -n longhorn-system
NAME                                            AGE
pvc-c67415ae-560b-49c7-8515-3467f4160794-e-eb822204   2m10s
~$ kubectl get replicas -n longhorn-system
NAME                                         AGE
pvc-c67415ae-560b-49c7-8515-3467f4160794-r-4e2755e3   2m36s
pvc-c67415ae-560b-49c7-8515-3467f4160794-r-ba483050   2m36s
pvc-c67415ae-560b-49c7-8515-3467f4160794-r-daccc0db   2m36s
```

## Service与服务发现

Service对象的IP地址（可称为ClusterIP或ServiceIP）是虚拟IP地址，由Kubernetes系统在Service对象创建时在专用网络（Service Network）地址中自动分配或由用户手动指定，并且在Service对象的生命周期中保持不变

Service基于端口过滤到达其IP地址的客户端请求，并根据定义将请求转发至其后端的Pod对象的相应端口之上，因此这种代理机制也称为“端口代理”或四层代理，工作于TCP/IP协议栈的传输层。



### userspace 代理模型。用户空间和内核空间来回切换效率低

### iptables

在iptables代理模型中，Service的服务发现和负载均衡功能都使用iptables规则实现，而无须将流量在用户空间和内核空间来回切换，因此更为高效和可靠，但是性能一般，而且受规模影响较大，仅适用于少量Service规模的集群。

### ipvs

ipvs也构建于内核中的netfilter之上，但它使用hash表作为底层数据结构且工作于内核空间，因此具有流量转发速度快、规则同步性能好的特性，适用于存在大量Service资源且对性能要求较高的场景。ipvs代理模型支持rr、lc、dh、sh、sed和nq等多种调度算法。

## 应用编排与管理



## 网络模型与网络策略

* CNI K8s不内置网络管理功能，而是由CNI插件完成。
* Flannel
* Canal
* Calico

#### Linux 网络模型

* Network、IPC和UTC名称空间隔离技术是容器能够使用独立网络栈的根本
* 网络设备虚拟化是关键。Linux上的虚拟化设备有：VETH、Bridge、VLAN、MAC VLAN、IP VLAN、VX LAN、MACTV、TAP/IPVTAP。
  * Host模式中，需要避免容器间的端口冲突
  * Bridge模式是Linux内核虚拟网桥，工作于数据链路层，同一宿主机上的容器通过网桥和ARP协议完成本地通讯。在宿主机上网桥拥有IP地址。容器需要某种地址分配组件（IPAM）
    * ![img](https://res.weread.qq.com/wrepub/epub_36511877_137)
    * 容器作为请求方：需要Host iptables SNAT；作为服务方：需要Host iptables DNAT。NAT导致复杂度几何上升，iptables限制了规模和性能
    * ![img](https://res.weread.qq.com/wrepub/epub_36511877_138)



#### 容器网络模型

1. Pod内容器通信

## K8s 超详细总结

https://zhuanlan.zhihu.com/p/377312675

### 两地三中心

![img](https://pic2.zhimg.com/80/v2-a874760c55a497e9f47c6ad0cfcd6a1d_720w.jpg)

### 四层服务发现

![](/Users/gl/github/guileen.github.com/hexo/source/img/osi7/osi7-min.png)

### 五种共享资源

一个Pod中的应用容器共享五种资源：

- PID命名空间：Pod中的不同应用程序可以看到其他应用程序的进程ID。
- 网络命名空间：Pod中的多个容器能够访问同一个IP和端口范围。
- IPC命名空间：Pod中的多个容器能够使用SystemV IPC或POSIX消息队列进行通信。
- UTS命名空间：Pod中的多个容器共享一个主机名。
- Volumes(共享存储卷)：Pod中的各个容器可以访问在Pod级别定义的Volumes。

### 六个常用CNI插件

![img](https://filescdn.proginn.com/a5fea0dc3460b6948a6faecd97ba7852/1e2137a2a4aca908543beac64469099a.webp)

### 七层负载均衡

Ingress是基于7层的

### 八种隔离维度

![img](https://filescdn.proginn.com/71818d6a65695a3142b43107590492e4/27b76a25404efda6192bea58dec6a48c.webp)

### 九个网络模型原则

