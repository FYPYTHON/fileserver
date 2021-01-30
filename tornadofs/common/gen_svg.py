#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 13:45
# @Author  : 1823218990@qq.com
# @File    : gen_svg.py
# @Software: PyCharm
"""
all color: {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}
           {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',
            'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}

---

"""
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

maxX = 50
maxY = 50
fig = plt.figure()
ax = fig.add_subplot(111)
def storeage():
    # plt.axis('off')
    x, y = rect()
    plt.plot(x, y, 'g--')
    ellipse()
    # plt.axis('scaled')
    plt.axis('equal')
    plt.show()
    pass

def rect():
    x = [15, 35, 35, 15, 15]
    y = [15, 15, 35, 35, 15]
    return x, y

def ellipse():
    """
     edgecolor=None,
     facecolor=None,
     color=None,
     linewidth=None,
     linestyle=None,
     antialiased=None,
     hatch=None,
     fill=True,
     capstyle=None,
     joinstyle=None,
    :return:
    """
    fillcolor = 'purple'
    fillcolor2 = 'yellow'
    f2 = Ellipse(xy=(25.0, 31.0), width=20, height=6, angle=0.0, facecolor=fillcolor, alpha=0.3, edgecolor='black')
    f1 = Ellipse(xy=(25.0, 28.0), width=20, height=6, angle=0.0, facecolor=fillcolor2, alpha=0.3)
    el = Ellipse(xy=(25.0, 25.0), width=20, height=6, angle=0.0, facecolor=fillcolor, alpha=0.3, edgecolor='black')
    e2 = Ellipse(xy=(25.0, 22.0), width=20, height=6, angle=0.0, facecolor=fillcolor2, alpha=0.3)
    e3 = Ellipse(xy=(25.0, 19.0), width=20, height=6, angle=0.0, facecolor=fillcolor, alpha=0.3, edgecolor='black')
    ax.add_patch(el)
    ax.add_patch(e2)
    ax.add_patch(e3)
    ax.add_patch(f1)
    ax.add_patch(f2)


if __name__ == '__main__':
    storeage()