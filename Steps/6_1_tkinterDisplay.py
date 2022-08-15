import tkinter as tk
import HelperFunction as h
import time
import math
import numpy as np


# Load in and filt the angle
index, VP_x, VP_y, angle = h.GetFile('TonyRoad_Record.txt')
angle = np.array(angle)
for i in range(len(angle)):
    ang = angle[i]
    if(abs(ang)>0.7):
        angle[i] = 0
    elif(abs(ang)<0.01):
        angle[i] = 0
    elif(np.isnan(ang) == True):
        angle[i] = 0
angle = angle * -1

# angle = [0 for i in range(100)]
# angle = angle + [math.pi/80 for i in range(40)]
# angle = angle + [0 for i in range(100)]
# angle = np.array(angle)


# Find the turning point
# If last 10 are zeros and next 10 bigger than the threshold, then it's the turning point.
turning_point_all = []
threshold = 0.03
for i in range(10, len(angle)):
    if(angle[i-10:i].sum() == 0 and abs(angle[i:i+10].mean()) >= threshold):
        turning_point_all.append(i)
    # print(f"{i}, {angle[i-10:i].sum()}, {angle[i:i+10].mean()}")
for i in range(1, len(turning_point_all)):
    if(turning_point_all[i] == turning_point_all[i-1]+1):
        turning_point_all[i-1] = 0
turning_point = []
for point in turning_point_all:
    if(point != 0):
        turning_point.append(point)

# The 30 angle before turning point, add the missed angle
# which cannot be found from VP
for point in turning_point:
    angle[point-20:point] = np.pi/180*40 / 30 * np.sign(angle[point+5])





window = tk.Tk()
window.title('Moving Route')
window.resizable(False,False)
window_width = 600
window_height = 650
initial_x = 50
initial_y = 50
window.geometry(f'{window_width}x{window_height}+{initial_x}+{initial_y}')


canvas = tk.Canvas(window, width=window_width, height=window_height)
canvas.place(x=0, y=0)


step = 1
current_x = window_width/3
current_y = window_height*5/6
left_road_x, left_road_y = current_x - 20, current_y
right_road_x, right_road_y = current_x + 20, current_y
current_ang = 0


for i, ang in enumerate(angle):
    # print(f"{i}, {current_ang:.5f}, {-ang:.5f}")
    # print(i)

    # Update current angle and calculate moving vector
    current_ang += ang
    u = step * math.sin(current_ang)
    v = step * math.cos(current_ang)


    mag = (u**2 + v**2) ** 0.5
    scale = 15 / mag
    vec1 = [-v * scale, u * scale]
    vec2 = [v * scale, -u * scale]


    # Draw every frame results on canvas
    # h.create_line(canvas, current_x, current_y, current_x + u, current_y - v)
    if(i % 10 == 0):
        h.create_circle(canvas, current_x, current_y)
    
    h.create_circle(canvas, current_x + vec1[0], current_y - vec1[1], radius=1, fill='black')
    h.create_circle(canvas, current_x + vec2[0], current_y - vec2[1], radius=1, fill='black')

    
    # Update current locations
    current_x += u
    current_y -= v
  

    time.sleep(0.001)
    canvas.update()



# h.create_line(canvas, 100, 100, 200, 200)





window.mainloop()