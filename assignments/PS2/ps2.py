# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge


#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# Nodes represent buildings on MIT campus.
# Edges represent paths between these buildings.
# Distances are represented by the 'TotalDistance' attribute of each edge.
# Outdoor distances are represented by the 'OutdoorDistance' attribute of each edge.


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    print("Loading map from file...")
    with open(map_filename, 'r') as inFile:
        # 读取所有行并去除每行末尾的换行符
        lines = [line.strip() for line in inFile.readlines()]

        mit_map = Digraph()
        for line in lines:
            data = line.split(' ')
            from_node = Node(data[0])
            to_node = Node(data[1])
            total_distance = int(data[2])
            outdoor_distance = int(data[3])
            edge = WeightedEdge(from_node, to_node, total_distance, outdoor_distance)
            # 添加节点时避免重复添加
            if not mit_map.has_node(from_node):
                mit_map.add_node(from_node)
            if not mit_map.has_node(to_node):
                mit_map.add_node(to_node)

            mit_map.add_edge(edge)
    return mit_map


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print(load_map("test_load_map.txt"))


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective function is to find the shortest path from start to end building.
# The constraints are not exceeding the maximum distance outdoors.

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # 约束条件包括路径的总户外距离不能超过 max_dist_outdoors，同时在寻找过程中会不断更新并记录目前找到的best_path及对应best_dist
    # Convert start and end to Node objects
    start_node = Node(start)  # 将 start 和 end 转换为 Node 对象
    end_node = Node(end)
    path[0] = path[0] + [start]  # 将当前节点添加到路径中
    current_path, total_dist, outdoor_dist = path

    # Check if start and end nodes are valid
    if not (digraph.has_node(start_node) and digraph.has_node(end_node)):
        raise ValueError('Start or end node not in graph')

    elif start_node == end_node:  # 到达目标节点
        if total_dist < best_dist:  # 检查当前路径的总距离是否小于已知的最佳距离。如果是，则更新最佳路径和最佳距离。
            best_dist = total_dist
            best_path = current_path[:]
        return (best_path, best_dist)

    else:
        # Get all edges from the current node
        edges = digraph.get_edges_for_node(start_node)
        for edge in edges:  # 遍历起始节点的所有边及对应子节点
            next_node = edge.get_destination()
            next_node_name = next_node.get_name()
            edge_total_dist = edge.get_total_distance()  # 获得目前正在处理的edge的总距离和户外距离
            edge_outdoor_dist = edge.get_outdoor_distance()

            # Check if adding the edge violates the constraints
            if next_node_name not in current_path:  # Avoid cycles
                new_total_dist = total_dist + edge_total_dist  # 加上当前edge的总距离
                new_outdoor_dist = outdoor_dist + edge_outdoor_dist  # 加上当前edge的户外距离

                if new_outdoor_dist <= max_dist_outdoors and new_total_dist <= best_dist:  # 户外距离不能超过限制，且总距离没有超过最佳距离
                    # Recursively call get_best_path with the updated path
                    new_path = [current_path[:], new_total_dist, new_outdoor_dist]
                    best_path, best_dist = get_best_path(digraph, next_node_name, end, new_path, max_dist_outdoors,
                                                         best_dist, best_path)

    return (best_path, best_dist)


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    path = [[], 0, 0]  # 初始化路径，总距离和户外距离
    best_path, best_dist = get_best_path(digraph, start, end, path, max_dist_outdoors, max_total_dist, [])

    if best_dist >= max_total_dist:
        raise ValueError('No path satisfies the constraints')
    return best_path


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999  # 使用这个很大的距离值，在没有特别指定时相当于不对总距离做严格限制

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)  # 这里total_dist即为max_total_dist限制


if __name__ == "__main__":
    unittest.main()
