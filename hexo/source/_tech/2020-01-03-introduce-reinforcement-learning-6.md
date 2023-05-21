---
title: 强化学习简介（六）：策略梯度实例
date: 2020-01-03 14:40:51
tags:
categories: AI
---

和第四节DQN的实例一样，我们依然使用CartPole-v1来作为训练环境。策略梯度的网络和DQN的网络结构是类似的，只是在输出层需要做Softmax处理，因为策略梯度的输出本质上是一个分类问题——将某一个状态分类到某一个动作的概率。而DQN网络则是一个回归问题——某一个网络在各个动作的Q值是多少。

```python
class PolicyNet(nn.Module):
    def __init__(self, input_size, hidden, outputs):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden)
        self.fc2 = nn.Linear(hidden, outputs)

    def forward(self, x):
        x = F.relu(F.dropout(self.fc1(x), 0.1))
        x = self.fc2(x)
        # 输出层需要使用softmax
        return F.softmax(x, dim=1)
```

不要忘了输出层的SoftMax。

## 初始化参数

相对于DQN，我们也不需要额外的目标网络和参数复制操作，只需要一个策略网络即可。

```python
BATCH_SIZE = 256
GAMMA = 0.99
HIDDEN_SIZE = 15
LR = 0.005

n_actions = env.action_space.n
input_size = env.observation_space.shape[0]

policy_net = PolicyNet(input_size, HIDDEN_SIZE, n_actions)
optimizer = optim.Adam(policy_net.parameters(), lr=LR)

steps_done = 0
```

## 选择动作

在选择动作时，我们不再需要特地设置探索概率，因为输出结果就是各个动作的概率分布。我们使用`torch.distributions.categorical.Categorical` 来进行取样。在每次选择动作时，我们同时记录对应的概率，以便后续使用。这个概率就是 \`ln pi_theta(S_t,A_t)\`

```python
log_probs = []
rewards = []

def select_action(state):
    x = torch.unsqueeze(torch.FloatTensor(state),0)
    probs = policy_net(x)
    c = Categorical(probs)
    action = c.sample()
    # log action probs to plt
    prob = c.log_prob(action)
    log_probs.append(prob)
    return action
```

## 优化模型

为了更新参数，我们首先需要计算\`v_t\`，这在后续参数迭代中需要用到。

- \` v_t = r_(t+1) + gamma * v_(t+1) \`

在模拟执行的时候，我们记录了每一步的reward，我们需要计算每一步的\`v_t\`，其顺序与执行顺序一致。根据公式我们需要倒序的计算\`v_t\`，然后将计算好的结果倒序排列，就形成了\`v_1,v_2...v_t\`的序列。最后我们需要将数据标准化。(TODO: 这里可能存在一个序列对应的问题，其中每一个状态的累计收益，是后续状态收益之和，不包含本轮收益)

```python
values = []
v = 0
for reward in reversed(rewards):
    v = v * GAMMA + reward
    values.insert(0, v)
mean = np.mean(values)
std = np.std(values)
for i in range(size):
    values[i] = (values[i] - mean) / std
```

接下来我们需要更新参数，参数更新的公式为：

- \` theta larr theta + alpha v_t ln pi_theta (A_t|S_t) \`

我们将其转换为损失函数形式:

- \` L(theta) = - v_t ln pi_theta(A_t|S_t) \`

这个损失函数的形式可以帮助我们更好的理解策略梯度的原理。如果一个动作价值为负值，但是其选择概率为正，则损失较大。

```python
    loss = []
    for i in np.random.choice(size, n):
        loss.append(- values[i] * log_probs[i])
    loss = torch.cat(loss).sum()

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()
```

## 训练循环

训练循环需要在一局结束之后进行。并清除rewards、log_probs缓存。对于cartpole-v1环境，要注意他的每一步奖励都是1，很显然在最后一步代表着游戏失败，我们需要施加一定的惩罚，我们将最后一步的奖励设为-100。

```python
num_episodes = 5000
for i_episode in range(num_episodes):
    state = env.reset()
    for t in count():
        action = select_action(state)
        if i_episode % 2000 == 0:
            env.render()
        next_state, reward, done,_ = env.step(action.item())
        if done:
            reward = -100
        rewards.append(reward)
        state = next_state
        if done or t >= 2500:
            optimize_model()
            print('EP', i_episode)
            episode_durations.append(t+1)
            plot_durations()
            rewards = []
            log_probs = []
            break
```

![Clamp](/files/cart-pg.png)

[完整代码](/files/demo_dqn.py)
