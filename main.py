import numpy as np
import matplotlib.pyplot as plt
import math

def line_drawing(x0, y0, x1, y1, thickness, color=(255,255,255)):

    dx = x1-x0
    print("x0", x0)
    dy = y1-y0
    if(dy>dx):
        temp = dx
        dx = dy
        dy = temp
    dir = -1 if dy < 0 else 1
    y = y0
    p = 2*dy - dx
    for i in range(abs(dx)+1):
        put_pixel(x0+i, y)
        if p > 0:
            y += dir
            p = p-2*dx
        p = p+2*dy
    
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

def put_pixel(x, y, color = (255,255,255)):
    canvas[y,x] = color

width, height, color_channels = 80, 60, 3
canvas = np.zeros((height, width, 3),dtype=np.uint8)

line_drawing(30, 20, 40, 40, 0)

#canvas[400:500, 100:400] = (255,255,255)

plt.imshow(canvas)
plt.axis("off")
plt.show()


    
    