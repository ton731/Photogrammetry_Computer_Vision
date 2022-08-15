import numpy as np
import matplotlib.pyplot as plt

f = open('TonyRoadBig_Record.txt', 'r')
index = []
VP_x = []
VP_y = []
angle = []

for line in f.readlines():
    line = line.split(',')
    index.append(int(line[0]))
    VP_x.append(float(line[1]))
    VP_y.append(float(line[2]))
    angle.append(float(line[3].split('\n')[0]))


plt.plot(index, angle)




for i in range(len(angle)):
    ang = angle[i]
    if(abs(ang)>0.7):
        angle[i] = 0
    elif(abs(ang)<0.02):
        angle[i] = 0
    elif(np.isnan(ang) == True):
        angle[i] = 0
angle = np.array(angle)
angle = angle * -1

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
# for point in turning_point:
#     angle[point-30:point] = np.pi/4 / 30 * np.sign(angle[point+5])


# plt.plot(index, VP_x)
# plt.plot(index, VP_y)
# plt.plot(index, angle)
plt.show()