# o(n^2) level Dijkstra algorithm implementation

import heapq
import sys

def dijkstra(graph, start):
    """
    使用Dijkstra算法计算从起点到所有其他顶点的最短路径
    
    参数:
    graph: 邻接表表示的图，格式为 {u: [(v, w), ...]}，表示从u到v的边权为w
    start: 起始顶点
    
    返回:
    dist: 从起点到所有顶点的最短距离字典
    """
    n = len(graph)
    # 初始化距离数组，所有点的距离初始化为无穷大
    dist = {i: float('inf') for i in graph}
    # 起点到自身的距离为0
    dist[start] = 0
    # 已访问集合
    visited = set()
    
    # O(n^2)实现，每次找到未访问点中距离最小的点
    for _ in range(n):
        # 找到未访问点中距离最小的点
        min_dist = float('inf')
        min_vertex = None
        for v in graph:
            if v not in visited and dist[v] < min_dist:
                min_dist = dist[v]
                min_vertex = v
        
        # 如果没有可达的未访问点，则退出
        if min_vertex is None:
            break
        
        # 将该点加入已访问集合
        visited.add(min_vertex)
        
        # 更新相邻点的距离
        for neighbor, weight in graph[min_vertex]:
            if dist[min_vertex] + weight < dist[neighbor]:
                dist[neighbor] = dist[min_vertex] + weight
    
    return dist

def main():
    # 读取输入
    n, m = map(int, input().split())  # n个顶点，m条边
    
    # 初始化图
    graph = {i: [] for i in range(1, n+1)}
    
    # 读取边
    for _ in range(m):
        u, v, w = map(int, input().split())  # 从u到v的边，权重为w
        graph[u].append((v, w))
    
    # 计算从1号顶点出发的最短路径
    distances = dijkstra(graph, 1)
    
    # 输出结果
    for i in range(1, n+1):
        if i == 1:
            print(0)  # 起点到自身的距离为0
        else:
            if distances[i] == float('inf'):
                print(-1)  # 不可达
            else:
                print(distances[i])

if __name__ == "__main__":
    main()
    
## test case
"""
input:
4 5
1 2 2
1 3 5
2 3 1
2 4 4
3 4 2
output:
0
2
3
5
______________
input:
5 5
1 2 10
1 3 5
3 2 2
3 4 6
4 5 2
output:
0
7
5
11
13
_______________
input:
6 9
1 2 1
1 3 12
2 3 9
2 4 3
3 5 5
4 3 4
4 5 13
4 6 15
5 6 4
output:
0
1
8
4
13
17
"""