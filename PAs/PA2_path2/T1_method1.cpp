#include <iostream>
#include <vector>
#include <queue>
#include <limits>
using namespace std;

struct StateNode {
    int vertex;     // 原图中的顶点编号
    bool state;     // 0表示未使用免费边，1表示已使用免费边
    
    StateNode(int v, bool s) : vertex(v), state(s) {}
    
    // 用于在map或set中比较节点
    bool operator<(const StateNode& other) const {
        if (vertex != other.vertex) return vertex < other.vertex;
        return state < other.state;
    }
};

class StateGraphSolver {
private:
    using Distance = long long;
    const Distance INF = numeric_limits<Distance>::max();
    
    int vertex_count;
    // 邻接表：[vertex][state] -> vector<{next_node, cost}>
    vector<vector<vector<pair<StateNode, int>>>> state_graph;

    void buildStateGraph(const vector<tuple<int, int, int>>& edges) {
        state_graph.resize(vertex_count + 1, vector<vector<pair<StateNode, int>>>(2));
        
        for (const auto& [u, v, w] : edges) {
            state_graph[u][0].emplace_back(StateNode(v, 0), w);
            state_graph[v][0].emplace_back(StateNode(u, 0), w);
            
            state_graph[u][1].emplace_back(StateNode(v, 1), w);
            state_graph[v][1].emplace_back(StateNode(u, 1), w);
            
            state_graph[u][0].emplace_back(StateNode(v, 1), 0);
            state_graph[v][0].emplace_back(StateNode(u, 1), 0);
        }
    }

    Distance dijkstraOnStateGraph() {
        vector<vector<Distance>> dist(vertex_count + 1, vector<Distance>(2, INF));
        using QueueElement = pair<Distance, StateNode>;
        priority_queue<QueueElement, vector<QueueElement>, greater<QueueElement>> pq;
        
        dist[1][0] = 0;
        pq.push({0, StateNode(1, 0)});
        
        while (!pq.empty()) {
            auto [current_dist, current_node] = pq.top();
            pq.pop();
            
            if (current_dist > dist[current_node.vertex][current_node.state]) 
                continue;
            
            for (const auto& [next_node, cost] : state_graph[current_node.vertex][current_node.state]) {
                Distance new_dist = current_dist + cost;
                
                if (new_dist < dist[next_node.vertex][next_node.state]) {
                    dist[next_node.vertex][next_node.state] = new_dist;
                    pq.push({new_dist, next_node});
                }
            }
        }
        
        return min(dist[vertex_count][0], dist[vertex_count][1]);
    }

public:
    explicit StateGraphSolver(int n) : vertex_count(n) {}
    
    Distance solve(const vector<tuple<int, int, int>>& edges) {
        buildStateGraph(edges);
        Distance result = dijkstraOnStateGraph();
        return result == INF ? -1 : result;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m;
    cin >> n >> m;
    
    vector<tuple<int, int, int>> edges;
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.emplace_back(u, v, w);
    }
    
    StateGraphSolver solver(n);
    cout << solver.solve(edges) << endl;
    
    return 0;
}