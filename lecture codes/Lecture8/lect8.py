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


def makeHist(data, title, xlabel, ylabel, bins=20):
    pylab.hist(data, bins=bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)


def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1])
            population.append(tempC)
        except:
            continue
    return population  # 获取所有温度数据


def getMeansAndSDs(population, sample, verbose=False):
    popMean = sum(population) / len(population)
    sampleMean = sum(sample) / len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' + \
                 '(mean = ' + str(round(popMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        pylab.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' + \
                 '(mean = ' + str(round(sampleMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean, \
        numpy.std(population), numpy.std(sample)


# random.seed(0)
# population = getHighs()
# sample = random.sample(population, 100)
# getMeansAndSDs(population, sample, True)

# random.seed(0)
# population = getHighs()
# sampleSize = 100  # 总体中随机抽取 100 个数据作为样本
# numSamples = 1000  # 抽样次数
# sampleMeans = []
# for i in range(numSamples):
#     sample = random.sample(population, sampleSize)
#     popMean, sampleMean, popSD, sampleSD = \
#         getMeansAndSDs(population, sample, verbose=False)
#     sampleMeans.append(sampleMean)
# print('Mean of sample Means =',
#       round(sum(sampleMeans) / len(sampleMeans), 3))  # 计算样本均值的均值
# print('Standard deviation of sample means =',
#       round(numpy.std(sampleMeans), 3))
# makeHist(sampleMeans, 'Means of Samples', 'Mean', 'Frequency')  # 绘制样本均值的直方图
# pylab.axvline(x=popMean, color='r')  # 绘制总体均值作为参考线
# pylab.show()

def showErrorBars(population, sizes, numTrials):  # 误差棒图
    xVals = []
    sizeMeans, sizeSDs = [], []
    for sampleSize in sizes:  # 对不同样本大小分别进行numTrials次试验
        xVals.append(sampleSize)
        trialMeans = []
        for t in range(numTrials):
            sample = random.sample(population, sampleSize)
            popMean, sampleMean, popSD, sampleSD = \
                getMeansAndSDs(population, sample)
            trialMeans.append(sampleMean)
        sizeMeans.append(sum(trialMeans) / len(trialMeans))
        sizeSDs.append(numpy.std(trialMeans))
    print(sizeSDs)
    pylab.errorbar(xVals, sizeMeans,
                   yerr=1.96 * pylab.array(sizeSDs), fmt='o',
                   label='95% Confidence Interval')
    pylab.title('Mean Temperature ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Sample Size')
    pylab.ylabel('Mean')
    pylab.axhline(y=popMean, color='r', label='Population Mean')
    pylab.xlim(0, sizes[-1] + 10)
    pylab.legend()
    pylab.show()


'''
可以看出较大的样本数下，置信区间明显变小，但是此时试验次数进行了600*100=600k次，而总体数据仅为422k
'''


# random.seed(0)
# population = getHighs()
# showErrorBars(population,
#               (50, 100, 200, 300, 400, 500, 600), 100)


def sem(popSD, sampleSize):  # 计算标准误差
    return popSD / sampleSize ** 0.5


# sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600)
# numTrials = 50
# population = getHighs()
# popSD = numpy.std(population)
# sems = []
# sampleSDs = []
# for size in sampleSizes:  # 对每个样本size
#     sems.append(sem(popSD, size))  # 直接根据公式计算样本的标准差
#     means = []
#     for t in range(numTrials):  # 进行numTrials次试验
#         sample = random.sample(population, size)  # 随机抽样
#         means.append(sum(sample) / len(sample))  # 计算均值
#     sampleSDs.append(numpy.std(means))  # 计算多次试验样本均值的标准差
# pylab.plot(sampleSizes, sampleSDs,
#            label='Std of ' + str(numTrials) + ' means')
# pylab.plot(sampleSizes, sems, 'r--', label='SEM')
# pylab.xlabel('Sample Size')
# pylab.ylabel('Std and SEM')
# pylab.title('SD for ' + str(numTrials) + ' Means and SEM')
# pylab.legend()
# pylab.show()


def plotDistributions():  # 模拟绘制三种分布的直方图
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform, 'Uniform', 'Value', 'Frequency')
    pylab.figure()
    makeHist(normal, 'Gaussian', 'Value', 'Frequency')
    pylab.figure()
    makeHist(exp, 'Exponential', 'Value', 'Frequency')


# plotDistributions()


def getDiffs(population, sampleSizes):
    popStd = numpy.std(population)  # 计算总体标准差
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popStd - numpy.std(sample)))  # 针对每个样本大小，多次抽取样本（100 次）计算样本标准差与总体标准差差值的绝对值
        diffMean = sum(diffs) / len(diffs)  # 求这些差值的平均值
        diffsFracs.append(diffMean / popStd)  # 除以总体标准差得到相对差异
    return pylab.array(diffsFracs) * 100


