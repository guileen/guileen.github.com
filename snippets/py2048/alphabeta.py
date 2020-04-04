from math import log
import heapq

def count_open_block(map,y,x,W):
  # 检查# 尝试提升奇异格，探索法
  block = map[y][x]
  # 若左右上有接近于自己的则向最接近的搜索
  neighbors = []
  if y>1:
    neighbors.append((map[y-1][x], y-1, x))
  if x>0:
    neighbors.append((map[y][x-1], y, x-1))
  if x<W-1:
    neighbors.append((map[y][x+1], y, x+1))
  open_block = 0
  for neighbor in sorted(neighbors, reverse=True):
    if(neighbor[0]==0):
      open_block += 1
    if(block > neighbor[0]):
      open_block += count_open_block(map, neighbor[1], neighbor[2], W)
  return open_block

def add_connect_blocks(env, y, x, result_set, block_list):
  neighbors = []
  if y > 0:
    neighbors.append((y-1, x))
  # if y < env.h-1:
  #   neighbors.append((y+1, x))
  # if x > 0:
  #   neighbors.append((y, x-1))
  if x < env.w-1:
    neighbors.append((y, x+1))
  for n in neighbors:
    if env.map[y][x] >= env.map[n[0]][n[1]] and not n in result_set:
      result_set.add(n)
      block_list.append(env.map[y][x])
      add_connect_blocks(env, n[0], n[1], result_set, block_list)

def connect_block_ration(env):
  # 最大方块相连方块总和/所有方块总和
  max_pos = (0,0)
  max_block = 0
  total = 0
  all_blocks = []
  for i in range(env.h):
    for j in range(env.w):
      block = env.map[i][j]
      total += block
      all_blocks.append(block)
      if block > max_block:
        max_block = block
        max_pos = (i, j)
  max_pos = (env.h-1, 0)
  pos_set = set()
  block_list = []
  add_connect_blocks(env, max_pos[0], max_pos[1], pos_set, block_list)
  block_sum = sum(block_list)
  # 位置 四方向最大矩形面积占比，代表最大潜力
  # area_ratio = max(max_pos[0],env.h-max_pos[0])*max(max_pos[1], env.w-max_pos[1])/env.h/env.w
  area_ratio = max_pos[0]*(env.w-max_pos[1])
  last_row_conn = []
  i = 0
  block = env.map[env.h-1][i]
  while i < env.w-1:
    if block >= env.map[env.h-1][i+1]:
      last_row_conn.append(block)
    block = env.map[env.h-1][i+1]
    i+=1
  last_row_sum = sum(env.map[env.h-1])
  return area_ratio + \
    10*len(block_list) / len(all_blocks) + \
    10*block_sum / total + \
    100* len(last_row_conn) / env.w + \
    100*sum(last_row_conn) / total + \
    30*sum([b and log(b,2) or 0 for b in last_row_conn]) / sum([b and log(b,2) or 0 for b in all_blocks]) + \
    50*last_row_sum / total + \
    gini_ratio(all_blocks) + \
    gini_ratio([b and log(b,2) or 0 for b in block_list])

def gini_ratio(data):
  if len(data)==0:
    return 1
  data.sort()
  stack = []
  last_sum = 0
  for i in range(len(data)):
    last_sum += data[i]
    stack.append(last_sum)
  B = sum(stack)
  AB = last_sum*(len(data)+1)/2
  if AB == 0:
    return 1
  # print('stack',stack,'B',B,'AB',AB,'A',AB-B,'Gini',(AB-B)/AB)
  return (AB-B) / AB

def gini_index(env):
  # gini = sum(data[i]/total/N) + 2*sum((1-leiji[i])/N) - 1
  data = []
  for i in range(env.h):
    for j in range(env.w):
      block = env.map[i][j]
      if block:
        data.append(block)
  return gini_ratio(data)

def heuristic(env):
  # return gini_index(env)
  return connect_block_ration(env)
  # 方块数量少
  value = 0
  c = 0
  max_block = 0
  # 每一行的平滑度
  for i in range(env.h//2, env.h):
    for j in range(env.w//2):
      block = env.map[i][j]
      if block != 0:
        c+=1
        if block > max_block:
          max_block = block
  #     if j < env.w-1 and block >= env.map[i][j+1]:
  #       value += (block + 1) * (i*10+j)
  #     if j > 0 and block >= env.map[i-1][j]:
  #       value += (block + 1) * (i*10+j)
  # 最后一行的前一半的价值
  for j in range(env.w//2):
    block = env.map[env.h-1][j]
    if block == 0:
      value -= 1000
    else:
      value += block*(env.w//2-j)
  value += 1000000 * count_open_block(env.map, env.h-1, 0, env.w)
  if env.map[env.h-1][0] != max_block:
    value -= 10000000
  return value - c*1000

def add_worst_num(env):
  # add worst num
  c = 0
  for i in range(env.h-1, -1, -1):
    for j in range(env.w):
      if env.map[i][j]==0:
        env.map[i][j] = 2
        c+=1
        if c== 2:
          return

def absearch(env):
  # alpha beta
  def alphabeta(node, depth, alpha, beta, maximizingPlayer):
      if depth == 0:
          return heuristic(node), 0
      if maximizingPlayer:
          best_value = -10000000000
          best_action = 1
          for action in [1,2,4]:
            child = node.clone()
            moved = child.move(action)
            if not moved:
              continue
            v,_ = alphabeta(child, depth - 1, alpha, beta, False)
            if v > best_value:
              best_value = v
              best_action = action
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break # β裁剪
          return best_value,best_action
      else:
          best_value = 10000000000
          for i in range(2):# 随机3次生成2，4位置:
            child = node.clone()
            if i ==0:
              add_worst_num(child)
            else:
              child.randnum()
            v,_ = alphabeta(child, depth - 1, alpha, beta, True)
            if v < best_value:
              best_value = v
            beta = min(beta, v)
            if beta <= alpha:
              break # α裁剪
          return best_value,0

  v,a = alphabeta(env, 3, -10000000, 100000, True)
  return a, v
