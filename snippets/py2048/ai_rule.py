# 基于我的规则来实现
# 1. 自下而上检查每一行。奇数行左侧为默认方向，偶数行右侧为默认方向。
# 2. - 自反默认方向检查每一格
# 3. - - 如果该格上方格与该格相同，则向下。*
# 4. - - 如果该格与右侧格相同，向默认方向移动。*
# 5. - 向左、向右后，是否与下方有重合，如果都有重合，则向反默认方向移动。如果有一个方向有重合，则向该方向移动
# 5. - 该行如果有空格，奇数行则下左、偶数行则下右。*
# 6. - 该行是否保持降序，关注第一个非降序的格子，设为“异化格”。（努力提升该异化格。如何实现？是关键）
# 7. - 该行最小格是哪一格，努力提升该最小格。（如何实现，努力提升某一格）
# 9. - 需提升格，左、右、上如果与该格相同，则向该格合并
# 10. - 需提升格，左、右、上如果小于该格，则将这些格加入待提升格，向外扩张，直到外界的格为0，将该格设为边界格。
# 11. - 统计边界格左、右、上的边的数量，选取最大的那一边的反方向移动。*
from util import getch
from env import Game2048
from alphabeta import absearch, count_open_block
W = 8
H = 8
env = Game2048(W, H)
# env.map[H-1][0]=2**18
# env.map[H-1][1]=2**25
env.render()

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

def make_decision(map, not_move_count, not_move_dir, debug=False):
  a, v = absearch(env)
  return a, 'Alpha-Beta Search %f' % v
  # Rules:
  if not_move_count>2:
    # return down_loop(not_move_dir == LEFT and RIGHT or LEFT), '卡住了'
    return dldr(), '卡住了'
  print('open_block', count_open_block(map, H-1, 0, W))
  strange_block = 0
  strange_pos = None
  # 最底行方向性策略
  start = 0
  end = W
  step = 1
  default_action = LEFT
  strange_block = 0
  try_down = False
  # 遍历每一行
  for i in range(H-1,-1,-1):
    if debug:
      print(i, default_action)
    has_blank = False
    previous_strange_block = strange_block
    previous_strange_pos = strange_pos
    strange_block = 0
    max_block = 0
    for j in range(start, end, step):
      block = map[i][j]
      if block == 0:
        has_blank = True
      else:
        # 非空格
        if i>0 and block == map[i-1][j]:
          return DOWN, '上同'
        if j>0 and block == map[i][j-1]:
          # if i<H/2:
          #   action = compare_left_right_same_down(map, i)
          #   if action:
          #     return action, '左右比较重合'
          return default_action, '平同'
        if block > max_block:
          max_block = block
        if strange_block == 0 and block < 2**30 and j+step >=0 and j+step < W and block < map[i][j+step]:
          # 大于前一格
          strange_block = block
          strange_pos = (i, j)
    # 向左向右后，哪个更与下方重合。（本行首位有异常，本行大于上一行的异常，行小于4行）
    if try_down or i < H-1 and (previous_strange_block and previous_strange_pos[1] < W/2 and max_block>=previous_strange_block and max_block>128):# or (i<4 and not has_blank):
    # if i<4 and not has_blank:
    # (previous_strange_block <= 64 or previous_strange_block == 0) and max_block >= 512 or i<2:
      a, v = absearch(env)
      return a, 'Alpha-Beta Search %d' % v
      # action = compare_left_right_same_down(map, i)
      # if action:
      #   return action, '左右比较重合'
      # try_down = True
    if has_blank:
      # 有空格，下左
      return down_loop(default_action), '有空格'
    # if strange_block and is_block_open(map, strange_pos[0], strange_pos[1]):
    #   continue
      # return down_loop(default_action), '开放奇异格'
    # 本行已满，根据本行情况，决定下一行的方向性策略
    if strange_block and strange_pos[1]<strange_pos[0]-2:
      # 已满未排序, 奇异格权重大。
      # 但是有时需要放弃奇异格（没有希望了
      next_row_dir = try_upgrade_close(map, strange_pos[0], strange_pos[1])
      if debug:
        print('奇异格', strange_pos, next_row_dir)
    elif i>0 and map[i][end-step] < map[i-1][end-step]:
      # 已满已排序，最小行被遮住，往顺方向移动
      next_row_dir = default_action
      if debug:
        print('最小行被遮挡,顺方向',next_row_dir)
    else:
      # 否则，下一行往反方向移动
      next_row_dir = default_action == LEFT and RIGHT or LEFT
      if debug:
        print('正常，下一行反方向',next_row_dir)
    # 根据大策略决定下一行的遍历策略
    if next_row_dir == LEFT:
      start = 0
      end = W
      step = 1
      default_action = LEFT
    else:
      start = W-1
      end = -1
      step = -1
      default_action = RIGHT
  # 全部结束，没有特殊规则
  return dldr(), '默认'