def plotDiffs(sampleSizes, diffs, title, label, color='b'):
    pylab.plot(sampleSizes, diffs, label=label,
               color=color)
    pylab.xlabel('Sample Size')
    pylab.ylabel('% Difference in SD')
    pylab.title(title)
    pylab.legend()


'''
Once sample reaches a reasonable size, 
sample standard deviation is a pretty good approximation to population standard deviation
'''


# sampleSizes = range(20, 600, 1)
# diffs = getDiffs(getHighs(), sampleSizes)
# plotDiffs(sampleSizes, diffs,
#           'Sample SD vs Population SD, Temperatures',
#           label='High temps')
# pylab.show()


def compareDists():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs,
              'Sample SD vs Population SD',
              'Uniform population', 'm')
    plotDiffs(sampleSizes, ndiffs,
              'Sample SD vs Population SD',
              'Normal population', 'b')
    plotDiffs(sampleSizes, ediffs,
              'Sample SD vs Population SD',
              'Exponential population', 'r')
    pylab.show()


# compareDists()  # 可以看出趋势与Distributions无关

# colors = ['r', 'g', 'b']  # 修改原代码，用不同颜色绘制
# popSizes = (10000, 100000, 1000000)
# sampleSizes = range(20, 600, 1)
# color_index = 0  # 用于记录当前使用的颜色索引
# for size in popSizes:
#     population = []
#     for i in range(size):
#         population.append(random.expovariate(0.5))
#     ediffs = getDiffs(population, sampleSizes)
#     # 获取当前要使用的颜色
#     cur_color = colors[color_index % len(colors)]
#     plotDiffs(sampleSizes, ediffs,
#               'Sample SD vs Population SD, Uniform',
#               'Population size = ' + str(size),
#               color=cur_color)
#     color_index += 1
#
# pylab.show()

temps = getHighs()
popMean = sum(temps) / len(temps)
sampleSize = 200  # 根据前面的分析，选择样本大小为200
numTrials = 10000

random.seed(0)
numBad = 0
for t in range(numTrials):
    posStartingPts = range(0, len(temps) - sampleSize)  # 抽样方式为“选取连续的一段数据作为样本”
    start = random.choice(posStartingPts)
    sample = temps[start:start + sampleSize]
    sampleMean = sum(sample) / sampleSize
    se = numpy.std(sample) / sampleSize ** 0.5
    if abs(popMean - sampleMean) > 1.96 * se:
        numBad += 1
print('Fraction outside 95% confidence interval =',
      numBad / numTrials)  # 0.8906，非常不可靠的结果

random.seed(0)
numBad = 0
for t in range(numTrials):
    sample = random.sample(temps, sampleSize)  # 使用随机抽样方式
    sampleMean = sum(sample) / sampleSize
    se = numpy.std(sample) / sampleSize ** 0.5
    if abs(popMean - sampleMean) > 1.96 * se:
        numBad += 1
print('Fraction outside 95% confidence interval =',
      numBad / numTrials)  # 0.0511，说明样本大小为200时的随机抽样方式已经很可靠
