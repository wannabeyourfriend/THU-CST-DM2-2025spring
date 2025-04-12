#include <iostream>
#include <vector>
#include <queue>
#include <limits>
using namespace std;

struct Edge {
    int destination;
    int weight;
    Edge(int d, int w) : destination(d), weight(w) {}
};

class PathFinder {
private:
    using DistanceType = long long;  
    const DistanceType INF = numeric_limits<DistanceType>::max();
    
    int vertex_count;
    vector<vector<Edge>> connections;  

    vector<DistanceType> calculateShortestPaths(int source) {
        vector<DistanceType> distances(vertex_count + 1, INF);
        using QueueElement = pair<DistanceType, int>;
        // 建堆
        priority_queue<QueueElement, vector<QueueElement>, greater<QueueElement>> distance_queue;
        
        distances[source] = 0;
        distance_queue.push({0, source});

        while (!distance_queue.empty()) {
            auto [current_dist, current_vertex] = distance_queue.top();
            distance_queue.pop();

            if (current_dist > distances[current_vertex]) {
                continue;
            }

            for (const Edge& edge : connections[current_vertex]) {
                DistanceType new_distance = distances[current_vertex] + edge.weight;
                if (new_distance < distances[edge.destination]) {
                    distances[edge.destination] = new_distance;
                    distance_queue.push({new_distance, edge.destination});
                }
            }
        }
        return distances;
    }

public:
    explicit PathFinder(int size) : vertex_count(size) {
        connections.resize(size + 1);
    }

    void connectVertices(int from, int to, int weight) {
        connections[from].emplace_back(to, weight);
        connections[to].emplace_back(from, weight);
    }

    DistanceType findOptimalPath() {
        auto forward_distances = calculateShortestPaths(1);
        auto backward_distances = calculateShortestPaths(vertex_count);

        if (forward_distances[vertex_count] == INF) {
            return -1;
        }

        DistanceType optimal_distance = forward_distances[vertex_count];

        for (int vertex = 1; vertex <= vertex_count; ++vertex) {
            for (const Edge& edge : connections[vertex]) {
                if (forward_distances[vertex] != INF && 
                    backward_distances[edge.destination] != INF) {
                    optimal_distance = min(
                        optimal_distance,
                        forward_distances[vertex] + backward_distances[edge.destination]
                    );
                }
            }
        }

        return optimal_distance;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;

    PathFinder solver(vertex_count);

    for (int i = 0; i < edge_count; ++i) {
        int from, to, weight;
        cin >> from >> to >> weight;
        solver.connectVertices(from, to, weight);
    }

    cout << solver.findOptimalPath() << endl;
    return 0;
}

