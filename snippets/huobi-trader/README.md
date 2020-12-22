https://github.com/HuobiRDCenter/huobi_Python

```
python3 setup.py install
pip3 install 'tzlocal<3'
```

# 1
unix_time,y,m,d,week-of-year,day-of-week,hour,minute,second,
candle(high,low,open,close,count,amount,volume),candle_normal()
history_candle_input....(不同尺度的N个)，（other board state）

## 输出动作空间
输出1维预测概率， 0~1 之间，根据预测概率决定 动作。
无、持、出5档、入5档（5，10，20，40，70，100）。

## 算法 DQN

## 实时订阅事件并模拟操作

## 随机复盘计算

## 核心问题！
输入数据本身是有限的。模式不可持续，未来不确定。结果可能是个火鸡科学家。

### 使用GAN生成一个行情生成器

### 引入其他市场（外汇、美股）进行模拟


# 方法2 random trader -> market simulation -> train AI trader
理论：市场由不同性格（风险、谨慎）、不同认知(喜欢追涨杀跌还是喜欢反向交易）、下场率（长线、短线）的交易员构成，通过自然选择，会留下幸存的交易员，也会有新的随机小额玩家加入市场。交易员决定了买卖，买卖决定了价格，AI根据价格反推策略。交易员买卖原则，希望用更少的钱购买，希望用更高的价格售出。市场撮合。交易员出价时有个心理价格,


# 方法3 简单规则引擎——反弹
观测一个时间窗口，符合某个条件，则实施操作，止损平仓，获利减仓。