dldr_count=0
def dldr():
  # 下左下右
  global dldr_count
  dldr_count+=1
  if dldr_count>=4:
    dldr_count = 0
  return [DOWN,LEFT,DOWN,RIGHT][dldr_count]

def down_loop(left_right):
  # 下左下左，或者 下右下右
  global last_action
  return last_action==DOWN and left_right or DOWN

def compare_left_right_same_down(map,y):
  # 检查该行，向左，向右之后是否与下方重合，如果重合，则选择该方向。
  def move_row(start, end, step):
    row_after = [0 for i in range(W)]
    p = start
    for i in range(start, end, step):
      block = map[y][i]
      if block != 0:
        if row_after[p] == 0:
          row_after[p] = block
        elif row_after[p] == block:
          row_after[p] += block
        else:
          p+=step
          row_after[p] = block
    return row_after
  def check_same_down(row):
    # 检查与下方相同的价值
    value = 0
    for i in range(W):
      if row[i] == map[y+1][i]:
        # 奇数行右侧相同价值大，偶数行左侧相同价值大，每格价值相加
        value += 2**(y%2==0 and W-i or i+1) + map[y+1][i]
    return value
  if y == H-1:
    return 0
  lvalue = check_same_down(move_row(0, W, 1))
  rvalue = check_same_down(move_row(W-1,-1,-1))
  if lvalue!=0 or rvalue!=0:
    return lvalue > rvalue and LEFT or RIGHT
  return 0

def is_block_open(map,y,x):
  # 检查# 尝试提升奇异格，探索法
  block = map[y][x]
  # 若左右上有接近于自己的则向最接近的搜索
  neighbors = []
  if y>0:
    neighbors.append((map[y-1][x], y-1, x))
  if x>0:
    neighbors.append((map[y][x-1], y, x-1))
  if x<W-1:
    neighbors.append((map[y][x+1], y, x+1))
  for neighbor in sorted(neighbors, reverse=True):
    if(neighbor[0]==0):
      return True
    if(block > neighbor[0]):
      if is_block_open(map, neighbor[1], neighbor[2]):
        return True
  return False

def try_upgrade_close(map, y, x):
  # 尝试提升奇异格，简单规则法
  block = map[y][x]
  # 如果上方等自己，则向该方向集中
  if y>0:
    max_block = 0
    for i in range(W):
      if map[y-1][i] > max_block:
        max_block = map[y-1][i]
      if map[y-1][i] == block:
        #move i to x
        return i < x and RIGHT or LEFT
  if y>0 and block >= map[y-1][x]:
    # print('block',y,x,'>=',y-1,x)
    return x<W/2 and LEFT or RIGHT
  # 如果上方大于自己，则向反方向移动
  else:
    # print('block',y,x,'<',y-1,x)
    return x<W/2 and RIGHT or LEFT

def try_upgrade_block(map, y, x):
  # 尝试提升奇异格，探索法
  block = map[y][x]
  # 若邻近有相同的则直接合并
  if y>0 and block == map[y-1][x]:
    return DOWN
  elif x>0 and block == map[y][x-1]:
    return RIGHT
  elif x<W-1 and block == map[y][x+1]:
    return LEFT
  # 若左右上有接近于自己的则向最接近的搜索
  neighbors = []
  if y>0:
    neighbors.append((map[y-1][x], y-1, x))
  if x>0:
    neighbors.append((map[y][x-1], y, x-1))
  if x<W-1:
    neighbors.append((map[y][x+1], y, x+1))
  for neighbor in sorted(neighbors, reverse=True):
    if(block > neighbor[0] and neighbor[0]>0):
      action = try_upgrade_block(map, neighbor[1], neighbor[2])
      if action:
        return action

done = False
not_move_count = 0
not_move_dir = 0
step_count = 0
last_action = 0
while not done:
  c = 'x' #getch()
  env.render()
  pass_step = 1
  if c=='q':
    break
  elif c=='z':
    pass_step = 1000
  elif c=='x':
    pass_step = 100
  elif c=='v':
    pass_step = 10
  for i in range(pass_step):
    step_count+=1
    action, reason = make_decision(env.map, not_move_count, not_move_dir, i==0)
    last_action = action
    _,moved,done,_ = env.step(action)
    if not moved:
      not_move_count += 1
      if action == LEFT or action == RIGHT:
        not_move_dir = action
    else:
      not_move_count = 0
  # if(step_count%10==0):
  print(action, reason)
env.render()
