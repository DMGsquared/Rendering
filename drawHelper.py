import numpy as np
import matplotlib.pyplot as plt
import math
import heapq

class Canvas:
    def __init__(self, width, height, color_channels = 3, pixel_to_point_ratio = 1):
        self.point_width, self.point_height = width, height
        self.width, self.height, self.color_channels = width*pixel_to_point_ratio, height*pixel_to_point_ratio, color_channels
        self._canvas = np.zeros((self.height, self.width, color_channels),dtype=np.uint8)
        self.ptp = pixel_to_point_ratio
        print("Init")
    def create_point_set(self, *points: int):
        if(len(points)%2 != 0):
            raise ValueError("Unfinished coordinate")
        point_set = []
        for i in range(0, len(points), 2):
            temp_set = [points[i]*self.ptp, points[(i+1)]*self.ptp]
            point_set.append(temp_set)
        return point_set
    def insert_points(self, point_set: list, *points):
        if(len(points)%2 != 0):
            raise ValueError("Unfinished coordinate")
        for i in range(0, len(points), 2):
            temp_set = [points[i], points[(i+1)]]
            point_set.append(temp_set)
    def combine_sets(self, point_sets):
        new_set = []
        for point_set in point_sets:
            new_set.append(point_set)
    def draw_line(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        dy = y1 - y0
        dx = x1 - x0
        #print(dy, dx)
        if(abs(dy)>abs(dx)):
            if(dy<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            l = self.__line_drawingV(x0, y0, x1, y1, thickness, color)
        else:
            #print("H")
            if(dx<0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            l = self.__line_drawingH(x0, y0, x1, y1, thickness, color)
        return l
    def draw_arc(self, point_set, radius, arc_angle = 360, angle_offset = 0, draw_center = False, thickness = 0, color = (255,255,255)):
        for i in range(len(point_set)):
            cx,cy = point_set[i][0], point_set[i][1]
            if(draw_center):
                #print("centerdrawn")
                self.plot_pixel(cx, cy)
            x = radius
            y = 0
            xp = x*math.cos(math.radians(arc_angle+angle_offset)) - y*math.sin(math.radians(arc_angle+angle_offset))
            yp = x*math.sin(math.radians(arc_angle+angle_offset)) + y*math.cos(math.radians(arc_angle+angle_offset))
            pixel_set = []
            p = 5 - 4*radius
            while y >= -x:
                #print("working")
                pixel_set.append([x, y])
                if p > 0:
                    x -= 1
                    p += 4*(-2*(x+y)+1)
                    #print("shifted")
                else:
                    p += 4*(-2*y+1)
                y -= 1
            for i in range(len(pixel_set)-1, -1, -1):
                #print("iter", i)
                temp = [-pixel_set[i][1], -pixel_set[i][0]]
                pixel_set.append(temp)
            l = len(pixel_set)
            mirror_count=math.floor((arc_angle+angle_offset)/90)
            for i in range(mirror_count):
                x = len(pixel_set)
                x_sign = (-1)**(i%2+1)
                y_sign = (-1)**(i%2)
                #print("Signs:", x_sign, y_sign, i)
                for j in range(x-1, x-l-1, -1):
                    temp = [x_sign*pixel_set[j][0], y_sign*pixel_set[j][1]]
                    pixel_set.append(temp)
            if(radius == 1):
                degrees_per_pixel = 90
                pixels_count = round((arc_angle+angle_offset)/90)
            l = len(pixel_set)
            #print("L", l)
            if(radius%2 == 1):
                overlap = math.floor((arc_angle+angle_offset)/90)
            else:
                overlap = math.floor((arc_angle+angle_offset)/45)
            degrees_per_pixel = (90*(mirror_count+1)/(l-overlap))
            pixel_count = round(arc_angle/degrees_per_pixel)
            starting_pixel = round(angle_offset/degrees_per_pixel)
            end_pos = pixel_count+overlap+starting_pixel
            #print("Starting", starting_pixel, "count", pixel_count, "overlap", overlap)
            points = []
            for i in range(starting_pixel, end_pos):
                #print("Px",pixel_set[i][0],"Py", pixel_set[i][1])
                points.append((pixel_set[i][0]+cx, pixel_set[i][1]+cy))
                self.plot_pixel(cx+pixel_set[i][0], cy+pixel_set[i][1], color=color)

            return points
        return [[]]
    def draw_arc_extended(self, point_set, radius, arc_angle = 360, angle_offset = 0, draw_center = False, draw_as_secant = False, fill = False, thickness = 0, color = (255,255,255)):
        points1, points2, s = [], [], [ ]
        for i in range(len(point_set)):

            s = []
            cx,cy = point_set[i][0], point_set[i][1]
            if fill:
                draw_as_secant = True
                draw_center = False
            points1 = self.draw_arc([point_set[i]], radius, arc_angle,angle_offset,draw_center,thickness, color)
            #print(points)
            x_middle = round((points1[0][0]+points1[round(len(points1)/2)][0])/2)
            y_middle = round((points1[0][1]+points1[round(len(points1)/2)][1])/2)
            
            #print(x_middle, y_middle)

            if draw_as_secant and arc_angle < 360:
                s1 = self.draw_line(points1[0][0], points1[0][1], cx, cy)
                s2 = self.draw_line(points1[len(points1)-1][0], points1[len(points1)-1][1], cx, cy)
                s = s1 + s2
                pass
            if fill:
                if arc_angle > 180:
                    t = fill_algorithm(self, [x_middle, y_middle])
                    points2 = t[1]
                    for point in points2:
                        self.plot_pixel(point[0], point[1])
                else: 
                    for point in s:
                        for edge_point in points1:
                            self.draw_line(point[0], point[1], edge_point[0], edge_point[1])
        return points1 + s, points2

        
    def draw_poly(self,point_set: list, thickness = 0, color = (255,255,255)):
        lines_l = []
        l = len(point_set)
        if(l<3):
            raise ValueError("Requires at least 3 points")
        for i in range(l):
            s = self.draw_line(point_set[i][0], point_set[i][1],point_set[(i+1)%l][0], point_set[(i+1)%l][1],thickness, color)
            lines_l.append(s)
        
        return lines_l
    def draw_rectangle_1p(self, point_set: list, width, height, angle_offset = 0, thickness = 0, color=(255,255,255)):
        """
            Takes one point at a time from point_set as a reference for the top left corner. 
            angle_offset takes in a degrees input and rotates it that many degrees around the reference point.
        """
        
    def draw_rectangle_2p(self, point_set: list, width_to_height = 1.0, fill = False, thickness = 0, color = (255,255,255)):
        """
        Takes in two points at a time from the point set, corresponding to top left and bottom right, respectively. It then takes a float for the ratio of the width to height to calculate the other set of corners. 
        Note: width to height ratio will not always be exact when drawn due to pixel display inaccuracies 
        """
        points1, points2 = [()], [()]
        for i in range(0,len(point_set),2):
            x1,y1,x3,y3 = point_set[i][0], point_set[i][1], point_set[i+1][0], point_set[i+1][1]
            if (x1>x3):
                x1, x3 = x3, x1
                y1, y3 = y3, y1
            if(x3-x1 == 0):
                delta_angle = math.pi/2
            else:
                delta_angle = math.atan((y3-y1)/(x3-x1))
            #print("angle:", delta_angle)
            z = math.sqrt((x3-x1)**2 + (y3-y1)**2)
            h = math.sqrt(z/(width_to_height**2+1))
            w = width_to_height*h
            #print("h:", h, "w:", w)
            m = z*h**2/(h**2+w**2)
            x2, y2 = -m, -width_to_height*m
            x2p, y2p = round(x2*math.cos(delta_angle) - y2*math.sin(delta_angle)+x3), round(x2*math.sin(delta_angle) + y2*math.cos(delta_angle)+y3)
            #print(x2, y2, x2p, y2p)
            x4, y4 = -(z-m), width_to_height*m
            x4p, y4p = round(x4*math.cos(delta_angle) - y4*math.sin(delta_angle)+x3), round(x4*math.sin(delta_angle) + y4*math.cos(delta_angle)+y3)
            set = self.create_point_set(x1,y1,x2p,y2p,x3,y3,x4p,y4p)
            lines = self.draw_poly(set)
            points1 = []
            for line in lines:
                for point in line:
                    points1.append(point)
            if fill:
                leftmost = min(x1, x4p, x3, x2p)
                rightmost = max(x1, x4p,x3, x2p)
                topmost = min(y1, y2p,y3,y4p)
                bottommost = max(y1, y2p, y3, y4p)
                middle_point = [round((leftmost+rightmost)/2), round((topmost+bottommost)/2)]
                t = fill_algorithm(self, middle_point)
                points2 = t[1]
                for point in points2:
                    self.plot_pixel(point[0], point[1])
            
        return points1, points2
            
                    

    def erase(self):
        self._canvas[:,:,:] = 0

    def fill(self, draw_rectangle_2p):
        pass
    def __line_drawingH(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        line = []
        dx = x1-x0
        dy = y1-y0
        dir = -1 if dy < 0 else 1
        dy = dy*dir
        y = y0
        p = 2*dy - dx
        for i in range(abs(dx)+1):
            line.append((x0+i, y))
            self.plot_pixel(x0+i, y)
            if p > 0:
                y += dir
                p = p-2*dx
            p = p+2*dy
        return line
    def __line_drawingV(self, x0, y0, x1, y1, thickness = 0, color=(255,255,255)):
        line = []
        dx = x1-x0
        #print("x0", x0)
        dy = y1-y0
        dir = -1 if dx < 0 else 1
        dx = dx*dir
        x = x0
        p = 2*dx - dy
        for i in range(abs(dy)+1):
            line.append((x, y0+i))
            self.plot_pixel(x, y0+i)
            if p > 0:
                x += dir
                #print(x)
                p = p-2*dy
            p = p+2*dx
        return line
    def plot_point_set(self, point_set, color = (255,255,255)):
        for i in range(len(point_set)):
            self.plot_pixel(point_set[i][0],point_set[i][1], color)
    def plot_pixel(self, x, y, color = (255,255,255)):
        #print(x, y)
        good = True
        if(x >= self.width or x < 0):
            good = False
        if(y >= self.height or y < 0):
            good = False
        if(good):
            self._canvas[y,x] = color
    def multipoint_plot(self, point_set, offset: tuple = (0,0), color = (255,255,255)):
        for point in point_set:
            #print("points from multipoint", point[0]+offset[0], point[1]+offset[1])
            self.plot_pixel(point[0]+offset[0], point[1]+offset[1], color)
    def plot_point(self, x, y, color = (255,255,255)):
        pixels_x = round(x * self.ptp)
        pixels_x_end = pixels_x + self.ptp
        pixels_y = round(y * self.ptp)
        pixels_y_end = pixels_y+self.ptp
        for i in range(pixels_y+1, pixels_y_end+1):
            for j in range(pixels_x+1,pixels_x_end):
                self.plot_pixel(j,i, color)
    def render(self):
        print("opening")
        plt.imshow(self._canvas)
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
class PointNode:
    def __init__(self) -> None:
        self.parent_x = 0
        self.parent_y = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

D = 10
D2 = 14
def calc_H(x,y, dest):
    dx = abs(dest[0]-x)
    dy = abs(dest[1]-y)
    H = D*(dx+dy)+(D2-2*D)*min(dx,dy)
    return H
def is_valid(canvas: Canvas,x,y):
    #print("x",x)
    #print("y",y)
    #print(canvas.point_width, canvas.point_height)
    #print((x >= 0), (x < canvas.point_width), (y >= 0), (y < canvas.point_height))
    return (x >= 0) and (x < canvas.point_width) and (y >= 0) and (y < canvas.point_height)
def is_unblocked(canvas: Canvas, x,y):
    result = (canvas._canvas[y][x] == 0).all()
    #print("result", result)
    return result

def is_destination(x,y,dest):
     return y == dest[1] and x == dest[0]
def trace_path(node_details: list, dest):
    path = []
    x = dest[0]
    y = dest[1]

    while not(node_details[y][x].parent_x == x and node_details[y][x].parent_y == y):
         path.append((x,y))
         temp_x = node_details[y][x].parent_x
         temp_y = node_details[y][x].parent_y
         x = temp_x
         y = temp_y
    
    path.append((x,y))
    path.reverse()
    
    return path
def fill_algorithm(canvas: Canvas, src):
    if not is_valid(canvas, src[0], src[1]):
        #print("Failed")
        return (False, [])
    if not is_unblocked(canvas, src[0], src[1]):
        #print("Source or the destination is blocked")
        return (False, [])

    
    closed_list = [[False for _ in range(canvas.point_width)] for _ in range(canvas.point_height)]
    node_details = [[PointNode() for _ in range(canvas.point_width)]for _ in range(canvas.point_height)]
    #print(len(closed_list), len(node_details))
    x = src[0]
    y = src[1]
    node_details[y][x].f = 0.0
    node_details[y][x].g = 0
    node_details[y][x].h = 0
    node_details[y][x].parent_x = x
    node_details[y][x].parent_y = y

    open_list = []
    heapq.heappush(open_list, (0.0,x,y))
    #print("openlen", len(open_list))
    found_path = False
    path = []
    while len(open_list) > 0:
        p = heapq.heappop(open_list)
        #print("p:", p)
        x = p[1]
        y = p[2]
        coord = (x, y)
        path.append(coord)
        closed_list[y][x] = True
        #print("Appended:", path)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]

            if(is_valid(canvas,new_x,new_y) and is_unblocked(canvas, new_x, new_y) and not closed_list[new_y][new_x]):
                    #print("Calc")
                    g_new = node_details[y][x].g + D
                    h_new = 0
                    f_new = g_new+h_new

                    if node_details[new_y][new_x].f > f_new:
                        #print("Push")
                        heapq.heappush(open_list, (f_new,new_x,new_y))
                        node_details[new_y][new_x].f = f_new
                        node_details[new_y][new_x].g = g_new
                        node_details[new_y][new_x].h = h_new
                        node_details[new_y][new_x].parent_x = x
                        node_details[new_y][new_x].parent_y = y
    return(found_path, path)


def main():

    canvas = Canvas(80, 80, 3, 1)
    #print(canvas._canvas)
    #canvas.draw_line(30,30, 40, 45)
    p1 = canvas.create_point_set(13, 45, 47, 32, 11, 20, 72, 37)
    #print("Length",len(p1))
    #canvas.draw_poly(p1)
    s1 = canvas.draw_arc_extended([[50,35]], 20, 270 , 45, draw_center= False, draw_as_secant= True, fill= False)
    s2 = canvas.draw_rectangle_2p([[20,20], [40,20]], 1/2, True)
    l = [0,0]
    l2 = [1,1]
    l3 = l + l2
    print(l3)
    #print(s1, s2)
    
    #canvas.plot_point_set(s1)
    #s = pathfinding.fill_algorithm(canvas, [0,0])
    #points = s[1]
    #print(points)
    #for point in points:
     #   canvas.plot_pixel(point[0], point[1])
    canvas.render()




if __name__ == "__main__":
        main()


    
  
