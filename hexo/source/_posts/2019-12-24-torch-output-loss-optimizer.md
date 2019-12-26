---
title: Torch的损失函数和优化器
date: 2019-12-24 22:05:59
categories: AI
---

深度神经网络输出的结果与标注结果进行对比，计算出损失，根据损失进行优化。那么输出结果、损失函数、优化方法就需要进行正确的选择。

# 常用损失函数
pytorch 损失函数的基本用法

```python
criterion = LossCriterion(参数)
loss = criterion(x, y)
```
Mean Absolute Error
torch.nn.L1Loss
Measures the mean absolute error.

## Mean Absolute Error/ L1Loss
nn.L1Loss
![](/img/loss/l1loss.png)
很少使用

## Mean Square Error Loss
nn.MSELoss
![](/img/loss/mseloss.png)
针对数值不大的回归问题。
## Smooth L1 Loss
nn.SmoothL1Loss
![](/img/loss/smoothl1loss.png)
它在绝对差值大于1时不求平方，可以避免梯度爆炸。大部分回归问题都可以适用，尤其是数值比较大的时候。

## Negative Log-Likelihood Loss
torch.nn.NLLLoss，一般与 LogSoftmax 成对使用。使用时 `loss(softmaxTarget, target)`。用于处理多分类问题。
![](/img/loss/nllloss.png)
```python
m = nn.LogSoftmax(dim=1)
loss = nn.NLLLoss()
# input is of size N x C = 3 x 5， C为分类数
input = torch.randn(3, 5, requires_grad=True)
# each element in target has to have 0 <= value < C
target = torch.tensor([1, 0, 4])
output = loss(m(input), target)
output.backward()
```

## Cross Entropy Loss
nn.CrossEntropyLoss 将 LogSoftmax 和 NLLLoss 绑定到了一起。所以无需再对结果使用Softmax
```
loss = nn.CrossEntropyLoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.empty(3, dtype=torch.long).random_(5)
output = loss(input, target)
output.backward()
```

## BCELoss
二分类问题的CrossEntropyLoss。输入、目标结构是一样的。

```python
m = nn.Sigmoid()
loss = nn.BCELoss()
input = torch.randn(3, requires_grad=True)
target = torch.empty(3).random_(2)
output = loss(m(input), target)
output.backward()
```

## Margin Ranking Loss
![](/img/loss/marginrankingloss.png)

常用户增强学习、对抗生成网络、排序任务。给定输入x1，x2，y的值是1或-1，如果y==1表示x1应该比x2的排名更高，y==-1则相反。如果y值与x1、x2顺序一致，那么loss为0，否则错误为 y*(x1-x2)

## Hinge Embedding Loss
y的值是1或-1，用于衡量两个输入是否相似或不相似。

## Cosine Embedding Loss
给定两个输入x1，x2，y的值是1或-1，用于衡量x1和x2是否相似。
![](/img/loss/cosineembeddingloss.png)
其中cos(x1, x2)表示相似度
![](/img/loss/cossim.png)

# 各种优化器

大多数情况Adam能够取得比较好的效果。SGD 是最普通的优化器, 也可以说没有加速效果, 而 Momentum 是 SGD 的改良版, 它加入了动量原则. 后面的 RMSprop 又是 Momentum 的升级版. 而 Adam 又是 RMSprop 的升级版. 不过从这个结果中我们看到, Adam 的效果似乎比 RMSprop 要差一点. 所以说并不是越先进的优化器, 结果越佳.

```python
# SGD 就是随机梯度下降
opt_SGD         = torch.optim.SGD(net_SGD.parameters(), lr=LR)
# momentum 动量加速,在SGD函数里指定momentum的值即可
opt_Momentum    = torch.optim.SGD(net_Momentum.parameters(), lr=LR, momentum=0.8)
# RMSprop 指定参数alpha
opt_RMSprop     = torch.optim.RMSprop(net_RMSprop.parameters(), lr=LR, alpha=0.9)
# Adam 参数betas=(0.9, 0.99)
opt_Adam        = torch.optim.Adam(net_Adam.parameters(), lr=LR, betas=(0.9, 0.99))
```
