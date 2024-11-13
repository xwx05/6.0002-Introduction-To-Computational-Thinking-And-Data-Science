###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time


#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    print("Loading cow data from file...")
    # inFile: file
    with open('ps1_cow_data.txt', 'r') as inFile:
        # 读取所有行并去除每行末尾的换行符
        lines = [line.strip() for line in inFile.readlines()]

        # 解析每一行的数据并存储到字典中
        cowdata = {line.split(',')[0]: int(line.split(',')[1]) for line in lines}

    return cowdata


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    sorted_cows = sorted(cows.items(), key=lambda item: item[1], reverse=True)  # 按照cows字典的values降序排序，但不会改变原始cows字典
    cowsCopy = dict(sorted_cows).copy()
    trips = []
    while len(cowsCopy) != 0:
        current_weight = 0
        current_trip = []
        for cow_name, cow_weight in sorted_cows:
            if cow_name in cowsCopy and current_weight + cow_weight <= limit:  # current_trip下，已经运送的牛不在考虑
                current_trip.append(cow_name)
                current_weight += cow_weight
                del cowsCopy[cow_name]  # 已经运送的牛从cowsCopy中移除
        trips.append(current_trip)
    return trips


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cowsCopy = cows.copy()
    best_solution = None
    partitions = get_partitions(cowsCopy)

    for partition in partitions:
        valid_partition = True
        for current_trip in partition:
            current_weight = 0
            for cow in current_trip:
                current_weight += cowsCopy[cow]
                if current_weight > limit:
                    valid_partition = False
                    break
            if not valid_partition:
                break
        if valid_partition:
            if best_solution is None or len(partition) < len(best_solution):
                best_solution = partition
    return best_solution


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here

    # cows = {"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}
    cows = load_cows('ps1_cow_data.txt')
    # RUNNING TIME OF GREEDY ALGORITHM
    start = time.time()
    print(greedy_cow_transport(cows))
    end = time.time()
    print("RUNNING TIME OF GREEDY ALGORITHM:", end - start)

    # RUNNING TIME OF BRUTE FORCE ALGORITHM
    start = time.time()
    print(brute_force_cow_transport(cows))
    end = time.time()
    print("RUNNING TIME OF BRUTE FORCE ALGORITHM:", end - start)

if __name__ == '__main__':
    print(compare_cow_transport_algorithms())

"""
1. What were your results from compare_cow_transport_algorithms? Which 
algorithm runs faster? Why?
A: greedy_cow_transport更快，brute_force_cow_transport需要枚举所有可能的分区，然后检查每个分区是否满足重量限制。
生成所有可能分区的时间复杂度是指数级的，即O(2^n)

2. Does the greedy algorithm return the optimal solution? Why/why not?
A: 贪心算法 不一定返回最优解。
原因：
贪心算法 的策略是每次选择当前最重的牛来尽量减少行程数。这种局部最优的选择并不一定能保证全局最优。

3. Does the brute force algorithm return the optimal solution? Why/why not?
A: 暴力算法 总是返回最优解。
原因：
暴力算法 枚举了所有可能的分区，并检查每个分区是否满足重量限制。它会找到所有有效的分区，并从中选择行程数最少的分区。
"""