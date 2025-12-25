import numpy as np
import matplotlib.pyplot as plt
import math
class Canvas:
    def __init__(self, width, height, color_channels):
        width, height, color_channels = 80, 80, 3
        self.__canvas = np.zeros((height, width, color_channels),dtype=np.uint8)
        print("Init")
    def create_point_set(self,*points):
        if(len(points)%2 != 0):
            raise ValueError("Unfinished coordinate")
        point_set = []
        for i in range(0, len(points), 2):
            temp_set = [points[i], points[(i+1)]]
            point_set.append(temp_set)
        return point_set
    def __line_drawingH(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dx = x1-x0
        print("x0", x0)
        dy = y1-y0
        dir = -1 if dy < 0 else 1
        dy = dy*dir
        y = y0
        p = 2*dy - dx
        for i in range(abs(dx)+1):
            self.put_pixel(x0+i, y)
            if p > 0:
                y += dir
                p = p-2*dx
            p = p+2*dy
    def __line_drawingV(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dx = x1-x0
        #print("x0", x0)
        dy = y1-y0
        dir = -1 if dx < 0 else 1
        dx = dx*dir
        x = x0
        p = 2*dx - dy
        for i in range(abs(dy)+1):
            self.put_pixel(x, y0+i)
            print("p:", p)
            if p > 0:
                x += dir
                print(x)
                p = p-2*dy
            p = p+2*dx
    def draw_line(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dy = y1 - y0
        dx = x1 - x0
        print(dy, dx)
        if(abs(dy)>abs(dx)):
            print("V")
            if(dy<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                print("swapped")
            self.__line_drawingV(x0, y0, x1, y1, thickness, color)
        else:
            print("H")
            if(dx<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            self.__line_drawingH(x0, y0, x1, y1, thickness, color)
    def draw_poly(self,point_set: list, thickness = 0, color = (255,255,255)):
        l = len(point_set)
        if(l<3):
            raise ValueError("Requires at least 3 points")
        for i in range(l):
            self.draw_line(point_set[i][0], point_set[i][1],point_set[(i+1)%l][0], point_set[(i+1)%l][1],thickness, color)

    def put_pixel(self, x, y, color = (255,255,255)):
        print(x, y)
        self.__canvas[y,x] = color
    def render(self):
        print("opening")
        plt.imshow(self.__canvas)
        plt.axis("off")
        plt.show()
        """def __line_drawing_old(x0, y0, x1, y1, thickness, color=(255,255,255)):
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
            end_pos = math.floor(slope*(x+1)+y0) """

def main():

    canvas = Canvas(80, 30, 3)
    #canvas.draw_line(30,30, 40, 45)
    p1 = canvas.create_point_set(13, 45, 47, 32, 11, 20, 72, 37)
    print("Length",len(p1))
    canvas.draw_poly(p1)
    canvas.render()
    #canvas[400:500, 100:400] = (255,255,255)

    """plt.imshow(canvas)
    plt.axis("off")
    plt.show()"""



if __name__ == "__main__":
        main()


    
  
