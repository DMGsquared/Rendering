import numpy as np
import matplotlib.pyplot as plt
import math
import drawHelper as dh
import random

def checker():
    #for i in range(h)
    pass
def randomizer(canvas: dh.Canvas,
    object_size = 1, 
    choices: list = [1,2,3,4,5], 
    weights = [0.1,0.2,0.3,0.2,0.1],
    ratio_rangeA = 0.1,
    ratio_rangeB = 1.0,
    circle_size_rangeA = 1/12, 
    circle_size_rangeB = 1/6,
    margin_start_widthC = 1/9,
    margin_end_widthC = 8/9,
    margin_start_heightC = 1/9,
    margin_end_heightC = 8/9,
    margin_start_widthR = 1/9,
    margin_end_widthR = 5/9,
    margin_start_heightR = 1/9,
    margin_end_heightR = 5/9,
    add_rangeAW = 1/12, 
    add_rangeBW = 1/3, 
    add_rangeAH = 1/12, 
    add_rangeBH = 1/3):
    #canvas_collection = []

    w = canvas.point_width
    h = canvas.point_height
    has_intersection = False
    dummy_canvas = dh.Canvas(w, h)
    choice = random.choices(choices,weights)[0]
    #print(choice)
    pointsM1 = []
    pointsM2 = []
    for i in range(choice):
        points1 = []
        points2 = []
        chooser = random.randint(1,2)
        if(chooser==1):
            p1 = [random.randint(round(w*margin_start_widthR),round(w*margin_end_widthR)),random.randint(round(h*margin_start_heightR),round(h*margin_end_heightR))]
            p2 = [round(p1[0]+random.random()*(add_rangeBW*w-add_rangeAW*w)+add_rangeAW*w), round((p1[1]+random.random()*(add_rangeBH*h - add_rangeAH*h)+add_rangeAH*h))]
            s1 = dummy_canvas.create_point_set(p1[0], p1[1], p2[0], p2[1])
            ratio = random.random()*(ratio_rangeB-ratio_rangeA)+ratio_rangeA
            #print(ratio)
            points1 = dummy_canvas.draw_rectangle_2p(s1,ratio**(-1**random.randint(1,2)), fill=True)
            for point in points1:
                dummy_canvas.erase()
                temp = dummy_canvas.draw_arc_extended([point], object_size, fill=True, color=(255,0,255))
                points2 = points2 + temp
        else:
            points1 = dummy_canvas.draw_arc_extended([[random.randint(round(w*margin_start_widthC),round(w*margin_end_widthC)),random.randint(round(h*margin_start_heightC),round(h*margin_end_heightC))]], 
            random.randint(round(h*circle_size_rangeA), round(h*circle_size_rangeB)), fill=True, color=(225,225,225))
            for point in points1:
                dummy_canvas.erase()
                temp = dummy_canvas.draw_arc_extended([point], object_size, fill=True, color=(255,0,255))
                points2 = points2 + temp
        dummy_canvas.erase()
        #print("points2", points2)
        for point in points1:
            if point in pointsM1:
                has_intersection = True
        pointsM1 = pointsM1 + points1
        pointsM2 = pointsM2 + points2
    return pointsM1, pointsM2, has_intersection


    
def collector(canvas: dh.Canvas,
    epochs, 
    object_size = 1,
    choices = [1,2,3,4,5], 
    weights = [0.1,0.2,0.3,0.2,0.1],
    ratio_rangeA = 0.1,
    ratio_rangeB = 1.0,
    circle_size_rangeA = 1/12, 
    circle_size_rangeB = 1/6,
    margin_start_widthC = 1/9,
    margin_end_widthC = 8/9,
    margin_start_heightC = 1/9,
    margin_end_heightC = 8/9,
    margin_start_widthR = 1/9,
    margin_end_widthR = 5/9,
    margin_start_heightR = 1/9,
    margin_end_heightR = 5/9,
    add_rangeAW = 1/12, 
    add_rangeBW = 1/3, 
    add_rangeAH = 1/12, 
    add_rangeBH = 1/3):
    w = canvas.point_width
    h = canvas.point_height
    canvas_collection = np.zeros((epochs,h,w,3))
    for epoch in range(epochs):
        points, pathfinding_guide_points, has_intersection = randomizer(canvas, 
        object_size,
        choices, 
        weights,
        ratio_rangeA,
        ratio_rangeB,
        circle_size_rangeA, 
        circle_size_rangeB,
        margin_start_widthC,
        margin_end_widthC,
        margin_start_heightC,
        margin_end_heightC,
        margin_start_widthR,
        margin_end_widthR,
        margin_start_heightR,
        margin_end_heightR,
        add_rangeAW, 
        add_rangeBW, 
        add_rangeAH, 
        add_rangeBH)
        #canvas_collection.append(canvas._canvas)
        for point in points:
            canvas.plot_pixel(point[0], point[1])
        for point in pathfinding_guide_points:
            canvas.plot_pixel(point[0], point[1], color= (255,0,255))
        if not has_intersection:
            canvas_collection[epoch-1] =  canvas._canvas
        #canvas.render()
        canvas.erase()
    return canvas_collection
    

def main():
    random.seed(3213)
    w, h, r = 128, 72,1
    canvas = dh.Canvas(w,h,3)
    r_rangeA = .1
    r_rangeB = 1
    add_rangeAW = 1/12
    add_rangeBW = 5/12
    add_rangeAH = 1/12
    add_rangeBH = 1/3
    epochs = 100
    #canvas_collection = np.zeros((epochs,h,w,3))
    choices = [1,2,3,4,5]
    weights = [.1, .2, .3,.2,.1]
    choice_dis = [0,0,0,0,0]
    workcount = 0
    collection = collector(canvas, epochs)
    canvas_collection = np.array(collection)
    '''for i in range(w):
            path = 0
            for j in range(h, h-5):
                count = 0
                for n in range(5):
                    if(canvas._canvas[j+n,i] == (0,0,0)):
                        count += 1
                if(count == 5):
                    path += 1 
        if(path == w):
            canvas_collection[epoch] = canvas._canvas
            workcount += 1
            choice_dis[choice-1] += 1
        print("epoch", epoch) '''

    #print("worked", workcount)
    print(len(canvas_collection))
    random.seed(None)
    subplot_rows, subplot_columns = 5,5
    fig, axs = plt.subplots(subplot_rows, subplot_columns)
    for i in range(subplot_rows):
        for j in range(subplot_columns):
            axs[i][j].imshow(np.uint8(canvas_collection[random.randint(0, len(canvas_collection)-1)]))
    
    #fig.add_subplot(4,3,3)
    #plt.bar(choices,choice_dis)
    plt.show()


if __name__ == "__main__":
    main()