
import matplotlib.pyplot as plt
import networkx as nx

"""工序表
__________________
| 工序 | 耗时 | 前驱工序 |
| 1 | 5 | -    |
| 2 | 8 | 1,3  |
| 3 | 3 | 1    |
| 4 | 6 | 3    |
| 5 | 10| 2,3  |
| 6 | 4 | 2,3  |
| 7 | 8 | 3    |
| 8 | 2 | 6,7  |
| 9 | 4 | 5,8  |
| 10| 5 | 6,7  |
"""
class PT:
    def __init__(self, process_table):
        # 初始化图结构
        self.G = nx.DiGraph()
        self.process_table = process_table
        
        # 添加节点和边
        for process, info in process_table.items():
            self.G.add_node(process, duration=info['duration'])
            
            # 添加前驱工序的边
            if info['predecessors']:
                for pred in info['predecessors']:
                    self.G.add_edge(pred, process)
        
        # 计算最早开始时间和最晚开始时间
        self.calculate_times()
    
    def calculate_times(self):
        print("\n===== Computing Earliest Start Time and Latest Start Time =====")
        
        # 拓扑排序
        topo_order = list(nx.topological_sort(self.G))
        print(f"Topological Order: {' -> '.join(map(str, topo_order))}")
        
        # 初始化最早启动时间
        earliest_start = {node: 0 for node in self.G.nodes()}
        print("\nInitialize ES(i) = 0 for all i:")
        for node, time in earliest_start.items():
            print(f"  ES({node}) = {time}")
        
        # 计算最早启动时间(正向) - ES(j) = max{ES(i) + d(i) | i ∈ Pred(j)}
        print("\nCompute ES(j) = max{ES(i) + d(i) | i ∈ Pred(j)}:")
        for node in topo_order:
            predecessors = list(self.G.predecessors(node))
            if predecessors:
                print(f"  Pred({node}) = {predecessors}")
                pred_times = []
                for pred in predecessors:
                    pred_time = earliest_start[pred] + self.process_table[pred]['duration']
                    pred_times.append((pred, earliest_start[pred], self.process_table[pred]['duration'], pred_time))
                
                earliest_start[node] = max(earliest_start[pred] + self.process_table[pred]['duration'] 
                                          for pred in predecessors)
                
                print(f"  Calculation:")
                for pred, es, dur, total in pred_times:
                    print(f"    ES({node}) ≥ ES({pred}) + d({pred}) = {es} + {dur} = {total}")
                print(f"  ES({node}) = max{{...}} = {earliest_start[node]}")
            else:
                print(f"  Pred({node}) = ∅, ES({node}) = {earliest_start[node]}")
        
        # 计算项目完成时间
        # 找到没有后继节点的节点(终点节点)
        end_nodes = [node for node in self.G.nodes() if self.G.out_degree(node) == 0]
        print(f"\nEnd nodes: {end_nodes}")
        
        completion_times = []
        for node in end_nodes:
            time = earliest_start[node] + self.process_table[node]['duration']
            completion_times.append((node, earliest_start[node], self.process_table[node]['duration'], time))
        
        completion_time = max(earliest_start[node] + self.process_table[node]['duration']
                             for node in end_nodes)
        
        print("Project completion time T = max{ES(i) + d(i) | i ∈ End nodes}:")
        for node, es, dur, total in completion_times:
            print(f"  T ≥ ES({node}) + d({node}) = {es} + {dur} = {total}")
        print(f"T = {completion_time}")
        
        # 初始化最晚启动时间
        latest_start = {node: float('inf') for node in self.G.nodes()}
        for node in end_nodes:
            latest_start[node] = completion_time - self.process_table[node]['duration']
        
        print("\nInitialize LS(i) for end nodes:")
        for node in end_nodes:
            print(f"  LS({node}) = T - d({node}) = {completion_time} - {self.process_table[node]['duration']} = {latest_start[node]}")
        
        # 计算最晚启动时间(反向) - LS(i) = min{LS(j) - d(i) | j ∈ Succ(i)}
        print("\nCompute LS(i) = min{LS(j) - d(i) | j ∈ Succ(i)}:")
        for node in reversed(topo_order):
            successors = list(self.G.successors(node))
            if successors:
                print(f"  Succ({node}) = {successors}")
                succ_times = []
                for succ in successors:
                    succ_time = latest_start[succ] - self.process_table[node]['duration']
                    succ_times.append((succ, latest_start[succ], self.process_table[node]['duration'], succ_time))
                
                latest_start[node] = min(latest_start[succ] - self.process_table[node]['duration']
                                        for succ in successors)
                
                print(f"  Calculation:")
                for succ, ls, dur, total in succ_times:
                    print(f"    LS({node}) ≤ LS({succ}) - d({node}) = {ls} - {dur} = {total}")
                print(f"  LS({node}) = min{{...}} = {latest_start[node]}")
        
        # 计算时间余量(允许延误时间) - S(i) = LS(i) - ES(i)
        slack = {node: latest_start[node] - earliest_start[node] for node in self.G.nodes()}
        
        print("\nCompute Slack S(i) = LS(i) - ES(i):")
        for node in sorted(self.G.nodes()):
            print(f"  S({node}) = LS({node}) - ES({node}) = {latest_start[node]} - {earliest_start[node]} = {slack[node]}")
        
        # 存储计算结果
        self.earliest_start = earliest_start
        self.latest_start = latest_start
        self.slack = slack
        self.completion_time = completion_time
        
        print("\nCritical nodes (S(i) = 0):")
        critical_nodes = [node for node, s in slack.items() if s == 0]
        print(f"  {critical_nodes}")
        print("===== Calculation Complete =====\n")
    
    def draw(self):
        # 创建布局 - 使用spring_layout并调整参数
        # k控制节点间的距离(斥力大小),iterations控制迭代次数以获得更稳定的布局
        # pos = nx.spring_layout(self.G, k=0.5, iterations=100, seed=42)
        
        # 也可以尝试其他布局算法
        # pos = nx.kamada_kawai_layout(self.G)  # 基于能量最小化的布局
        pos = nx.planar_layout(self.G)  # 平面布局
        # pos = nx.shell_layout(self.G)  # 同心圆布局
        # pos = nx.spectral_layout(self.G)  # 基于图拉普拉斯特征向量的布局
        
        # 绘制节点
        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=500)
        
        # 绘制边
        nx.draw_networkx_edges(self.G, pos, arrows=True)
        
        # 添加节点标签
        labels = {node: f"{node}" for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, pos, labels=labels)
        
        # 添加边标签(显示源节点的持续时间作为边的权值)
        edge_labels = {(u, v): self.process_table[u]['duration'] for u, v in self.G.edges()}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        
        # 设置图形大小以获得更好的可视化效果
        plt.figure(figsize=(12, 8))
        
        # # 显示图形
        # plt.title("PT Graph")
        # plt.axis('off')
        # plt.show()
    
    def critical_path(self):
        # 找出关键路径上的节点(时间余量为0的节点)
        critical_nodes = [node for node, slack in self.slack.items() if slack == 0]
        
        # 构建关键路径子图
        critical_subgraph = self.G.subgraph(critical_nodes)
        
        # 找出关键路径
        paths = []
        start_nodes = [node for node in critical_subgraph.nodes() if critical_subgraph.in_degree(node) == 0]
        end_nodes = [node for node in critical_subgraph.nodes() if critical_subgraph.out_degree(node) == 0]
        
        # 计算每条路径的长度
        for start in start_nodes:
            for end in end_nodes:
                try:
                    for path in nx.all_simple_paths(critical_subgraph, start, end):
                        # 计算路径长度
                        path_length = sum(self.process_table[node]['duration'] for node in path[:-1])
                        # 加上最后一个节点到结束的时间
                        path_length += self.process_table[path[-1]]['duration']
                        
                        # 只保留长度等于项目完成时间的路径
                        if path_length == self.completion_time:
                            paths.append(path)
                except nx.NetworkXNoPath:
                    continue
        
        return {
            'critical_nodes': critical_nodes,
            'critical_paths': paths,
            'completion_time': self.completion_time
        }
    
    def delay(self):
        # 计算最大允许延误
        return self.slack
        
    def print_schedule_table(self):
        """以表格形式打印每个节点的最早启动时间,最晚启动时间和允许延误时间"""
        print("=" * 60)
        print(f"{'Process':^10}{'ES(i)':^15}{'LS(i)':^15}{'Slack S(i)':^15}")
        print("-" * 60)
        
        # 按工序编号排序
        for node in sorted(self.G.nodes()):
            p = self.earliest_start[node]
            t = self.latest_start[node]
            slack = self.slack[node]
            print(f"{node:^10}{p:^15}{t:^15}{slack:^15}")
        
        print("=" * 60)
        print(f"Project completion time T = {self.completion_time}")
        
        # 打印关键路径
        critical_info = self.critical_path()
        print("\nCritical nodes:", critical_info['critical_nodes'])
        if critical_info['critical_paths']:
            print("Critical paths:")
            for i, path in enumerate(critical_info['critical_paths']):
                print(f"  Path {i+1}: {' -> '.join(map(str, path))}")
    
    def print_process_table(self):
        """打印工序号,工序时间和前序工序的表格"""
        print("=" * 50)
        print(f"{'Process':^10}{'Duration':^10}{'Predecessors':^20}")
        print("-" * 50)
        
        # 按工序编号排序
        for process in sorted(self.process_table.keys()):
            info = self.process_table[process]
            duration = info['duration']
            predecessors = info['predecessors']
            
            # 格式化前驱工序列表
            if not predecessors:
                pred_str = "-"
            else:
                pred_str = ",".join(map(str, predecessors))
            
            print(f"{process:^10}{duration:^10}{pred_str:^20}")
        
        print("=" * 50)