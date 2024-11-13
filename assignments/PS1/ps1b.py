###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    # Base case: if target_weight is 0, no eggs are needed
    if target_weight == 0:
        return 0

    if target_weight in memo:
        return memo[target_weight]  # 计算过的，针对某个目标重量所需要的最少鸡蛋数

    # Initialize the minimum number of eggs to a large number
    minEggs = float('inf')

    # Try each egg weight and recursively find the minimum number of eggs needed
    for weight in egg_weights:
        # 例如当target_weight = 5时，先用weight = 1尝试，得到numEggs = 5，然后用weight = 5尝试，得到numEggs = 1，更新minEggs为1。
        if target_weight - weight >= 0:  # 对于某种鸡蛋重量，目标重量减去该鸡蛋重量后大于0，才可以使用当前这个鸡蛋重量来凑目标重量。
            numEggs = dp_make_weight(egg_weights, target_weight - weight, memo) + 1  # 加上一个当前使用的鸡蛋
            # 得到使用当前鸡蛋重量参与组合凑目标重量时总共需要的鸡蛋个数 numEggs。和之前记录的最小鸡蛋个数 minEggs 进行比较，
            # 更新 minEggs 为两者中的较小值，这样不断循环遍历所有鸡蛋重量后，minEggs 就会记录下所有可能组合中最少的鸡蛋个数。
            minEggs = min(minEggs, numEggs)

    # Store the result in the memo dictionary
    memo[target_weight] = minEggs

    return minEggs




# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 11
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

"""
1. Explain why it would be difficult to use a brute force algorithm to solve this problem if there 
were 30 different egg weights. You do not need to implement a brute force algorithm in order to 
answer this.
A: 在暴力算法中，需要穷举所有可能的鸡蛋组合情况来找到达到目标重量的最少鸡蛋个数。
对于给定的 30 种不同鸡蛋重量，随着目标重量的增加，可能的组合数量会呈指数级增长。
例如，假设要达到一个特定的目标重量，每一种鸡蛋重量都有选或不选两种情况，那么总的组合可能性就有2^30种

2. If you were to implement a greedy algorithm for finding the minimum number of eggs 
needed, what would the objective function be? What would the constraints be? What strategy 
would your greedy algorithm follow to pick which coins to take? You do not need to implement a 
greedy algorithm in order to answer this.
A: 
目标函数：最小化所使用的鸡蛋个数。
约束条件：所选鸡蛋的重量之和必须等于给定的目标重量。只能从给定的 30 种鸡蛋重量集合中去选择鸡蛋，不能使用集合之外的其他重量值。
选取策略：每次都从从当前剩余的鸡蛋重量集合中挑选出最大重量且能使剩余目标重量仍大于等于 0 的鸡蛋，
        然后更新目标重量（减去已选鸡蛋的重量），重复这个过程，直到目标重量变为 0，也就是凑出了目标重量。
        这样的策略是希望通过优先选择大重量的鸡蛋，尽可能用少的鸡蛋个数来达到目标重量。
 
3. Will a greedy algorithm always return the optimal solution to this problem? Explain why it is 
optimal or give an example of when it will not return the optimal solution. Again, you do not need 
to implement a greedy algorithm in order to answer this.
A: 局部最优不能保证全局最优。假设有以下鸡蛋重量：{1,7,10}，目标重量为 14。
使用贪心算法的结果是5(10+4*1)，而最优解应该是2(7+7)。
"""