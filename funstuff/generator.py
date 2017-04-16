#!/usr/bin/python

import math
import numpy
from PIL import Image

equations = []
equations.append("(y == 15 or y == 5) and x < 15 and x > 5")
equations.append("(x == 15 or x == 5) and y < 15 and y > 5")

print equations

im = Image.new('RGB',(20,20))
pix = im.load()
for x in range(0,20):
  for y in range(0,20):
    for eq in equations:
      if eval(eq) == True:
        pix[x,y] = (0,0,0)
        break
      else:
        pix[x,y] = (255,255,255)

im.save("square.png")

