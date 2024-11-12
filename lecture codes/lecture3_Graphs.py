# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:04:56 2016

@author: guttag, revised egrimson
"""


class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Edge(object):
    def __init__(self, src, dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()


class Digraph(object):
    """Adjacency list: edges is a dict mapping each node to a list of
    its children"""

    def __init__(self):
        self.edges = {}

    def addNode(self, node):  # Node是edges字典的key,
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []

    def addEdge(self, edge):  # key是src Node，value是dest Node列表，共同构成edges
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)

    def childrenOf(self, node):  # children也即destNode列表
        return self.edges[node]

    def hasNode(self, node):
        return node in self.edges

    def getNode(self, name):  # 要找的是在 self.edges 中的一个满足名称条件的节点
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)

    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->' \
                         + dest.getName() + '\n'
        return result[:-1]  # omit final newline


class Graph(Digraph):  # Graph 继承自 Digraph
    def addEdge(self, edge):  # 无向图，添加双向边
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):  # Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


# 深度优先搜索
def DFS(graph, start, end, path, shortest, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns the shortest path from start to end in graph"""
    path = path + [start]  # start为出发节点
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:  # 如果已经到达目标节点
        return path
    for node in graph.childrenOf(start):  # 在出发节点的子节点中遍历
        if node not in path:  # avoid cycles，即node还没有访问过
            if shortest == None or len(path) < len(shortest):  # 如果当前路径比已有最短路径更短
                newPath = DFS(graph, node, end, path, shortest,
                              toPrint)  # 以此节点为出发节点start进行DFS，即先沿着某一条支路往深处探索
                if newPath != None:  # 如果找到了新的最短路径，更新shortest
                    shortest = newPath
        elif toPrint:
            print('Already visited', node)  # 已经访问过，但不是最短路径
    return shortest


def shortestPath(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)


def TestSP(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination),
                      toPrint=True)
    if sp != None:
        print('Shortest path from', source, 'to',
              destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)


# TestSP('Chicago', 'Boston')
# print()
# TestSP('Boston', 'Phoenix')
# print()

printQueue = True

# 广度优先搜索
"""
由于 BFS 是按照离起始节点的距离（以边的数量来衡量）从小到大的顺序来探索路径的，所以一旦找到目标节点，这条路径必然是最短路径。
假设存在另一条更短的路径到达目标节点。但是根据 BFS 的搜索顺序，这条更短的路径会在之前就被探索到，因为它的节点层数更少。
"""


def BFS(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]  # 队列将用于存储待探索的路径
    while len(pathQueue) != 0:  # 还有待探索的路径
        # Get and remove oldest element in pathQueue
        if printQueue:  # 打印路径列表
            print('Queue:', len(pathQueue))
            for p in pathQueue:
                print(printPath(p))
        tmpPath = pathQueue.pop(0)  # 当前正在探索的路径，使用pop以确保按照先进先出的原则进行探索
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
            print()
        lastNode = tmpPath[-1]
        if lastNode == end:  # 判断是否到达目标节点
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):  # 还没到达目标节点，遍历 lastNode 的所有子节点 nextNode。
            if nextNode not in tmpPath:  # nextNode 可能是已经探索过的，避免重复探索
                newPath = tmpPath + [nextNode]  # 创建一个新的路径 newPath，并将 nextNode 添加到 tmpPath 的末尾。
                # 将下一层的节点先都加入pathQueue，由于对pathQueue的探索是按照先进先出的顺序，这样保证是先探索当前层的所有节点，再探索下一层
                pathQueue.append(newPath)
    return None  # 遍历完所有可能的路径仍未找到目标节点


def shortestPath(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)


TestSP('Boston', 'Phoenix')
