import drawHelper as dh
import pynputHelper as ph
import dataGen as dg
import pathfinding as pf


canvas = dh.Canvas(128,72)
array_of_data = dg.collector(canvas, 100, object_size= 4, choices= [2,3,4,5,6])