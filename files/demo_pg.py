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

import gym

env = gym.make('CartPole-v0').unwrapped

class PolicyNet(nn.Module):
    def __init__(self, input_size, hidden, outputs):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden)
        self.fc2 = nn.Linear(hidden, outputs)

    def forward(self, x):
        x = F.relu(F.dropout(self.fc1(x), 0.1))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

BATCH_SIZE = 256
GAMMA = 0.99
HIDDEN_SIZE = 15
LR = 0.005

n_actions = env.action_space.n
input_size = env.observation_space.shape[0]

policy_net = PolicyNet(input_size, HIDDEN_SIZE, n_actions)
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

print('Complete')
env.render()
env.close()
plt.ioff()
plt.show()
