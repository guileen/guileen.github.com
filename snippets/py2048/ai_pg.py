from collections import namedtuple
import random
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from torch.distributions.categorical import Categorical

from env import Game2048

env = Game2048(4,4)

class PolicyNet(nn.Module):
    def __init__(self, input_size, h1, h2, outputs):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(input_size, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, outputs)

    def forward(self, x):
        x = F.relu(F.dropout(self.fc1(x), 0.1))
        x = self.fc2(x)
        x = self.fc3(x)
        return F.softmax(x, dim=1)

BATCH_SIZE = 256
GAMMA = 0.99
HIDDEN_SIZE = 32
LR = 0.005

n_actions = len(env.action_space)
input_size = env.w*env.h #env.observation_space.shape[0]

policy_net = PolicyNet(input_size, 32, 16, n_actions)
optimizer = optim.Adam(policy_net.parameters(), lr=LR)

steps_done = 0

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

episode_durations = []

def plot_durations():
    plt.figure(2)
    plt.clf()
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated


def optimize_model():
    # 仅关心最后 n 条数据
    size = len(rewards)
    n = min(BATCH_SIZE, size)
    values = []
    v = 0
    for reward in reversed(rewards):
        v = v * GAMMA + reward
        values.insert(0, v)
    mean = np.mean(values)
    std = np.std(values)
    for i in range(size):
        values[i] = (values[i] - mean) / std
    # loss = - vt * ln π(At, St)
    loss = []

    for i in np.random.choice(size, n):
        loss.append(- values[i] * log_probs[i])
    loss = torch.cat(loss).sum()

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()

num_episodes = 5000
sub_episode = 0
for i_episode in range(num_episodes):
    state = env.reset()
    for t in count():
        action = select_action(state)
        next_state, reward, done,_ = env.step(action.item()+1)
        if sub_episode % 10 == 0:
            env.render()
        if done:
          reward = -1000+t
        elif reward==0:
          # 非法移动，视同失败
          reward = -1000
        else:
          reward = math.log(t+1,2)
        # for num in next_state:
        #   if num != 0:
        #     reward += 0.1
        rewards.append(reward)
        state = next_state
        # if done or (t>=1000 and t % 1000 == 0) and len(rewards)>1:
        if done:
            optimize_model()
            sub_episode += 1
            print('EP', i_episode, sub_episode)
            # episode_durations.append(t+1)
            episode_durations.append(max(*next_state))
            plot_durations()
            rewards = []
            log_probs = []
        if done:
          break

print('Complete')
env.render()
env.close()
plt.ioff()
plt.show()
