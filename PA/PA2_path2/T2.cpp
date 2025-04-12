#include <iostream>
#include <vector>
#include <queue>
#include <memory>
#include <algorithm>
using namespace std;

// 前向声明
class DirectedGraph;
class GraphProcessor;

// 图的边结构
struct DirectedEdge {
    int source;
    int target;
    DirectedEdge(int s, int t) : source(s), target(t) {}
};

// 图节点类
class GraphNode {
private:
    int identifier;
    vector<int> outbound_connections;
    int dependency_count;

public:
    explicit GraphNode(int id) : identifier(id), dependency_count(0) {}
    
    void addOutboundConnection(int target) {
        outbound_connections.push_back(target);
    }
    
    void incrementDependencies() { ++dependency_count; }
    void decrementDependencies() { --dependency_count; }
    bool isIndependent() const { return dependency_count == 0; }
    int getId() const { return identifier; }
    const vector<int>& getConnections() const { return outbound_connections; }
};

// 有向图类
class DirectedGraph {
private:
    vector<unique_ptr<GraphNode>> nodes;
    int node_count;

    bool isValidNode(int id) const {
        return id >= 1 && id <= node_count;
    }

public:
    explicit DirectedGraph(int size) : node_count(size) {
        nodes.resize(size + 1);
        for (int i = 1; i <= size; ++i) {
            nodes[i] = make_unique<GraphNode>(i);
        }
    }

    void establishConnection(const DirectedEdge& edge) {
        if (!isValidNode(edge.source) || !isValidNode(edge.target)) return;
        
        nodes[edge.source]->addOutboundConnection(edge.target);
        nodes[edge.target]->incrementDependencies();
    }

    friend class GraphProcessor;
};

// 图处理器类
class GraphProcessor {
private:
    const DirectedGraph& graph;
    vector<int> processing_sequence;

    void initializeProcessing() {
        queue<int> independent_nodes;
        
        // 查找初始的独立节点
        for (int i = 1; i <= graph.node_count; ++i) {
            if (graph.nodes[i]->isIndependent()) {
                independent_nodes.push(i);
            }
        }

        processNodes(independent_nodes);
    }

    void processNodes(queue<int>& node_queue) {
        vector<unique_ptr<GraphNode>> node_copies;
        node_copies.reserve(graph.node_count + 1);
        
        // 创建节点副本
        for (int i = 0; i <= graph.node_count; ++i) {
            if (i == 0) {
                node_copies.push_back(nullptr);
                continue;
            }
            auto node = make_unique<GraphNode>(i);
            *node = *graph.nodes[i];
            node_copies.push_back(move(node));
        }

        while (!node_queue.empty()) {
            int current = node_queue.front();
            node_queue.pop();
            processing_sequence.push_back(current);

            for (int next : node_copies[current]->getConnections()) {
                node_copies[next]->decrementDependencies();
                if (node_copies[next]->isIndependent()) {
                    node_queue.push(next);
                }
            }
        }
    }

public:
    explicit GraphProcessor(const DirectedGraph& g) : graph(g) {}

    vector<int> generateSequence() {
        processing_sequence.clear();
        initializeProcessing();
        
        return (processing_sequence.size() == graph.node_count) ? 
               processing_sequence : vector<int>();
    }
};

// 结果格式化器
class ResultFormatter {
public:
    static string format(const vector<int>& sequence) {
        if (sequence.empty()) return "-1";
        
        string result;
        for (size_t i = 0; i < sequence.size(); ++i) {
            result += to_string(sequence[i]);
            if (i < sequence.size() - 1) result += " ";
        }
        return result;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;

    DirectedGraph graph(vertex_count);
    
    for (int i = 0; i < edge_count; ++i) {
        int from, to;
        cin >> from >> to;
        graph.establishConnection(DirectedEdge(from, to));
    }

    GraphProcessor processor(graph);
    vector<int> sequence = processor.generateSequence();
    
    cout << ResultFormatter::format(sequence) << endl;

    return 0;
}