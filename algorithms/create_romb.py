import numpy as np
import matplotlib.pyplot as plt
import json

def delete_point(x0,y0,arr):
    point = [x0-258,y0-258]

    while True:
        while True:
            if point in arr:
                arr.remove(point)
            point[1] += 6

            if point[1] > 250:
                break

        point[0] += 6
        point[1] = y0-258

        if point[0] > 250:
            break

def save_pattern(dx,dy,arr):
    coords = np.array([(0, -2), (-1,1), (-2, -3), (-3, -1), (-4, 0), (-5, 2)])
    coords[:, 0] -= (dx - 1)
    coords[:, 1] -= (dy - 1)

    for x,y in coords:
        delete_point(x,y,arr)

    if [0,0] in arr:
        arr.remove([0,0])

    with open("build_patterns\\"+ f"new_romb5_{dx}_{dy}.txt", 'w') as f:
        json.dump(arr,f)

dx = 2
for dy in range(1,6):
    with open("build_patterns\\romb.txt") as f:
        arr = json.load(f)
    print(dx, dy)
    save_pattern(dx, dy, arr)