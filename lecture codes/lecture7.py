import random, pylab, numpy

# set line width
pylab.rcParams['lines.linewidth'] = 4
# set font size for titles
pylab.rcParams['axes.titlesize'] = 20
# set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
# set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
# set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
# set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
# set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
# set size of markers, e.g., circles representing points
# set numpoints for legend
pylab.rcParams['legend.numpoints'] = 1


class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1, 37):  # 1~36号口袋
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1  # 总共 36 个口袋，除去押中的那一个，赔率是 35

    def spin(self):
        self.ball = random.choice(self.pockets)  # 随机旋转，确定球落入的口袋编号

    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt * self.pocketOdds
        else:
            return -amt

    def __str__(self):
        return 'Fair Roulette'


def playRoulette(game, numSpins, pocket, bet, toPrint):  # bet为每次下注的金额
    totPocket = 0  # 初始化总收益为0
    for i in range(numSpins):  # numSpins 表示要进行轮盘旋转（下注）的次数。
        game.spin()
        totPocket += game.betPocket(pocket, bet)  # 累计每次下注的收益
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=', \
              str(100 * totPocket / numSpins) + '%\n')  # 打印收益率
    return (totPocket / numSpins)  # 返回多次下注的平均收益


def findPocketReturn(game, numTrials, trialSize, toPrint):  # 多次重复进行一定次数的轮盘赌游戏
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)  # 固定下注口袋编号 2、每次下注金额 1
        pocketReturns.append(trialVals)
    return pocketReturns


def getMeanAndStd(X):  # 用于计算给定数据列表X的均值和标准差
    mean = sum(X) / float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean) ** 2
    std = (tot / len(X)) ** 0.5
    return mean, std


# random.seed(1)
# dist, numSamples = [], 1000000
#
# for i in range(numSamples):
#     dist.append(random.gauss(0, 100))  # 生成 1000000 个服从均值为 0、标准差为 100 的正态分布的随机数
#
# weights = [1 / numSamples] * len(dist)  # 保证每个数据的具有相同的权重，以便直方图可以更准确地反映数据的概率分布
# v = pylab.hist(dist, bins=100,
#                weights=[1 / numSamples] * len(dist))
#
# # bins=100 指定了直方图的区间数量为 100，也就是将数据的取值范围划分成 100 个等间距的区间来统计落入每个区间的数据情况
# print('Fraction within ~200 of mean =',
#       sum(v[0][30:70]))  # 对于正态分布，大约 68% 的数据会落在均值左右 1 个标准差范围内，大约 95% 的数据落在均值左右 2 个标准差范围内等
# pylab.show()

def gaussian(x, mu, sigma):  # 定义了正态分布的概率密度函数公式
    factor1 = (1.0 / (sigma * ((2 * pylab.pi) ** 0.5)))
    factor2 = pylab.e ** -(((x - mu) ** 2) / (2 * sigma ** 2))
    return factor1 * factor2


# xVals, yVals = [], []
# mu, sigma = 0, 1
# x = -4
# while x <= 4:  # 通过循环在-4到4的范围内以步长 0.05 生成x值，计算对应的正态分布概率密度函数值作为y值
#     xVals.append(x)
#     yVals.append(gaussian(x, mu, sigma))
#     x += 0.05
# pylab.plot(xVals, yVals)
# pylab.title('Normal Distribution, mu = ' + str(mu) \
#             + ', sigma = ' + str(sigma))  # 根据数学公式绘制正态分布曲线
# pylab.show()

import scipy.integrate


# 多次随机生成不同的均值mu和标准差sigma，通过积分计算在给定标准差倍数（1、1.96、3）范围内正态分布曲线下的面积（即概率），以此来验证正态分布的一些经验性质
def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-10, 10)
        sigma = random.randint(1, 10)
        print('For mu =', mu, 'and sigma =', sigma)
        for numStd in (1, 1.96, 3):
            area = scipy.integrate.quad(gaussian,
                                        mu - numStd * sigma,
                                        mu + numStd * sigma,
                                        (mu, sigma))[0]
            print(' Fraction within', numStd,
                  'std =', round(area, 4))


# checkEmpirical(3)

#Test CLT  验证中心极限定理
def plotMeans(numDice, numRolls, numBins, legend, color, style):  # 模拟掷骰子并计算多次掷骰子的平均值的分布情况
    means = []
    for i in range(numRolls // numDice):
        vals = 0
        for j in range(numDice):
            vals += 5 * random.random()
        means.append(vals / float(numDice))
    pylab.hist(means, numBins, color=color, label=legend,
               weights=[1 / len(means)] * len(means),
               hatch=style)
    return getMeanAndStd(means)


# mean, std = plotMeans(1, 1000000, 19, '1 die', 'b', '*')
# print('Mean of rolling 1 die =', str(mean) + ',', 'Std =', std)
# mean, std = plotMeans(50, 1000000, 19, 'Mean of 50 dice', 'r', '//')
# print('Mean of rolling 50 dice =', str(mean) + ',', 'Std =', std)  # 随着掷骰子次数的增加，平均值的分布趋于正态分布
# pylab.title('Rolling Continuous Dice')
# pylab.xlabel('Value')
# pylab.ylabel('Probability')
# pylab.legend()
# pylab.show()

#Test CLT
numTrials = 1000000  # 试验次数
numSpins = 200  # 每次试验下注的次数
game = FairRoulette()

means = []
for i in range(numTrials):
    means.append(findPocketReturn(game, 1, numSpins,
                                  False)[0])  # 200次下注平均收益率的概率分布


pylab.hist(means, bins=19,
           weights=[1 / len(means)] * len(means))
pylab.xlabel('Mean Return')
pylab.ylabel('Probability')
pylab.title('Expected Return Betting a Pocket 200 Times')
pylab.show()

def throwNeedles(numNeedles):
    inCircle = 0
    for Needles in range(1, numNeedles + 1, 1):  # 在单位正方形内随机生成点
        x = random.random()
        y = random.random()
        if (x * x + y * y) ** 0.5 <= 1.0:
            inCircle += 1
    return 4 * (inCircle / float(numNeedles))


def getEst(numNeedles, numTrials):  # 多次试验，计算估计值的平均值和标准差
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = numpy.std(estimates)
    curEst = sum(estimates) / len(estimates)
    print('Est. = ' + str(curEst) + \
          ', Std. dev. = ' + str(round(sDev, 6)) \
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)


def estPi(precision, numTrials):  # 不断增加投针数量，重复调用getEst函数来逐步提高估算圆周率的精度，直到估算值的标准差小于等于给定精度的一半
    numNeedles = 1000
    sDev = precision
    while sDev >= precision / 2:
        curEst, sDev = getEst(numNeedles,
                              numTrials)
        numNeedles *= 2
    return curEst

# random.seed(0)
# estPi(0.005, 100)
