import numpy as np
import matplotlib.pyplot as plt
import math

def line_drawingH(x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
    dx = x1-x0
    print("x0", x0)
    dy = y1-y0
    dir = -1 if dy < 0 else 1
    dy = dy*dir
    y = y0
    p = 2*dy - dx
    for i in range(abs(dx)+1):
        put_pixel(x0+i, y)
        if p > 0:
            y += dir
            p = p-2*dx
        p = p+2*dy
def line_drawingV(x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
    dx = x1-x0
    #print("x0", x0)
    dy = y1-y0
    dir = -1 if dx < 0 else 1
    dx = dx*dir
    x = x0
    p = 2*dx - dy
    for i in range(abs(dy)+1):
        put_pixel(x, y0+i)
        print("p:", p)
        if p > 0:
            x += dir
            print(x)
            p = p-2*dy
        p = p+2*dx
def line_drawing(x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
    dy = y1 - y0
    dx = x1 - x0
    print(dy, dx)
    if(abs(dy)>abs(dx)):
        print("V")
        if(dy<0):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            print("swapped")
        line_drawingV(x0, y0, x1, y1, thickness, color)
    else:
        print("H")
        if(dx<0):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        line_drawingH(x0, y0, x1, y1, thickness, color)
def put_pixel(x, y, color = (255,255,255)):
    canvas[y,x] = color

width, height, color_channels = 80, 80, 3
canvas = np.zeros((height, width, 3),dtype=np.uint8)

#line_drawing(0, 20, 40, 0)
line_drawing(10, 40, 0, 10)

#canvas[400:500, 100:400] = (255,255,255)

plt.imshow(canvas)
plt.axis("off")
plt.show()


    
  
def line_drawing_old(x0, y0, x1, y1, thickness, color=(255,255,255)):
    y_dif = y1-y0
    x_dif = x1-x0
    slope = y_dif/x_dif
    end_pos = y0
    print(x_dif, abs(x_dif), slope, math.ceil(slope))
    for x in range(abs(x_dif)+1):
        neg = 1
        if slope<0:
            neg = -1
        r = math.ceil(neg*slope)
        if(neg == 1):
            canvas[(end_pos-thickness):(r+end_pos+thickness), (x+x0)] = color
        else:
            canvas[(-r+end_pos-thickness):(end_pos+thickness), (x+x0)] = color
        print("r:", r, "end:", end_pos)
        end_pos = math.floor(slope*(x+1)+y0)