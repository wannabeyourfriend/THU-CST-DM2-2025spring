#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>  
struct Edge {
    int u, v, weight;
    Edge(int _u, int _v, int _w) : u(_u), v(_v), weight(_w) {}
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};
class DSU {
public:
    std::vector<int> parent;
    std::vector<int> sz; // Stores the size of the component rooted at i
    DSU(int n_vertices) {
        parent.resize(n_vertices + 1);
        sz.assign(n_vertices + 1, 1); // Each component initially has size 1
        for (int i = 1; i <= n_vertices; ++i) {
            parent[i] = i;
        }
    }
    int find(int i) {
        if (parent[i] == i)
            return i;
        return parent[i] = find(parent[i]);
    }
    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);

        if (root_i != root_j) {
            if (sz[root_i] < sz[root_j])
                std::swap(root_i, root_j); // Ensure root_i is the larger tree
            parent[root_j] = root_i; // Make root_i the parent of root_j
            sz[root_i] += sz[root_j]; // Update the size of the new combined set
            return true; 
        }
        return false;
    }
};

class Graph {
public:
    int num_vertices;
    std::vector<Edge> edges;
    Graph(int n) : num_vertices(n) {}
    void add_edge(int u, int v, int weight) {
        edges.emplace_back(u, v, weight);
    }
    long long kruskal_mst() {
        std::sort(edges.begin(), edges.end());
        DSU dsu(num_vertices);
        long long mst_weight = 0; // Total weight of the MST
        int edges_in_mst = 0;     // Number of edges added to the MST
        for (const auto& edge : edges) {
            if (dsu.unite(edge.u, edge.v)) {
                mst_weight += edge.weight; // Add edge weight to MST total
                edges_in_mst++;            // Increment count of edges in MST
                if (edges_in_mst == num_vertices - 1) {
                    break;
                }
            }
        }

        if (num_vertices == 1) { // A single vertex graph
            return 0; // MST weight is 0, 0 edges
        }
        
        if (edges_in_mst < num_vertices - 1) {
            return -1; // Graph is not connected
        }

        return mst_weight; // Return the total weight of the MST
    }
};

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    int n, m; 
    std::cin >> n >> m;

    Graph g(n);
    for (int i = 0; i < m; ++i) {
        int u, v, w; // u, v: vertices, w: weight
        std::cin >> u >> v >> w;
        g.add_edge(u, v, w);
    }
    long long result = g.kruskal_mst();
    std::cout << result << std::endl;

    return 0;
}