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
    def draw_line(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dy = y1 - y0
        dx = x1 - x0
        print(dy, dx)
        if(abs(dy)>abs(dx)):
            if(dy<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            self.__line_drawingV(x0, y0, x1, y1, thickness, color)
        else:
            print("H")
            if(dx<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            self.__line_drawingH(x0, y0, x1, y1, thickness, color)
    def draw_arc(self, point_set, radius, arc_angle = 360, offset = 0, draw_center = False, thickness = 0, color = (255,255,255)):
        for i in range(len(point_set)):
            cx,cy = point_set[i][0], point_set[i][1]
            if(draw_center):
                self.plot_pixel(cx, cy)
            x = radius
            y = 0
            xp = x*math.cos(math.radians(arc_angle+offset)) - y*math.sin(math.radians(arc_angle+offset))
            yp = x*math.sin(math.radians(arc_angle+offset)) + y*math.cos(math.radians(arc_angle+offset))

            pixel_set = []
            p = 1 - 4*radius
            while y >= -x:
                print("working")
                pixel_set.append([x, y])
                if p > 0:
                    x -= 1
                    p += 4*(-2*(x+y)+1)
                    print("shifted")
                else:
                    p += 4*(-2*y+1)
                y -= 1
            for i in range(len(pixel_set)-1, -1, -1):
                print("iter", i)
                temp = [-pixel_set[i][1], -pixel_set[i][0]]
                pixel_set.append(temp)
            l = len(pixel_set)
            x_sign=1
            y_sign=1
            for i in range(3):
                x = len(pixel_set)
                x_sign = (-1)**(i%2+1)
                y_sign = (-1)**(i%2)
                print("Signs:", x_sign, y_sign, i)
                for j in range(x-1, x-l-1, -1):
                    temp = [x_sign*pixel_set[j][0], y_sign*pixel_set[j][1]]
                    pixel_set.append(temp)
            if(radius == 1):
                degrees_per_pixel = 90
                pixels_count = round(arc_angle/90)
            l = len(pixel_set)
            print("L", l)
            degrees_per_pixel = (360/(l-4)) if radius%2 == 1 else (360/(l-8))
            pixel_count = round(arc_angle/degrees_per_pixel)
            starting_pixel = round(offset/degrees_per_pixel)
            if(radius%2 == 1):
                sections = math.floor(arc_angle/90)
            else:
                sections = math.floor(arc_angle/45)
            print("Starting", starting_pixel, "count", pixel_count, "overlap", sections)
            for i in range(starting_pixel, pixel_count+sections):
                print("Px",pixel_set[i][0],"Py", pixel_set[i][1])
                self.plot_pixel(cx+pixel_set[i][0], cy+pixel_set[i][1], color=color)

            
            return pixel_set
    def draw_poly(self,point_set: list, thickness = 0, color = (255,255,255)):
        l = len(point_set)
        if(l<3):
            raise ValueError("Requires at least 3 points")
        for i in range(l):
            self.draw_line(point_set[i][0], point_set[i][1],point_set[(i+1)%l][0], point_set[(i+1)%l][1],thickness, color)
    def __line_drawingH(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dx = x1-x0
        dy = y1-y0
        dir = -1 if dy < 0 else 1
        dy = dy*dir
        y = y0
        p = 2*dy - dx
        for i in range(abs(dx)+1):
            self.plot_pixel(x0+i, y)
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
            self.plot_pixel(x, y0+i)
            if p > 0:
                x += dir
                print(x)
                p = p-2*dy
            p = p+2*dx
    def plot_point_set(self, point_set, color = (255,255,255)):
        for i in range(len(point_set)):
            self.plot_pixel(point_set[i][0],point_set[i][1], color)
    def plot_pixel(self, x, y, color = (255,255,255)):
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
    #canvas.draw_poly(p1)
    s1 = canvas.draw_arc([[50,35]], 8,360)
    #canvas.plot_point_set(s1)
    canvas.render()




if __name__ == "__main__":
        main()


    
  
