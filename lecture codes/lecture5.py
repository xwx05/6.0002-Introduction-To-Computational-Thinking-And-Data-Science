import random, pylab
import time

import matplotlib.pyplot as plt

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


class Location(object):  # 一个坐标
    def __init__(self, x, y):
        """x and y are numbers"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):  # 更新坐标
        """deltaX and deltaY are numbers"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):  # 计算欧几里得距离
        xDist = self.x - other.getX()
        yDist = self.y - other.getY()
        return (xDist ** 2 + yDist ** 2) ** 0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


class Field(object):  # a collection of places and drunks
    def __init__(self):
        self.drunks = {}  # key为Drunk, value为Location

    def addDrunk(self, drunk, loc):  # 添加一个Drunk到Field中
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):  # 更新Drunk的位置
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        # use move method of Location to get new location
        self.drunks[drunk] = self.drunks[drunk].move(xDist, yDist)

    def getLoc(self, drunk):  # 获取drunk的位置
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


class Drunk(object):
    def __init__(self, name=None):
        """Assumes name is a str"""
        self.name = name

    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'


class UsualDrunk(Drunk):  # 可能向4个方向移动一步
    def takeStep(self):
        stepChoices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(stepChoices)


class MasochistDrunk(Drunk):  # 总是向北移动的更多
    def takeStep(self):
        stepChoices = [(0.0, 1.1), (0.0, -0.9),
                       (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)


# 模拟一次numSteps步的随机行走
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
       Moves d numSteps times, and returns the distance between
       the final location and the location at the start of the
       walk."""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))  # 返回起止位置间的距离


# 模拟numTrials次随机行走
def simWalks(numSteps, numTrials, dClass):
    """Assumes numSteps an int >= 0, numTrials an int > 0,
         dClass a subclass of Drunk
       Simulates numTrials walks of numSteps steps each.
       Returns a list of the final distances for each trial"""
    Homer = dClass('Homer')
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)  # 每次行走把Homer放到原点
        distances.append(round(walk(f, Homer, numSteps), 1))  # round函数四舍五入保留1位小数
    return distances  # 返回多次行走的距离列表


def drunkTest(walkLengths, numTrials, dClass):
    """Assumes walkLengths a sequence of ints >= 0
         numTrials an int > 0, dClass a subclass of Drunk
       For each number of steps in walkLengths, runs simWalks with
         numTrials walks and prints results"""
    for numSteps in walkLengths:  # walkLengths 是一个指定的步数列表
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances) / len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))


# random.seed(0)
# random.seed(time.time())
# drunkTest((10, 100, 1000, 10000), 100, UsualDrunk)
# drunkTest((0, 1, 2), 100, UsualDrunk)


def simAll(drunkKinds, walkLengths, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)


# random.seed(0)
# random.seed(time.time())
# simAll((UsualDrunk, MasochistDrunk), (1000, 10000), 100)

# xVals = [1, 2, 3, 4]
# yVals1 = [1, 2, 3, 4]
# pylab.plot(xVals, yVals1, 'b-', label = 'first')
# yVals2 = [1, 7, 3, 5]
# pylab.plot(xVals, yVals2, 'r--', label = 'second')
# pylab.legend()
# plt.show()

class styleIterator(object):  # 迭代器类，用于选择绘图样式
    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result


def simDrunk(numTrials, dClass, walkLengths):  # 模拟不同步数下的随机行走，并计算每次模拟的平均距离
    meanDistances = []
    for numSteps in walkLengths:
        print('Starting simulation of',
              numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)  # trials 是一个距离列表
        mean = sum(trials) / len(trials)
        meanDistances.append(mean)
    return meanDistances


def simAll(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle,
                   label=dClass.__name__)
    pylab.title('Mean Distance from Origin ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc='best')


# random.seed(0)
# random.seed(time.time())
# numSteps = (10, 100, 1000, 10000, 100000)
# simAll((UsualDrunk, MasochistDrunk), numSteps, 100)
#
# pylab.plot(numSteps, pylab.array(numSteps) ** 0.5, 'k-.',
#            label='Square root of steps')  # 步数的平方根，通常用于表示随机游走的理论距离增长趋势
# # (参考：在Random Walk中，步数 n 和距离 D 之间的关系可以用扩散方程来描述)
# pylab.plot(numSteps, pylab.array(numSteps) * 0.05, 'g-.',
#            label='numSteps*0.05')  # 步数乘以 0.05，用于提供一个线性增长的参考
# pylab.legend(loc='best')
# plt.show()


def getFinalLocs(numSteps, numTrials, dClass):  # 画出numTrials次的落点
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs


def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals)) / len(xVals)
        meanY = sum(abs(yVals)) / len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label=dClass.__name__ + \
                         ' mean abs dist = <'
                         + str(meanX) + ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks ('
                + str(numSteps) + ' steps)')
    pylab.ylim(-1000, 1000)
    pylab.xlim(-1000, 1000)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='lower center')
    plt.show()


# random.seed(0)
random.seed(time.time())
# plotLocs((UsualDrunk, MasochistDrunk), 10000, 1000)


class OddField(Field):  # 继承自Field，添加了虫洞
    def __init__(self, numHoles=1000,
                 xRange=100, yRange=100):  # numHoles为虫洞数量，xRange和yRange为虫洞坐标的范围
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)  # Return random integer in range [a, b], including both end points.
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc  # 虫洞字典，键为原始位置，值为跳转的新位置

    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:  # 检查是否移动到了虫洞位置，如果是则跳转到新的位置
            self.drunks[drunk] = self.wormholes[(x, y)]


# TraceWalk using oddField
def traceWalk(fieldKinds, numSteps):  # 画出在两种场地的行走轨迹
    styleChoice = styleIterator(('b+', 'r^', 'ko'))
    for fClass in fieldKinds:
        d = UsualDrunk()
        # d = MasochistDrunk()
        f = fClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label=fClass.__name__)
    pylab.title('Spots Visited on Walk ('
                + str(numSteps) + ' steps)')
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='best')
    plt.show()


# random.seed(0) 设置随机数生成器的种子为 0。种子是一个固定的值，用于初始化随机数生成器的状态。
# 当使用相同的种子时，随机数生成器会生成相同的随机数序列。
random.seed(0)
random.seed(time.time())
traceWalk((Field, OddField), 500)
