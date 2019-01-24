import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, acos
import time

from tools import *

t = 1

def init(v, e):
    plt.scatter(v[0][0], v[0][1], color='k')
    plt.plot((v[0][0], v[7][0]+0.5), (v[0][1], v[0][1]), '--', color='k')
    lines = []
    for i in v[1:9]:
        plt.scatter(i[0], i[1], color='g')
        l, = plt.plot((v[0][0], i[0]), (v[0][1], i[1]), '-.')  # color='k'
        lines.append(l)

    for i in [1, 2, 3, 5, 6, 7]:
        if i % 2 == 1:
            s = 11
        else:
            s = 12.5
        # quiver: origin_x, origin_y, vector_x, vector_y
        plt.quiver(v[i][0], v[i][1], v[i + 1][0] - v[i][0], v[i + 1][1] - v[i][1], scale=s, width = 0.004)

    plt.quiver(v[1][0], v[1][1], v[4][0] - v[1][0], v[4][1] - v[1][1], scale=12.5, width = 0.004)
    plt.quiver(v[5][0], v[5][1], v[8][0] - v[5][0], v[8][1] - v[5][1], scale=12.5, width = 0.004)

    plt.text(v[0][0], v[0][1]+0.3, 'v', fontsize = 14)
    for i in range(1, len(v)):
        if i in [2, 3, 6, 7]:
            x_offset = +0
        else:
            x_offset = -0.4
        if v[i][1] > v[0][1]:
            y_offset = +0.1
        else:
            y_offset = -0.3
        plt.text(v[i][0] + x_offset, v[i][1] + y_offset, 'v' + str(i), fontsize=14)

    for i in range(1, len(e)):
        if i in [4, 8]:
            x = e[i][0][0] +0.1
            y = (e[i][0][1]+e[i][1][1])/2 - 0.3
        elif i in [2, 6]:
            x = e[i][0][0] -0.5
            y = (e[i][0][1]+e[i][1][1])/2 - 0.3
        elif i in [3, 7]:
            x = e[i][1][0] + 1
            y = e[i][0][1] - 0.4
        else:
            x = e[i][0][0] + 1
            y = e[i][0][1] + 0.2
        plt.text(x, y, 'E'+str(i), fontsize=14)

    return lines

if __name__=='__main__':
    plt.figure(figsize=(8, 6))

    # parameters are measured from the book:

    v = ((0, 5),\
         (3.5, 5-3.5), (6.5, 5-3.5), (6.5, 5+1.9), (3.5, 5+1.9),\
         (7.1, 5-4.2), (9.7, 5-4.2), (9.7, 5+4.2), (7.1, 5+4.2))

    # E0 is the vertical line
    # E1 ~ E8
    e = [((v[0]), (v[7][0] + 0.5, v[0][1]))]
    for i in range(1, len(v)):
        if i == 4:
            e_line = (v[1], v[i])
        elif i == 8:
            e_line = (v[5], v[i])
        else:
            e_line = (v[i], v[i + 1])
        e.append(e_line)

    text = plt.text(-1, -0.5, 'Get all alpha value', fontsize=20)

    alpha_lines = init(v, e)

    plt.pause(10)

    # create all alpha
    alpha = []
    epsilon = []
    for i in range(1, len(v)):
        ux = 10; uy = 0 # horizontal line
        vx = v[i][0] - v[0][0]; vy = v[i][1] - v[0][1]
        alpha = angle(ux, vx, uy, vy)
        if v[i][1] < v[0][1]:
            alpha = 2*np.pi-alpha
        alpha = alpha*180/np.pi
        epsilon.append((i, alpha))

    # create vertex list epsilon, alpha sorted in order
    epsilon.sort(key=lambda x: (x[1]))
    print epsilon

    # create active list s
    s = []
    for i in range(1, len(e)):
        if xdetect(e[0], e[i]):
            s.append(i)

    print s

    # highlight what is in s
    objs = []
    for i in s:
        if e[i][1][0]-e[i][0][0] == 0:
            scale = 12.5
        else:
            scale = 11
        obj = plt.quiver(e[i][0][0], e[i][0][1], e[i][1][0]-e[i][0][0], e[i][1][1]-e[i][0][1], scale = scale, color = 'r')
        objs.append(obj)

    text.set_text('initial S: ' + str(s))

    i = 0
    plt.draw()
    plt.pause(t)
    [i.remove() for i in objs]
    plt.draw()
    plt.pause(t)

    visG = []
    # for all \alpha_i do loop starts here
    testLine = []
    for k in s:
        testLine.append(plot(e[k], '-', colour='b', lw=3))
    plt.draw(); plt.pause(t)
    for j in epsilon:
        i = j[0]
        targetPt = plt.scatter(v[i][0], v[i][1], color='k', linewidth=10)
        text.set_text('S=' + str(s))
        plt.draw()
        plt.pause(t)

        targetLine = plot((v[0], v[i]), '-', colour='g', lw=3)

        # debugging start point
        plt.draw(); plt.pause(t)

        # check if vi is visible to v:
        line = (v[0], v[i])
        visible = True
        for k in s:
            if v[i] in e[k]:
                continue
            if xdetect(line, e[k]) == True:
                visible = False

                #drawing then break
                obj = plot(e[k], colour='r', lw = 3)
                targetLine.remove()
                targetLine = plot((v[0], v[i]), '-', colour='r', lw=3)
                text.set_text('S=' + str(s) + '; v' + str(i) + ' is NOT visible')
                plt.draw(); plt.pause(t*2)
                obj.remove()
                print 'remove ' + str(i)
                alpha_lines[i-1].set_alpha(0)
                break
            else:
                #drawing then break
                obj = plot(e[k], colour='g', lw = 3)
                plt.draw();plt.pause(t)
                obj.remove()

        if visible == True:
            plot((v[0], v[i]), '-', colour='k', lw=1)
            print 'visible:' + str(i) + ', ',
            visG.append(i)
            text.set_text('S=' + str(s) + '; v' + str(i) + ' is visible')

        targetLine.remove()
        plt.draw(); plt.pause(t)

        # if v_i is the beginning of an edge, add this edge:
        for k in range(1, len(e)):
            if v[i] == e[k][0]:
                if not(k in s):
                    s.append(k)
                    print 'add ' + str(k) + ', ',

                    #draw
                    text.set_text('S=' + str(s) + ' add E' + str(k) + ' -> ' + str(s))
                    obj = plot(e[k], linetype='--', colour='g', lw=5)
                    plt.draw()
                    plt.pause(t)
                    obj.remove()

        # if v_i is the end of an edge, del this edge:
        for k in range(1, len(e)):
            if v[i] == e[k][1]:
                s.remove(k)
                print 'remove ' + str(k) + ',',

                # draw
                text.set_text('S=' + str(s) + ' del E' + str(k) + ' -> ' + str(s))
                obj = plot(e[k], linetype='--', colour='r', lw=5)
                plt.draw()
                plt.pause(t)
                obj.remove()

        text.set_text('S=' + str(s))
        print 'S for now: ' + str(s)
        plt.draw()
        plt.pause(t)
        if len(s) < 4:
            plt.pause(t*(3-len(s)))
        targetPt.remove()
        [m.remove() for m in testLine]
        testLine = []
        for k in s:
            testLine.append(plot(e[k], '-', colour='b', lw=3))
        plt.draw()
        plt.pause(t)

    [m.remove() for m in testLine]
    plt.draw()
    plt.pause(t)
    print visG
    plt.show()