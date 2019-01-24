import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, acos

def angle(ux, vx, uy, vy):
    eq = sqrt((ux*vx+uy*vy)**2/((ux**2+uy**2)*(vx**2+vy**2)))
    eq = acos(eq)
    return eq

def xdetect(line1, line2):
    # line1: a0 a1
    # line2: b0, b1
    # line1 is: ((xa0,ya0), (xa1, ya1))
    # return True if there is a crossing

    xa0 = line1[0][0]
    ya0 = line1[0][1]
    xa1 = line1[1][0]
    ya1 = line1[1][1]

    xb0 = line2[0][0]
    yb0 = line2[0][1]
    xb1 = line2[1][0]
    yb1 = line2[1][1]


    s1 = (xb0 - xa0) * (yb1 - ya0) - (xb1 - xa0) * (yb0 - ya0)
    s2 = (xb0 - xa1) * (yb1 - ya1) - (xb1 - xa1) * (yb0 - ya1)
    if s1*s2 > 0:
        return False
    s3 = (xa1 - xb0) * (ya0 - yb0) - (xa0 - xb0) * (ya1 - yb0)
    s4 = s2 - s1 + s3
    if s3*s4 > 0:
        return False
    return True


def plot(line, linetype = '-', colour='k', lw = 1):
    # line1 is: ((xa0,ya0), (xa1, ya1))
    # plot needs: (xa0, xa1), (ya0, ya1)
    xa0 = line[0][0]
    ya0 = line[0][1]
    xa1 = line[1][0]
    ya1 = line[1][1]
    obj, = plt.plot((xa0, xa1), (ya0, ya1), linetype, color=colour, linewidth = lw)
    return obj