---
title: 强化学习简介（二）：Q-learning实战
date: 2019-12-27 16:02:19
categories: AI
---

我们现在通过一个例子来演练Q-learning算法。在练习强化学习之前，我们需要拥有一个模拟器环境。我们主要的目的是学习编写机器人算法，所以对模拟器环境部分不推荐自己写。直接使用`gym`来作为我们对实验环境。安装方法：

```shell
pip install gym
```

## 初识环境

我们的实验环境是一个冰湖滑行游戏，你将控制一个agent在冰面到达目标终点，前进方向并不总受你的控制，你还需要躲过冰窟。

```python
import gym
# 构造游戏环境
env = gym.make('FrozenLake-v0')
# 动作空间-> Discrete(4)
print(env.action_space)
# 状态空间-> Discrete(16)
print(env.observation_space)
# 初始化游戏环境，并得到状态s
s = env.reset()
for _ in range(10):
    # 渲染游戏画面
    env.render()
    # 从动作空间中随机选择一个动作a
    a = env.action_space.sample()
    # 执行动作a，得到新状态s，奖励r，是否完成done
    s, r, done, info = env.step(a) # take a random action
    print(s, r, done, info)
# 关闭环境
env.close()
```

游戏画面示意如下：

```txt
SFFF       (S: 起点，安全)
FHFH       (F: 冰面，安全)
FFFH       (H: 冰窟，进入则失败)
HFFG       (G: 终点，到达则成功)
```

## Agent结构

```python
import random
import math
import gym

class QLAgent():
    q = None
    action_space = None
    epsilon = 0.1 # 探索率
    gamma = 0.99  # 衰减率
    lr = 0.1 # 学习率
    def __init__(self, action_space, state_count, epsilon=0.1, lr=0.1, gamma=0.99):
        self.q = [[0. for a in range(action_space.n)] for s in range(state_count)]
        self.action_space = action_space
        self.epsilon = epsilon
        self.lr = lr
        self.gamma = gamma

    # 根据状态s，选择动作a
    def choose_action(self, s):
        pass

    # 更新状态变化并学习，状态s执行了a动作，得到了奖励r，状态转移到了s_
    def update_transition(self, s, a, r, s_):
        pass
```

这是一个Agent的一般结构，主要由初始化、选择动作、更新状态变化，三个方法构成。后续的其他算法将依然采用该结构。q表数据使用一个二维数组表示，其大小为 state_count action_count，对于这个项目而言是一个 \`16*4\` 的大小。

## 添加Q-table的辅助方法

```python
    # 返回状态s的最佳动作a、及其r值。
    def argmax(self, s):
        max_r = -math.inf
        max_a = None
        for a in range(self.action_space.n):
            r = self.q_get(s, a)
            if r > max_r:
                max_a = a
                max_r = r
        return max_a, max_r
    # 获得 状态s，动作a 对应的r值
    def q_get(self, s, a):
        return self.q[s][a]
    # 更新 状态s 动作a 对应的r值
    def q_put(self, s, a, v):
        self.q[s][a] = v
```

## Q-learning的关键步骤

```python
    def choose_action(self, s):
        if random.random() < self.epsilon:
            # 按一定概率进行随机探索
            return self.action_space.sample()
        # 返回最佳动作
        a, _ = self.argmax(s)
        return a

    def update_transition(self, s, a, r, s_):
        q = self.q_get(s, a)
        _, r_ = self.argmax(s_)
        # Q <- Q + a(Q' - Q)
        # <=> Q <- (1-a)Q + a(Q')
        q = (1-self.lr) * q + self.lr * (r + self.gamma * r_)
        self.q_put(s, a, q)
```

## 训练主循环

我们进行10000局游戏的训练，每局游戏执行直到完成。

```python
env = gym.make('FrozenLake-v0')
agent = QLAgent(env.action_space, env.observation_space.n)
for epoch in range(10000):
    s = env.reset()
    done = False
    while not done:
        # env.render()  # 训练过程不需要渲染
        a = agent.choose_action(s) # 选择动作
        s_, r, done, info = env.step(a) # 执行动作
        agent.update_transition(s, a, r, s_) # 更新状态变化
        s = s_
# 显示训练后的Q表
print(agent.q)
```

## 测试效果

在测试中，我们只选择最佳策略，不再探索，也不再更新Q表。

```python
# 获胜次数
total_win = 0
for i in range(10000):
    s = env.reset()
    done = False
    while not done:
        # 选择最佳策略
        a, _ = agent.argmax(s)
        # 执行动作 a
        s_, r, done, info = env.step(a)
        if done and r == 1:
            total_win += 1
        s = s_
print('Total win=', total_win)
env.close()
```

最终测试的效果是在1万局中获胜了7284次，说明达到了不错的实验效果。
