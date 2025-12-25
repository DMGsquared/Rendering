import numpy as np
import matplotlib.pyplot as plt
import math
import drawHelper as dh

def main():
    canvas = dh.Canvas(80, 80, 3)
    canvas.draw_line(30, 30, 45, 40)
    canvas.render()


if __name__ == "__main__":
    main()