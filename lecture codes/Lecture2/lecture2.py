class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w

    def getValue(self):
        return self.value

    def getCost(self):
        return self.calories

    def density(self):
        return self.getValue() / self.getCost()

    def __str__(self):
        return self.name + ': <' + str(self.value) \
            + ', ' + str(self.calories) + '>'


def buildMenu(names, values, calories):
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i],
                         calories[i]))
    return menu


def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of Items to numbers"""
    itemsCopy = sorted(items, key=keyFunction,
                       reverse=True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost + itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)


def TestGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)


def TestGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, lambda x: 1 / Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, Food.density)


def maxVal(toConsider, avail):  # toConsider 是一个列表，包含待考虑是否放入背包的所有物品；avail 是背包剩余的可用容量
    """Assumes toConsider a list of items, avail a weight
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the items of that solution"""
    if toConsider == [] or avail == 0:
        result = (0, ())  # 如果没有任何物品可以考虑或者背包已经没有剩余空间，则返回 (0, ())，表示总价值为0，且没有选中任何物品
    elif toConsider[0].getCost() > avail:  # 第一个物品的cost超过了背包的剩余可用空间，无法放入背包，只能从之后的物品开始考虑
        #Explore right branch only
        result = maxVal(toConsider[1:], avail)
    else:  # 第一个物品可以放入背包，自行选择放入或不放入
        nextItem = toConsider[0]  # 获得当前要进行判断的第一个物品
        #Explore left branch
        withVal, withToTake = maxVal(toConsider[1:],
                                     avail - nextItem.getCost())  # 选择了第一个物品的情况，减去该物品和其价值
        withVal += nextItem.getValue()  # 已选择的物品的价值
        #Explore right branch
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)  # 没有选择nextItem
        #Choose better branch，即选择总价值更大的branch返回
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))  # 选择了第一个物品，加进结果元组
        else:
            result = (withoutVal, withoutToTake)
    return result


def TestMaxVal(foods, maxUnits, printItems=True):
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = maxVal(foods, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print('   ', item)


names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89, 90, 95, 100, 90, 79, 50, 10]
calories = [123, 154, 258, 354, 365, 150, 95, 195]
foods = buildMenu(names, values, calories)

TestGreedys(foods, 750)
print('')
TestMaxVal(foods, 750)

import random


def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    return items


# 计算速度太慢
# for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45):
#    print('Try a menu with', numItems, 'items')
#    items = buildLargeMenu(numItems, 90, 250)
#    TestMaxVal(items, 750, False)

# 常规思路计算斐波那契数列，重复调用
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# for i in range(121):
#    print('fib(' + str(i) + ') =', fib(i))


def fastFib(n, memo={}):
    """Assumes n is an int >= 0, memo used only by recursive calls
       Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fastFib(n - 1, memo) + fastFib(n - 2, memo)
        memo[n] = result
        return result


# for i in range(121):
#    print('fib(' + str(i) + ') =', fastFib(i))


def fastMaxVal(toConsider, avail, memo={}):  # 参考斐波那契数列的记忆化实现，避免重复计算
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]  # memo字典存储计算过的（剩余要考虑的物品数量，剩余可用cost），这样做确保未来遇到相同的子问题时可以直接使用已有的结果。
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake = \
            fastMaxVal(toConsider[1:],
                       avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                               avail, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result  # 存储的值为在（剩余要考虑的物品数量，剩余可用cost）时，可以得到的最大价值的物品组合
    return result


def TestMaxVal(foods, maxUnits, algorithm, printItems=True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = algorithm(foods, maxUnits)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)


for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
    items = buildLargeMenu(numItems, 90, 250)
    TestMaxVal(items, 750, fastMaxVal, True)
