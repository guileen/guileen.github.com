import env
import random
from util import getch
game = env.Game2048(4,4)
game.render()
i=0
t=0
t_map = [[0 for j in range(game.w)] for i in range(game.h)]

def copy_map(s, d):
  for i in range(len(s)):
    for j in range(len(s[i])):
      d[i][j] = s[i][j]

def evaluate(m, w, h):
  v = 0
  for i in range(h-1):
    for j in range(w-1):
      l = w-j
      #上大于下，右大于左
      a = m[i][j] > m[i+1][j]
      b = m[i][j+1] > m[i][j]
      if a and b:
        v -= i*100+(w-j)*50
      elif a:
        v -= (w-j)*10
      elif b:
        v -= i*20
  if m[0][0]==0:
    v -= 1000
  return v

def smart_action_2(t):
  best_action = 2
  best_score = -1000000
  for a in [1,4]:
    copy_map(game.map, t_map)
    moved = env.move(t_map, a, game.w, game.h)
    if moved:
      value = evaluate(t_map, game.w, game.h)
      if value > best_score:
        best_score = value
        best_action = a
  return best_action

last_action = 0
def samrt_action(t):
  for i in range(game.h-1,0,-1):
    # 从基座开始扫描
    for j in range(game.w):
      # 从左下开始扫描
      x = game.map[i][j]
      if x == 0:
        continue
        # 如果有空格，比较上侧和右侧的方块大小
        fu = 0
        fr = 0
        for hh in range(i, 0, -1):
          fu = game.map[hh][j]
          if fu!=0:
            break
        for hh in range(j, game.w):
          fr = game.map[i][hh]
          if fr!=0:
            break
        if fu or fr:
          # 如果移动后出现右边比左边大，上边比下边大的情况，则反之而行

          # 右侧或上侧都有方块，上侧大则向下，右侧大则向左
          # print('emtpy return', i, j, fu, fr)
          return fu >= fr and 4 or 1
      if j<game.w-1 and x == game.map[i-1][j+1]:
        # 三角形
        if x == game.map[i-1][j]:
          # print('triangle')
          return 4
        elif x == game.map[i][j+1]:
          # print('back triangle')
          return 1
      if j>0 and x == game.map[i-1][j-1] and x == game.map[i-1][j]:
        return 4
  global last_action
  last_action = last_action == 1 and 4 or 1
  return last_action

def smart_loop():
  for t in count():
    a = samrt_action(t)
    # a = smart_action_2(t)
    _,moved,done,_ = game.step(a)
    # if moved == 0:
    #   _,moved,done,_ = game.step(2)
    if t >= 0 or done or moved==0:
      return done

def loop_action(actions, n, stop_on_no_move=True):
  for _ in range(n):
    for a in actions:
      if a == 5:
        a = random.randint(1,4)
      _,moved,done,_ = game.step(a)
      if done or (stop_on_no_move and moved==0):
        return done
  return False

while True:
  c = getch()
  if c == 'q':
    break
  if c == 'z' or c == 'x':
    done = loop_action([1,4], c == 'z' and 100 or 10)
    game.render()
    if done:
      break
    continue
  if c == 'f':
    done = smart_loop()
    game.render()
    if done:
      break
    continue
  if c == 'v':
    done = loop_action([1,4],100)
    game.render()
    if done:
      break
    continue
  if c == 'g':
    done = loop_action([1,4,2,4,1,4],100,False)
    game.render()
    if done:
      break
    continue
  if c == 'h' or c == 'a':
    a = 1
  elif c == 'l' or c == 'd':
    a = 2
  elif c == 'k' or c == 'w':
    a = 3
  elif c == 'j' or c == 's':
    a = 4
  else:
    continue

  if a:
    _,_,done,_ = game.step(a)
    game.render()
    print('ASWD  Z-AS*100  X-random*100')
    if done:
      break
