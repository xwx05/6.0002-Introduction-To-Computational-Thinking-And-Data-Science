# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag
"""

import random, pylab, numpy

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1


def rSquared(observed, predicted):
    error = ((predicted - observed) ** 2).sum()
    meanError = error / len(observed)
    return 1 - (meanError / numpy.var(observed))


def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = pylab.polyfit(xVals, yVals, d)
        models.append(model)
    return models


def TestFits(models, degrees, xVals, yVals, title):
    pylab.plot(xVals, yVals, 'o', label='Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        pylab.plot(xVals, estYVals,
                   label='Fit of degree ' \
                         + str(degrees[i]) \
                         + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc='best')
    pylab.title(title)


def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline()  #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)


def labelPlot():
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')


def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81  #acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label='Measured displacements')
    labelPlot()


def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81  #get force
    pylab.plot(xVals, yVals, 'bo',
               label='Measured points')
    model = pylab.polyfit(xVals, yVals, 1)
    xVals = xVals + [2]
    yVals = yVals + []
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'r',
               label='Linear fit, r**2 = '
                     + str(round(rSquared(yVals, estYVals), 5)))
    model = pylab.polyfit(xVals, yVals, 2)
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'g--',
               label='Quadratic fit, r**2 = '
                     + str(round(rSquared(yVals, estYVals), 5)))
    pylab.title('A Linear Spring')
    labelPlot()
    pylab.legend(loc='best')


random.seed(0)


class tempDatum(object):
    def __init__(self, s):
        info = s.split(',')
        self.high = float(info[1])
        self.year = int(info[2][0:4])

    def getHigh(self):
        return self.high

    def getYear(self):
        return self.year


def getTempData():
    inFile = open('temperatures.csv')
    data = []
    for l in inFile:
        data.append(tempDatum(l))
    return data


def getYearlyMeans(data):
    years = {}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
            # 获取年份作为键，然后获取温度添加到以该年份为键的值列表中。如果键已经存在，那么直接添加温度到值列表里。
        except:
            years[d.getYear()] = [d.getHigh()]  # 第一次读到某个年份时，创建新键
    for y in years:
        years[y] = sum(years[y]) / len(years[y])  # 计算每年最高温度的平均值
    return years


data = getTempData()
years = getYearlyMeans(data)
xVals, yVals = [], []
for e in years:
    xVals.append(e)
    yVals.append(years[e])
pylab.plot(xVals, yVals)
pylab.xlabel('Year')
pylab.ylabel('Mean Daily High (C)')
pylab.title('Select U.S. Cities')
pylab.show()


def splitData(xVals, yVals):
    toTrain = random.sample(range(len(xVals)),
                            len(xVals) // 2)  # 随机抽取一半数据加入到数据集中，剩下的作为测试集
    trainX, trainY, testX, testY = [], [], [], []
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX, trainY, testX, testY


# UNCOVER FOR SECOND DEMO
numSubsets = 10  # 进行10次试验
dimensions = (1, 2, 3, 4)
rSquares = {}
for d in dimensions:
    rSquares[d] = []

for f in range(numSubsets):
    trainX, trainY, testX, testY = splitData(xVals, yVals)
    for d in dimensions:
        model = pylab.polyfit(trainX, trainY, d)
        # estYVals = pylab.polyval(model, trainX)
        estYVals = pylab.polyval(model, testX)
        rSquares[d].append(rSquared(testY, estYVals))
print('Mean R-squares for test data')
for d in dimensions:
    mean = round(sum(rSquares[d]) / len(rSquares[d]), 4)
    sd = round(numpy.std(rSquares[d]), 4)
    print('For dimensionality', d, 'mean =', mean,
          'Std =', sd)  # dimension1 看起来是最好的拟合 mean = 0.7535 Std = 0.0656
print(rSquares[1])  # 注意到单次试验中会出现0.5709的低R2值，所以要多次试验取平均值
