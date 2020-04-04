import env
import random
from util import getch
game = env.Game2048(4,4)
game.render()
i=0
t=0
while True:
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
