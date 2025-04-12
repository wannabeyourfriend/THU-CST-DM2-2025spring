# 实现PERT图
import networkx as nx
import matplotlib.pyplot as plt

class PERT:
    def __init__(self, process_table):
        # 初始化图结构 - 在PERT图中，边表示工序，节点表示工序之间的关系
        self.G = nx.DiGraph()
        self.process_table = process_table
        
        # 创建节点映射 - 用于跟踪每个工序的起点和终点节点
        self.process_nodes = {}
        
        # 首先找出所有工序的前驱和后继关系
        successors = {}
        for process, info in process_table.items():
            predecessors = info.get('predecessors', [])
            for pred in predecessors:
                if pred not in successors:
                    successors[pred] = []
                successors[pred].append(process)
        
        # 创建节点和边
        node_id = 1  # 节点ID从1开始
        
        # 创建一个公共起始节点
        start_node = f"v{node_id}"
        self.G.add_node(start_node, label="start")
        node_id += 1
        
        # 使用拓扑排序确保按正确顺序处理工序
        processed = set()
        while len(processed) < len(process_table):
            # 找出所有可以处理的工序（前驱都已处理）
            available = []
            for process, info in process_table.items():
                if process in processed:
                    continue
                predecessors = info.get('predecessors', [])
                if not predecessors or all(pred in processed for pred in predecessors):
                    available.append(process)
            
            # 处理可用的工序
            for process in available:
                info = process_table[process]
                predecessors = info.get('predecessors', [])
                
                # 创建该工序的终点节点
                end_node = f"v{node_id}"
                self.G.add_node(end_node, label=f"{process}")
                node_id += 1
                
                if not predecessors:
                    # 如果没有前驱，从起始节点连接
                    self.G.add_edge(start_node, end_node,
                                  process=process,
                                  duration=info['duration'],
                                  label=f"{process}({info['duration']})")
                    self.process_nodes[process] = (start_node, end_node)
                else:
                    # 从每个前驱工序的终点连接到该工序
                    for pred in predecessors:
                        pred_end_node = self.process_nodes[pred][1]  # 前驱工序的终点
                        self.G.add_edge(pred_end_node, end_node,
                                      process=process,
                                      duration=info['duration'],
                                      label=f"{process}({info['duration']})")
                    self.process_nodes[process] = (None, end_node)  # 起点设为None表示有多个
                
                processed.add(process)
        
        # 计算最早开始时间和最晚开始时间
        self.calculate_times()
    
    def calculate_times(self):
        # 拓扑排序
        topo_order = list(nx.topological_sort(self.G))
        
        # 初始化最早完成时间
        earliest_completion = {node: 0 for node in self.G.nodes()}
        
        # 计算最早完成时间（正向）
        for node in topo_order:
            predecessors = list(self.G.predecessors(node))
            if predecessors:
                for pred in predecessors:
                    edge_data = self.G.get_edge_data(pred, node)
                    if edge_data:
                        duration = edge_data.get('duration', 0)
                        earliest_completion[node] = max(
                            earliest_completion[node],
                            earliest_completion[pred] + duration
                        )
        
        # 找到终点节点
        end_nodes = [node for node in self.G.nodes() if self.G.out_degree(node) == 0]
        
        # 计算项目完成时间
        completion_time = max(earliest_completion[node] for node in end_nodes) if end_nodes else 0
        
        # 初始化最晚完成时间
        latest_completion = {node: completion_time for node in self.G.nodes()}
        
        # 计算最晚完成时间（反向）
        for node in reversed(topo_order):
            successors = list(self.G.successors(node))
            if successors:
                latest_completion[node] = min(
                    latest_completion[succ] - self.G.get_edge_data(node, succ)['duration']
                    for succ in successors
                )
        
        # 计算时间余量
        slack = {node: latest_completion[node] - earliest_completion[node] for node in self.G.nodes()}
        
        # 存储计算结果
        self.earliest_completion = earliest_completion
        self.latest_completion = latest_completion
        self.slack = slack
        self.completion_time = completion_time
        
        # 找出关键路径上的节点和边
        self.critical_nodes = [node for node, s in slack.items() if s == 0]
        self.critical_edges = []
        
        for u, v, data in self.G.edges(data=True):
            if (u in self.critical_nodes and v in self.critical_nodes and
                self.earliest_completion[u] + data['duration'] == self.earliest_completion[v]):
                self.critical_edges.append((u, v))
    
    def draw(self):
        # 创建布局
        pos = nx.planar_layout(self.G)
        
        # 绘制节点
        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=500)
        
        # # 高亮关键路径上的节点
        # nx.draw_networkx_nodes(self.G, pos, 
        #                       nodelist=self.critical_nodes,
        #                       node_color='red', 
        #                       node_size=500)
        
        # 绘制边
        nx.draw_networkx_edges(self.G, pos, arrows=True, width=1.0)
        
        # # 高亮关键路径上的边
        # nx.draw_networkx_edges(self.G, pos, 
        #                       edgelist=self.critical_edges,
        #                       edge_color='red', 
        #                       width=2.0,
        #                       arrows=True)
        
        # 添加节点标签
        labels = {node: self.G.nodes[node].get('label', node) for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=8)
        
        # 添加边标签
        edge_labels = {(u, v): data['label'] for u, v, data in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8)
        
        # # 设置图形大小
        # plt.figure(figsize=(12, 8))
        # plt.title("PERT图 (边表示工序，节点表示工序之间的关系)")
        # plt.axis('off')
        # plt.show()
    
    def critical_path(self):
        # 找出关键路径
        critical_processes = []
        
        for u, v in self.critical_edges:
            edge_data = self.G.get_edge_data(u, v)
            if 'process' in edge_data:
                critical_processes.append(edge_data['process'])
        
        return {
            'critical_nodes': self.critical_nodes,
            'critical_edges': self.critical_edges,
            'critical_processes': critical_processes,
            'completion_time': self.completion_time
        }
    
    def print_process_table(self):
        """打印工序信息表格"""
        print("=" * 50)
        print(f"{'工序':^10}{'持续时间':^10}{'前驱工序':^20}")
        print("-" * 50)
        
        for process in sorted(self.process_table.keys()):
            info = self.process_table[process]
            duration = info['duration']
            
            # 格式化前驱工序列表
            predecessors = info.get('predecessors', [])
            if not predecessors:
                pred_str = "-"
            else:
                pred_str = ",".join(map(str, predecessors))
            
            print(f"{process:^10}{duration:^10}{pred_str:^20}")
        
        print("=" * 50)
    
    def print_schedule_table(self):
        """打印计划时间表格"""
        print("=" * 70)
        print(f"{'工序':^10}{'最早开始':^12}{'最晚开始':^12}{'时间余量':^12}{'持续时间':^10}")
        print("-" * 70)
        
        # 为每个工序计算最早和最晚开始时间
        for process, info in self.process_table.items():
            # 获取该工序对应的边
            process_edges = []
            for u, v, data in self.G.edges(data=True):
                if data.get('process') == process:
                    process_edges.append((u, v, data))
            
            if process_edges:
                # 取第一条边（应该只有一条）
                u, v, data = process_edges[0]
                
                # 计算最早和最晚开始时间
                earliest_start = self.earliest_completion[u]
                latest_start = self.latest_completion[v] - data['duration']
                slack = latest_start - earliest_start
                
                print(f"{process:^10}{earliest_start:^12}{latest_start:^12}{slack:^12}{data['duration']:^10}")
        
        print("=" * 70)
        print(f"项目完成时间: {self.completion_time}")
        
        # 打印关键路径
        critical_info = self.critical_path()
        print("\n关键路径工序:", critical_info['critical_processes'])