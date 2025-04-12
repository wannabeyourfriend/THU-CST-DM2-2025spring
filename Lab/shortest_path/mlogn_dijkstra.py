# o(mlogn) level Dijkstra algorithm implementation

import heapq

def dijkstra(graph, start):
    """
    使用优先队列优化的Dijkstra算法计算从起点到所有其他顶点的最短路径
    
    参数:
    graph: 邻接表表示的图，格式为 {u: [(v, w), ...]}，表示从u到v的边权为w
    start: 起始顶点
    
    返回:
    dist: 从起点到所有顶点的最短距离字典
    """
    # 初始化距离数组，所有点的距离初始化为无穷大
    dist = {i: float('inf') for i in graph}
    # 起点到自身的距离为0
    dist[start] = 0
    
    # 优先队列，存储(距离, 顶点)对，按距离排序
    pq = [(0, start)]
    
    # 已处理集合
    processed = set()
    
    while pq:
        # 取出当前距离最小的顶点
        current_dist, current_vertex = heapq.heappop(pq)
        
        # 如果该顶点已经处理过，则跳过
        if current_vertex in processed:
            continue
        
        # 将该顶点加入已处理集合
        processed.add(current_vertex)
        
        # 如果取出的距离大于已知距离，则跳过（可能是旧的记录）
        if current_dist > dist[current_vertex]:
            continue
        
        # 更新相邻点的距离
        for neighbor, weight in graph[current_vertex]:
            if current_vertex in processed and neighbor in processed:
                continue
                
            # 计算新的距离
            new_dist = dist[current_vertex] + weight
            
            # 如果找到更短的路径，则更新距离并加入优先队列
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
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