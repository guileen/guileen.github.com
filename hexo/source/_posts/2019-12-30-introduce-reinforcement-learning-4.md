---
title: 强化学习简介（四）：DQN实战
date: 2019-12-30 14:37:03
tags:
categories: AI
---

我们在上文简述了DQN算法。此文以PyTorch来实现一个DQN的例子。我们的环境选用[CartPole-v1](https://gym.openai.com/envs/CartPole-v1/)。我们的输入是一幅图片，动作是施加一个向左向右的力量，我们需要尽可能的保持木棍的平衡。

![CartPole-v1](/files/cartpole-v1.gif)

对于这个环境，尝试了很多次，总是不能达到很好的效果，一度怀疑自己的代码写的有问题。后来仔细看了这个环境的奖励，是每一帧返回奖励1，哪怕是最后一帧也是返回1 的奖励。这里很明显是不合理的俄。我们需要重新定义这个奖励函数，也就是在游戏结束的时候，给一个比较大的惩罚，r=-100。很快可以达到收敛。

## Replay Memory

```python
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

class ReplayMemory:
    def __init__(self, capacity):
        self.cap = capacity
        self.mem = []
        self.pos = 0

    def push(self, *args):
        """Save a transition."""
        if len(self.mem) < self.cap:
            self.mem.append(None)
        self.mem[self.pos] = Transition(*args)
        self.pos = (self.pos + 1) % self.cap

    def sample(self, batch_size):
        return random.sample(self.mem, batch_size)

    def __len__(self):
        return len(self.mem)
```

## Q网络

```python
class DQN(nn.Module):
    def __init__(self, input_size, hidden, outputs):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden)
        self.fc2 = nn.Linear(hidden, outputs)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

## 初始化参数和状态

```python
import gym

env = gym.make('CartPole-v0').unwrapped

BATCH_SIZE = 128
GAMMA = 0.9
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10
LR = 0.01

n_actions = env.action_space.n
input_size = env.observation_space.shape[0]

# 策略网络
policy_net = DQN(input_size, 10, n_actions)
# 目标网络
target_net = DQN(input_size, 10, n_actions)
# 目标网络从策略网络复制参数
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
memory = ReplayMemory(10000)
```

## 探索和选择最佳动作

```python
steps_done = 0

def select_action(state, no_explore=False):
    x = torch.unsqueeze(torch.FloatTensor(state), 0)
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold or no_explore:
        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(x).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], dtype=torch.long)

```

## 优化模型(关键代码)

这里主要是抽样、目标值计算、损失计算的部分。损失计算采用Huber loss。

```python
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    non_final_mask = torch.tensor(tuple(map(lambda  s: s is not None,
                        batch.next_state)), dtype=torch.uint8)
    non_final_next_states = torch.FloatTensor([s for s in batch.next_state if s is not None])
    state_batch = torch.FloatTensor(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.FloatTensor(batch.reward)
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    # 限制网络更新的幅度，可以大幅提升训练的效果。
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()
```

## 训练循环

这里主要有主循环、获取输入、记录回放、训练、复制参数等环节。

```python
num_episodes = 1000
for i_episode in range(num_episodes):
    state = env.reset()
    for t in count():
        action = select_action(state, i_episode%50==0)
        if(i_episode%50==0):
            env.render()
        next_state, reward,done,_ = env.step(action.item())
        # reward = torch.tensor([reward])
        if done:
            reward = -100
        memory.push(state, action, next_state, reward)
        state = next_state
        if done or t > 2500:
            for i in range(10):
                optimize_model()
            episode_durations.append(t+1)
            plot_durations()
            break
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
```

![Clamp](/files/dqn2.png)

[完整代码](/files/demo_dqn.py)
