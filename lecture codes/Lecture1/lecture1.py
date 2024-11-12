class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v  # value-喜爱程度
        self.calories = w  # calories

    def getValue(self):
        return self.value

    def getCost(self):
        return self.calories

    def density(self):
        return self.getValue() / self.getCost()  # 最喜爱且消耗卡路里最少

    def __str__(self):
        return self.name + ': <' + str(self.value) \
            + ', ' + str(self.calories) + '>'


def buildMenu(names, values, calories):
    """names, values, calories lists of same length.
       name a list of strings
       values and calories lists of numbers
       returns list of Foods"""
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i],
                         calories[i]))
    return menu


def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of items to numbers"""
    itemsCopy = sorted(items, key=keyFunction,
                       reverse=True)  # keyFunction决定根据哪个值排序
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost + itemsCopy[i].getCost()) <= maxCost:  # 累计卡路里不超过限制
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()  # 累计value
    return (result, totalValue)


def TestGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)


def TestGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, Food.getValue)  # 按照value从大到小排序
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, lambda x: 1 / Food.getCost(x))  # cost取倒数按照从大到小排序，即按照cost从小到大排序
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    TestGreedy(foods, maxUnits, Food.density)  # 按照density从大到小排序


names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89, 90, 95, 100, 90, 79, 50, 10]
calories = [123, 154, 258, 354, 365, 150, 95, 195]
foods = buildMenu(names, values, calories)
TestGreedys(foods, 900)
