# -*- coding: utf-8 -*-
"""
   程序名称：渗流程序
   程序功能：根据渗流模型计算区域是否连通
   程序作者：何冰
   建立日期：2017年5月13日
"""

from pylab import *
from scipy.ndimage import measurements

# import statsmodels.api as sm
import numpy as np
from random import random
from numba import jit
from datetime import datetime

"""
   
"""


def CreateRegion(regionsize, templatecell):
    rownum = templatecell.shape[0] * regionsize[0]
    colnum = templatecell.shape[1] * regionsize[1]
    region = np.zeros((rownum, colnum))
    tsize = templatecell.shape
    for i in range(regionsize[0]):
        for j in range(regionsize[1]):
            startrow = i * tsize[0]
            endrow = startrow + tsize[0]
            startcol = j * tsize[1]
            endcol = startcol + tsize[1]
            region[startrow:endrow, startcol:endcol] = templatecell
    return region


def InitRegionRandomData(region, regionsize, templatecell):
    tsize = templatecell.shape
    for i in range(regionsize[0]):
        for j in range(regionsize[1]):
            startrow = i * tsize[0]
            startcol = j * tsize[1]
            region[startrow + 1, startcol + 3] = random()
            region[startrow + 3, startcol + 1] = random()
        # randomnumber=np.random.rand(2,1)
        # region[startrow+1,startcol+3]=randomnumber[0,0]
        # region[startrow+3,startcol+1]=randomnumber[1,0]


def CreateRegion3D(regionsize, templatecell):
    totalsize = templatecell.shape * regionsize
    region = np.zeros(totalsize)
    tsize = templatecell.shape
    for i in range(regionsize[0]):
        for j in range(regionsize[1]):
            for k in range(regionsize[2]):
                start = np.array([i, j, k]) * tsize
                end = start + tsize
                region[start[0] : end[0], start[1] : end[1], start[2] : end[2]] = (
                    templatecell
                )
    return region


def InitRegionRandomData3D(region, regionsize, templatecell):
    pass


def CaluRegionConnectivity(region, randnumber, debug=False):
    regionIsConnect = region < randnumber
    lw, num = measurements.label(regionIsConnect)
    sliced = measurements.find_objects(lw)
    if num > 0:
        for slic in sliced:
            for i in range(len(slic)):
                if (slic[i].start == 0) and slic[i].stop == region.shape[i]:
                    return [True, i]
    return [False, 0]


if __name__ == "__main__":
    start = datetime.now()
    templategrid = np.array(
        [
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ]
    )
    rsize = [10, 10]
    NumberOfStep = 20
    xlist = [i * 0.01 + 0.2 for i in range(NumberOfStep)]
    ylist = [0.0 for i in range(NumberOfStep)]
    # region=CreateRegion(rsize,templategrid)
    tmpregion = np.fromfile("occupyrate.dat", dtype=np.double, sep="")
    arrayregion = tmpregion.reshape(100, 1, 20, 20)
    for num in range(100):
        seed()
        region = arrayregion[num]
        for i in range(NumberOfStep):
            ran = xlist[i]
            # InitRegionRandomData(region,rsize,templategrid)
            [con, contype] = CaluRegionConnectivity(region, ran, False)
            if con == True:
                ylist[i] = ylist[i] + 1
        if num // 200 == 0:
            print(num)

    y = [data / 200.0 for data in ylist]
    stop = datetime.now()
    print(stop - start)
    plt.plot(xlist, y, color="red")
    plt.show()
    plt.savefig("result.png")
    print(xlist)
    print(ylist)
    print(y)
    for index, x in enumerate(xlist):
        print(" {0}  {1}".format(xlist[index], y[index]))
