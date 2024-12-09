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


def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline()  # discard header
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
    xVals = xVals * 9.81  # acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label='Measured displacements')
    labelPlot()


def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81  # get force
    pylab.plot(xVals, yVals, 'bo',
               label='Measured points')
    labelPlot()
    a, b = pylab.polyfit(xVals, yVals, 1)
    estYVals = a * pylab.array(xVals) + b
    print('a =', a, 'b =', b)
    pylab.plot(xVals, estYVals, 'r',
               label='Linear fit, k = '
                     + str(round(1 / a, 5)))
    pylab.legend(loc='best')


# fitData('springData.txt')  # 一阶线性回归


def fitData1(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81  #get force
    pylab.plot(xVals, yVals, 'bo',
               label='Measured points')
    labelPlot()
    model = pylab.polyfit(xVals, yVals, 1)
    estYVals = pylab.polyval(model, xVals)  # pylab.polyval函数产生根据拟合的model预测的y值
    pylab.plot(xVals, estYVals, 'r',
               label='Linear fit, k = '
                     + str(round(1 / model[0], 5)))
    pylab.legend(loc='best')


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
    pylab.show()


xVals, yVals = getData('mysteryData.txt')
degrees = (1, 2)  # 对比一阶、二阶的拟合效果
models = genFits(xVals, yVals, degrees)


# TestFits(models, degrees, xVals, yVals, 'Mystery Data')

# Compare higher-order fits
# degrees = (2, 4, 8, 16)  # 更高阶的拟合效果
# models = genFits(xVals, yVals, degrees)
# TestFits(models, degrees, xVals, yVals, 'Mystery Data')


def genNoisyParabolicData(a, b, c, xVals, fName):  # 生成带有噪声的抛物线型数据
    yVals = []
    for x in xVals:
        theoreticalVal = a * x ** 2 + b * x + c
        yVals.append(theoreticalVal \
                     + random.gauss(0, 35))  # 在理论函数上添加一个均值为 0、标准差为 35 的高斯噪声
    f = open(fName, 'w')
    f.write('x        y\n')
    for i in range(len(yVals)):
        f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
    f.close()


# parameters for generating data
xVals = range(-10, 11, 1)
a, b, c = 3.0, 0.0, 0.0
degrees = (2, 4, 8, 16)
#
# generate data
random.seed(0)
genNoisyParabolicData(a, b, c, xVals,
                      'Dataset 1.txt')
genNoisyParabolicData(a, b, c, xVals,
                      'Dataset 2.txt')
#
xVals1, yVals1 = getData('Dataset 1.txt')
models1 = genFits(xVals1, yVals1, degrees)
# TestFits(models1, degrees, xVals1, yVals1,
#          'DataSet 1.txt')  # 仍然是16阶拟合的R2最大
# #
# pylab.figure()
xVals2, yVals2 = getData('Dataset 2.txt')
models2 = genFits(xVals2, yVals2, degrees)
# TestFits(models2, degrees, xVals2, yVals2,
#          'DataSet 2.txt')  # 仍然是16阶拟合的R2最大
#
# 我们希望拟合结果具有普适性，进行交叉验证 -> 16阶为过拟合
pylab.figure()
TestFits(models1, degrees, xVals2, yVals2,
         'DataSet 2/Model 1')  # 将数据集2拟合到模型1，2阶和4阶拟合的R2最好
pylab.figure()
TestFits(models2, degrees, xVals1, yVals1,
         'DataSet 1/Model 2')  # 将数据集1拟合到模型2，2阶和4阶拟合的R2最好

# # a line
# xVals = (0, 1, 2, 3)
# yVals = xVals
# pylab.plot(xVals, yVals, label='Actual values')
# a, b, c = pylab.polyfit(xVals, yVals, 2)
# print('a =', round(a, 4), 'b =', round(b, 4),
#       'c =', round(c, 4))
# estYVals = pylab.polyval((a, b, c), xVals)  # a=0, b=1, c=0, 拟合结果为y=x
# pylab.plot(xVals, estYVals, 'r--', label='Predictive values')
# print('R-squared = ', rSquared(yVals, estYVals))  # R2 = 1.0
# pylab.legend(loc='best')
# pylab.show()
#
# # OPEN FOR SECOND DEMO
# #
# pylab.figure()  # 用于新开一个图形绘画窗口
# # Extend domain
# xVals = xVals + (20,)
# yVals = xVals
# pylab.plot(xVals, yVals, label='Actual values')
# estYVals = pylab.polyval((a, b, c), xVals)
# pylab.plot(xVals, estYVals, 'r--', label='Predictive values')
# print('R-squared = ', rSquared(yVals, estYVals))  # R2仍然为1.0
# pylab.legend(loc='best')
# pylab.show()
#
# # OPEN FOR THIRD DEMO
# # almost a line
# pylab.figure()
# xVals = (0, 1, 2, 3)
# yVals = (0, 1, 2, 3.1)  # 加入微小的噪声
# pylab.plot(xVals, yVals, label='Actual values')
# # model = pylab.polyfit(xVals, yVals, 2)  # 仍然使用二阶拟合
# model = pylab.polyfit(xVals, yVals, 1)  # 改用一阶拟合测试 R2=0.9987682926829268
# print(model)  # a, b, c = [0.025 0.955 0.005]
# estYVals = pylab.polyval(model, xVals)
# pylab.plot(xVals, estYVals, 'r--', label='Predicted values')
# print('R-squared = ', rSquared(yVals, estYVals))  # 0.9999057936881771
# pylab.legend(loc='best')
#
# # OPEN FOR FOURTH DEMO
#
# pylab.figure()
# # Extend domain
# xVals = xVals + (20,)
# yVals = xVals  # 实际的函数仍应该为y=x
# pylab.plot(xVals, yVals, label='Actual values')
# estYVals = pylab.polyval(model, xVals)  # 但是由于前面拟合出得模型是在加入了噪声的数据上拟合的，预测的值明显偏离
# pylab.plot(xVals, estYVals, 'r--', label='Predicted values')
# print('R-squared = ', rSquared(yVals, estYVals))  # 0.7026164813486382，此时拟合效果明显变差
# pylab.legend(loc='best')
# pylab.show()
