import random
import sys, termios, tty
from os import system, name
import math
import time

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def rgbToAnsi256(r, g, b):
    if (r == g and g == b):
        if (r < 8):
            return 16
        if (r > 248):
            return 231
        return round(((r - 8) / 247) * 24) + 232

    ansi = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    return ansi
def fmtnum(n, is_new=False):
  if n == 0:
    return '\033[47m    \033[0m'
  l = math.log(n, 2)
  if l == 1:
    bg = rgbToAnsi256(is_new and 150 or 120,120,120)
  elif l == 2:
    bg = rgbToAnsi256(is_new and 120 or 64,64,64)
  else:
    bg = rgbToAnsi256(l*8,max(180-l*12,0),20+l*2)

  unit = ''
  if n < 1000:
    unit = ' '
  elif n < 1000000:
    unit = 'K'
    n //= 0x400
  elif n < 1000000000:
    unit = 'M'
    n //= 0x100000
  else:
    unit = 'G'
    n //= 0x40000000
  s = '%d' % n
  l = (3-len(s))//2
  s = ' ' * (3 - len(s)-l) + s + unit + ' ' * l

  return "\033[1;37;48;5;%dm%s\033[0m" % (bg,s)

for i in range(30):
  print(fmtnum(pow(2,i)))

def move(map, a, w, h):
  # return next_state, reward, done, _
  moved = False
  if a == 1:
    # 1 to left
    for i in range(h):
      lastx = 0
      q = 0 # 0
      for j in range(w):
        x = map[i][j]
        if x!=0:
          map[i][j] = 0
          if x == lastx:
            map[i][q-1] = x * 2
            lastx = 0
            moved = True
          else:
            map[i][q] = x
            if q != j:
              moved = True
            lastx = x
            q += 1
  elif a == 2:
    # 2 to right
    for i in range(h-1, -1, -1):
      lastx = 0
      q = w - 1 # 0
      for j in range(w-1, -1, -1):
        x = map[i][j]
        if x!=0:
          map[i][j] = 0
          if x == lastx:
            map[i][q+1] = x * 2
            lastx = 0
            moved = True
          else:
            map[i][q] = x
            if q!=j:
              moved = True
            lastx = x
            q -= 1
  elif a == 3:
    # 3 to top
    for j in range(w):
      lastx = 0
      q = 0
      for i in range(h):
        x = map[i][j]
        if x!=0:
          map[i][j] = 0
          if x == lastx:
            map[q-1][j] = x * 2
            lastx = 0
            moved = True
          else:
            map[q][j] = x
            if q!=i:
              moved = True
            lastx = x
            q += 1
  elif a == 4:
    # 4 to bottom
    for j in range(w-1,-1,-1):
      lastx = 0
      q = h-1
      for i in range(h-1,-1,-1):
        x = map[i][j]
        if x!=0:
          map[i][j] = 0
          if x == lastx:
            map[q+1][j] = x * 2
            lastx = 0
            moved = True
          else:
            map[q][j] = x
            if q != i:
              moved = True
            lastx = x
            q -= 1
  return moved

class Game2048:

  def __init__(self, w=8, h=8):
    self.w = w
    self.h = h
    self.new_pos = [(0,0),(0,0)]
    self.action_space = [1,2,3,4]
    self.reset()

  def clone(self):
    env = Game2048(self.w, self.h)
    for i in range(self.w):
      for j in range(self.h):
        env.map[i][j] = self.map[i][j]
    return env

  def get_state(self):
    return [math.log(self.map[i][j] or 1, 2) for j in range(self.w) for i in range(self.h)]

  def reset(self):
    self.map = [[0 for j in range(self.w)] for i in range(self.h)]
    self.randnum()
    return self.get_state()

  def randnum(self):
    self.new_pos.clear()
    empty = []
    for i in range(self.h):
      for j in range(self.w):
        if self.map[i][j] == 0:
          empty.append((i,j))
    for i in range(2):
      if len(empty) > 0:
        n = random.randint(0, len(empty) - 1)
        pt = empty.pop(n)
        self.new_pos.append(pt)
        self.map[pt[0]][pt[1]] = random.random() > 0.1 and 2 or 4

  def is_done(self):
    for i in range(self.h):
      for j in range(self.w):
        x = self.map[i][j]
        # empty or same neighbour is not done
        if x == 0 or (j < self.w-1 and x==self.map[i][j+1]) or (i<self.h-1 and x==self.map[i+1][j]):
          return False
    return True

  def move(self, a):
    return move(self.map, a, self.w, self.h)

  def step(self, a):
    moved = self.move(a)
    if moved:
      self.randnum()
    return self.get_state(), moved and 1 or 0, self.is_done(), 0

  def render(self):
    pos = self.new_pos
    clear()
    for i in range(self.h):
      print('')
      for j in range(self.w):
        is_new = (len(pos)>0 and i == pos[0][0] and j == pos[0][1]) or (len(pos)>1 and i == pos[1][0] and j == pos[1][1])
        print(fmtnum(self.map[i][j],is_new), end='')
        print(' ', end='')
      print('')
