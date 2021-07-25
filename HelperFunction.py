import numpy as np

def CheckIfGoodLine(x1, y1, x2, y2, height, width):
    if(x1 == x2):return False
    slope = abs((y2-y1)/(x2-x1))

    # Remove near horizontal lines
    if(slope<0.2):return False

    # Remove near vertical lines
    if(slope>10):return False

    # Remove top half lines
    if(y1<height*2/5 and y2<height*2/5):return False
    if(y1<height/4 or y2<height/4):return False

    # Remove very left and right vertical lines
    if(x1<width/4 and x2<width/4 and slope>5):return False
    if(x1>width*3/4 and x2>width*3/4 and slope>5):return False

    # If line is in the left area, the slope should be negative
    if(x1<width/2 and x2<width/2 and ((y2-y1)/(x2-x1))>0):return False
    if(x1>width/2 and x2>width/2 and ((y2-y1)/(x2-x1))<0):return False

    # the two end of line should be in the same side (left or right)
    if(x1<width/2 and x2>width/2):return False
    if(x1>width/2 and x2<width/2):return False

    return True

def GetAngleBetween2Vectors(last_vector, current_vector):
    unit_last_vector = last_vector / np.linalg.norm(last_vector)
    unit_current_vector = current_vector / np.linalg.norm(current_vector)
    dot_product = np.dot(unit_last_vector, unit_current_vector)
    angle = np.arccos(dot_product)
    # Assume turn right will get positive angle
    return angle if unit_current_vector[0]>unit_last_vector[0] else -angle

def GetFile(filename):
    f = open(filename, 'r')
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

    return index, VP_x, VP_y, angle


# Create line
def create_line(canvas, x0, y0, x1, y1, width=2):
    return canvas.create_line(x0, y0, x1, y1, fill='black', width=width)

# Create circle
def create_circle(canvas, x, y, radius=3, fill='red', **kwargs):
    return canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=fill, **kwargs)
