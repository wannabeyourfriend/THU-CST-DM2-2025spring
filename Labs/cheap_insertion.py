def cheapest_insertion_algorithm(distance_matrix):
    """
    Implementation of the cheapest insertion algorithm for TSP
    
    Args:
        distance_matrix: Distance matrix
    
    Returns:
        tour: Final tour as a list of node indices
    """
    n = len(distance_matrix) + 1  # Nodes are numbered from 1
    
    # Initialize
    S = list(range(2, n))  # Unprocessed nodes set {2,3,4,5}
    T = [1, 1]  # Initial tour T = (1,1)
    
    # Initialize distance and predecessor arrays
    d = {i: distance_matrix[i-1][0] for i in S}  # d(i) = w(i,1), i ∈ S
    c = {i: 1 for i in S}  # c(i) = 1, i ∈ S
    
    print("Initial tour:", T)
    print("Initial unprocessed nodes:", S)
    print("Initial distance array d:", d)
    print("Initial predecessor array c:", c)
    
    # Main loop: process all nodes until S is empty
    while S:
        # Find node j with minimum d(i) value
        j = min(S, key=lambda i: d[i])
        t = c[j]  # t = c(j)
        
        # Insertion logic
        t_index = T.index(t)
        
        if t == T[0]:  # Special case for first node
            t1, t2 = T[-2], T[1]
            insert_pos = len(T)-1 if w(j, t1, distance_matrix) - w(t, t1, distance_matrix) <= w(j, t2, distance_matrix) - w(t, t2, distance_matrix) else 1
            T.insert(insert_pos, j)
        else:
            t1, t2 = T[t_index - 1], T[t_index + 1]  # Left and right neighbors
            insert_pos = t_index if w(j, t1, distance_matrix) - w(t, t1, distance_matrix) <= w(j, t2, distance_matrix) - w(t, t2, distance_matrix) else t_index + 1
            T.insert(insert_pos, j)
        
        # Remove j from unprocessed set and dictionaries
        S.remove(j)
        del d[j], c[j]
        
        if not S:
            break
        
        # Update d and c values for remaining unprocessed nodes
        for i in S:
            if w(i, j, distance_matrix) < d[i]:
                d[i] = w(i, j, distance_matrix)
                c[i] = j
                
        print(f"Current unprocessed nodes: {S}")
        print(f"Added node {j}, current tour: {T}")
        print(f"Updated distance array d: {d}")
        print(f"Updated predecessor array c: {c}")
    
    return T

def w(i, j, distance_matrix):
    """Return the distance between nodes i and j"""
    return distance_matrix[i-1][j-1]  # Adjust indices to match 1~5 node numbering

def calculate_tour_length(distance_matrix, tour):
    """Calculate the total tour length"""
    return sum(distance_matrix[tour[i]-1][tour[i+1]-1] for i in range(len(tour) - 1))

# Main function
if __name__ == "__main__":
    # Distance matrix (indices 0~4 correspond to nodes 1~5)
    distance_matrix = [
        [0, 42, 33, 52, 29, 45],
        [42, 0, 26, 38, 49, 36],
        [33, 26, 0, 34, 27, 43],
        [52, 38, 34, 0, 35, 30],
        [29, 49, 27, 35, 0, 41],
        [45, 36, 43, 30, 41, 0]
    ]
    
    print("Distance matrix:")
    for row in distance_matrix:
        print(row)
    
    print("\nStarting cheapest insertion algorithm...")
    final_tour = cheapest_insertion_algorithm(distance_matrix)
    
    # Calculate final tour length
    tour_length = calculate_tour_length(distance_matrix, final_tour)
    print(f"\nFinal tour: {final_tour}")
    print(f"Tour length: {tour_length}")
    
    # Print detailed path
    print("\nDetailed path:")
    print(" -> ".join(str(node) for node in final_tour))