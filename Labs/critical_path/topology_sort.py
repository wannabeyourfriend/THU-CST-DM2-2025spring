# 实现拓扑排序

def topology_sort(graph):
    """
    对有向无环图进行拓扑排序
    
    参数:
    graph: 邻接表表示的图,格式为 {u: [v1, v2, ...]},表示从u到v1, v2, ...的边
    
    返回:
    sorted_vertices: 拓扑排序后的顶点列表,如果图中有环则返回None
    """
    # 计算每个顶点的入度
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    
    # 将所有入度为0的顶点加入队列
    queue = [u for u in graph if in_degree[u] == 0]
    
    # 存储拓扑排序结果
    sorted_vertices = []
    
    # BFS遍历
    while queue:
        # 取出一个入度为0的顶点
        u = queue.pop(0)
        sorted_vertices.append(u)
        
        # 将所有u指向的顶点的入度减1
        for v in graph[u]:
            in_degree[v] -= 1
            # 如果入度变为0,则加入队列
            if in_degree[v] == 0:
                queue.append(v)
    
    # 如果不是所有顶点都被访问,说明图中有环
    if len(sorted_vertices) != len(graph):
        return None
    
    return sorted_vertices

def main():
    # 读取输入
    n, m = map(int, input().split())  # n个顶点,m条边
    
    # 初始化图 - 修改为从0开始的顶点编号
    graph = {i: [] for i in range(1, n+1 )}
    
    # 读取边
    for _ in range(m):
        u, v = map(int, input().split())  # 从u到v的边
        graph[u].append(v)
    
    # 进行拓扑排序
    result = topology_sort(graph)
    
    # 输出结果
    if result is None:
        print("图中存在环,无法进行拓扑排序")
    else:
        # 将结果格式化为数学符号形式
        path = " \\to ".join(f"v_{{{str(v)}}}" for v in result)
        print(path)

if __name__ == "__main__":
    main()
    
## test case
    """
    vertex: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    edge:
    0 3
    0 7
    1 9
    2 1
    3 8
    4 5 
    4 6
    5 8
    6 1
    7 2
    7 4
    8 9
    9 10
    """