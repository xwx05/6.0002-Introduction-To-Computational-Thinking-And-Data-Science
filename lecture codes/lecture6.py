import random, pylab
import time

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
        for i in range(1, 37):
            self.pockets.append(i)  # 模拟轮盘上的1~36号口袋
        self.ball = None  # 初始化为 None，用于表示轮盘旋转后球最终落入的口袋编号
        self.pocketOdds = len(self.pockets) - 1  # 也就是总共 36 个口袋，除去押中的那一个，赔率是 35

    def spin(self):
        self.ball = random.choice(self.pockets)  # 随机旋转，确定球落入的口袋编号

    def betPocket(self, pocket, amt):  # amt表示下注金额
        if str(pocket) == str(self.ball):
            return amt * self.pocketOdds  # 如果押中，获得下注金额*赔率
        else:
            return -amt  # 没押中时扣掉下注金额

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


# random.seed(0)
# random.seed(time.time())
# game = FairRoulette()
# for numSpins in (100, 1000000):
#     for i in range(3):
#         playRoulette(game, numSpins, 2, 1, True)  # 固定下注口袋编号 2、每次下注金额 1


#  两种更不公平的轮盘
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')  # 添加一个标记为0的口袋

    def __str__(self):
        return 'European Roulette'


class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')  # 在EuRoulette基础上再添加一个标记为00的口袋

    def __str__(self):
        return 'American Roulette'


def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):  # 进行numTrials次试验
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)  # 每次试验进行trialSize次轮盘旋转（下注）操作
        pocketReturns.append(trialVals)  # 记录每次试验的收益率
    return pocketReturns


# random.seed(0)
# # random.seed(time.time())
numTrials = 20  # 20次试验
#
# resultDict = {}
# games = (FairRoulette, EuRoulette, AmRoulette)  # 遍历三种不同的轮盘
# for G in games:
#     resultDict[G().__str__()] = []
# for numSpins in (1000, 10000, 100000, 1000000):
#     print('\nSimulate', numTrials, 'trials of', numSpins, 'spins each')
#     for G in games:
#         pocketReturns = findPocketReturn(G(), numTrials, numSpins, False)
#         expReturn = 100 * sum(pocketReturns) / len(pocketReturns)  # 统计某种轮盘类型的收益率
#         print('Exp. return for', G(), '=',
#               str(round(expReturn, 4)) + '%')


def getMeanAndStd(X):
    mean = sum(X) / float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean) ** 2
    std = (tot / len(X)) ** 0.5  # 计算标准差
    return mean, std


random.seed(0)
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
for G in games:
    resultDict[G().__str__()] = []
for numSpins in (1000, 100000, 1000000):
    print('\nSimulate betting a pocket for', numTrials, 'trials of', numSpins, 'spins each')
    for G in games:
        pocketReturns = findPocketReturn(G(), 20, numSpins, False)
        mean, std = getMeanAndStd(pocketReturns)
        resultDict[G().__str__()].append((numSpins, 100 * mean, 100 * std))
        print('Exp. return for', G(), '=', str(round(100 * mean, 3))
              + '%,', '+/- ' + str(round(100 * 1.96 * std, 3))
              + '% with 95% confidence')
