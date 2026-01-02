import numpy as np
import matplotlib.pyplot as plt
import math
import drawHelper as dh
import random
import heapq
import dataGen as dg
D = 10
D2 = 14
class PointNode:
    def __init__(self) -> None:
        self.parent_x = 0
        self.parent_y = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0


def calc_H(x,y, dest):
    dx = abs(dest[0]-x)
    dy = abs(dest[1]-y)
    H = D*(dx+dy)+(D2-2*D)*min(dx,dy)
    #H = round(D*math.sqrt(dx**2+dy**2))
    #H = dx+dy
    return H
def is_valid(canvas:dh.Canvas,x,y):
    #print("x",x)
    #print("y",y)
    #print(canvas.point_width, canvas.point_height)
    #print((x >= 0), (x < canvas.point_width), (y >= 0), (y < canvas.point_height))
    return (x >= 0) and (x < canvas.point_width) and (y >= 0) and (y < canvas.point_height)
def is_unblocked(canvas:dh.Canvas, x,y):
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
def fill_algorithm(canvas: dh.Canvas, src):
    if not is_valid(canvas, src[0], src[1]):
        print("Failed")
        return (False, [])
    if not is_unblocked(canvas, src[0], src[1]):
        print("Source or the destination is blocked")
        return (False, [])

    
    closed_list = [[False for _ in range(canvas.point_width)] for _ in range(canvas.point_height)]
    node_details = [[PointNode() for _ in range(canvas.point_width)]for _ in range(canvas.point_height)]
    print(len(closed_list), len(node_details))
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
        print("p:", p)
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


def a_star_algorithm(canvas: dh.Canvas, src, dest):
    if not is_valid(canvas, src[0], src[1], ) or not is_valid(canvas, dest[0], dest[1]):
        print("Failed")
        return (False, [])
    if not is_unblocked(canvas, src[0], src[1]) or not is_unblocked(canvas, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return (False, [])

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return (False, [])
    
    closed_list = [[False for _ in range(canvas.point_width)] for _ in range(canvas.point_height)]
    node_details = [[PointNode() for _ in range(canvas.point_width)]for _ in range(canvas.point_height)]
    print(len(closed_list), len(node_details))
    x = src[0]
    y = src[1]
    node_details[y][x].f = 0.0
    node_details[y][x].g = 0
    node_details[y][x].h = 0
    node_details[y][x].parent_x = x
    node_details[y][x].parent_y = y

    open_list = []
    heapq.heappush(open_list, (0.0,x,y))
    print("openlen", len(open_list))
    found_path = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)
        #print("p:", p)
        path = []
        x = p[1]
        y = p[2]
        closed_list[y][x] = True
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]
            distance = D if abs(dir[0])+abs(dir[1]) == 1 else D2
            if(is_valid(canvas,new_x,new_y) and is_unblocked(canvas, new_x, new_y) and not closed_list[new_y][new_x]):
                if is_destination(new_x,new_y,dest):
                    node_details[new_y][new_x].parent_x = x
                    node_details[new_y][new_x].parent_y = y
                    
                    path = trace_path(node_details, dest)
                    found_path = True
                    return (found_path, path)
                else:
                    #print("Calc")
                    g_new = node_details[y][x].g + distance
                    h_new = calc_H(new_x,new_y,dest)
                    f_new = g_new+h_new

                    if node_details[new_y][new_x].f > f_new:
                        #print("Push")
                        heapq.heappush(open_list, (f_new,new_x,new_y))
                        node_details[new_y][new_x].f = f_new
                        node_details[new_y][new_x].g = g_new
                        node_details[new_y][new_x].h = h_new
                        node_details[new_y][new_x].parent_x = x
                        node_details[new_y][new_x].parent_y = y
    if(not found_path):
         print("No path")
    return(found_path, path)
    
    
def main():
    canvas = dh.Canvas(128,72)
    points, pathfinding_points, has_intersection = dg.randomizer(canvas, object_size= 3)
    print("Pathfinding", pathfinding_points[0])
    canvas.multipoint_plot(pathfinding_points, color = (255,0,255))
    #canvas.plot_pixel(pathfinding_points[0][0], pathfinding_points[0][1], (255,0,255))
    canvas.multipoint_plot(points)
    print("done")
    print("intersects", has_intersection)
    src, dest = [0,71], [127, 0]
    a_star_result = a_star_algorithm(canvas,src,dest)
    #print(a_star_result)
    if(a_star_result[0]):
        for point in a_star_result[1]:
               canvas.plot_pixel(point[0],point[1],(32,255,32))
        #print(a_star_result[1])
    canvas.render()
    

if __name__ == "__main__":
     main()
                             

                      
            



