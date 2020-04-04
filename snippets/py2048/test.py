import env
import random
from util import getch
game = env.Game2048(8,8)

for i in range(8):
  for j in range(8):
    game.map[i][j] = 2**(i*8+ (i%2==0 and j+1 or 8-j) -1)
game.map[0][0] = 2
game.render()
i=0
t=0
while False:
  # for i in range(32):
  #   print(fmtnum(pow(2, i)))
  # break
  c = getch()
  if c == 'q':
    break
  if c == 'h' or c == 'a':
    a = 1
  elif c == 'l' or c == 'd':
    a = 2
  elif c == 'k' or c == 'w':
    a = 3
  elif c == 'j' or c == 's':
    a = 4
  if a:
    _,_,done,_ = game.step(a)
    # if t%100==0 or done:
    game.render()
    # time.sleep(0.01)
    if done:
      break
