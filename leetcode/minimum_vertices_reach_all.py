# LeetCode 1557: Minimum Number of Vertices to Reach All Nodes
#%%
"""
Problem Statement:
------------------
Given a directed acyclic graph (DAG) with n vertices labeled from 0 to n-1, and 
a list of directed edges, find the smallest set of vertices from which all nodes 
in the graph are reachable.

It's guaranteed that a unique solution exists.

Example 1:
Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
Output: [0,3]
Explanation: 
- From vertex 0, we can reach nodes [0,1,2,5]
- From vertex 3, we can reach nodes [3,4,2,5]
- Therefore, the smallest set of vertices is [0,3]

Example 2:
Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
Output: [0,2,3]
Explanation: 
- Vertices 0, 2, and 3 have no incoming edges
- They cannot be reached from any other node
- To ensure all nodes are reachable, we must include these vertices

KEY INSIGHT:
-----------
In a directed graph, nodes with NO incoming edges (in-degree = 0) are called 
"source" nodes. These nodes cannot be reached from any other node, so they MUST 
be in our starting set.

Why this works:
1. If a node has in-degree > 0: it can be reached from another node
2. If a node has in-degree = 0: it CANNOT be reached from any other node
3. Therefore: we must include ALL nodes with in-degree 0
4. Sufficiency: from these source nodes, we can reach all other nodes via DFS/BFS

APPROACH:
---------
1. Count in-degree for each vertex (number of incoming edges)
2. Return all vertices with in-degree = 0

TIME COMPLEXITY: O(V + E) where V = vertices, E = edges
- O(E) to count in-degrees by iterating through edges
- O(V) to collect vertices with in-degree 0

SPACE COMPLEXITY: O(V) for the in-degree array

INTERVIEW TIPS:
--------------
1. Key insight: Only need to find source nodes (in-degree = 0)
2. No need for DFS/BFS - simple counting is sufficient!
3. Edge cases:
   - Disconnected components: each needs at least one source
   - Self-loops: edge from i to i (doesn't affect in-degree count)
   - Multiple edges: count all incoming edges
   - Isolated nodes: have in-degree 0, must be included
4. Common mistake: Trying to use DFS/BFS (unnecessary complexity)
5. Why DAG matters: In a DAG, there's always at least one source node
"""

from typing import List

class Solution:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find the smallest set of vertices from which all nodes are reachable.
        
        Strategy:
        - Count in-degree for each vertex
        - Return all vertices with in-degree 0 (source nodes)
        
        Args:
            n: Number of vertices (labeled 0 to n-1)
            edges: List of [from, to] directed edges
            
        Returns:
            List of source vertices (nodes with in-degree 0)
        """
        # Initialize in-degree array (count of incoming edges for each vertex)
        in_degree = [0] * n
        
        # Count incoming edges for each vertex
        # For edge [from, to], 'to' receives an incoming edge
        for from_node, to_node in edges:
            in_degree[to_node] += 1
        
        # Return all vertices with in-degree 0 (source nodes)
        # These are the vertices that cannot be reached from any other node
        return [i for i in range(n) if in_degree[i] == 0]

#%% TEST CASES WITH EXPLANATIONS

def test_basic_cases():
    """Test basic cases from examples"""
    print("=" * 70)
    print("TEST 1: Basic Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Example 1
    n = 6
    edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    expected = {0, 3}
    
    print(f"\n1. n = {n}, edges = {edges}")
    print(f"   Expected: {expected}")
    print(f"   Got: {result_set}")
    print(f"   Explanation:")
    print(f"   - Node 0: in-degree 0 (source) → can reach [0,1,2,5]")
    print(f"   - Node 1: in-degree 1 (from 0)")
    print(f"   - Node 2: in-degree 2 (from 0,4)")
    print(f"   - Node 3: in-degree 0 (source) → can reach [3,4,2,5]")
    print(f"   - Node 4: in-degree 1 (from 3)")
    print(f"   - Node 5: in-degree 1 (from 2)")
    print(f"   ✓ Sources: {result_set}")
    
    # Test 2: Example 2
    n = 5
    edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    expected = {0, 2, 3}
    
    print(f"\n2. n = {n}, edges = {edges}")
    print(f"   Expected: {expected}")
    print(f"   Got: {result_set}")
    print(f"   Explanation:")
    print(f"   - Node 0: in-degree 0 (source)")
    print(f"   - Node 1: in-degree 3 (from 0,2,3)")
    print(f"   - Node 2: in-degree 0 (source)")
    print(f"   - Node 3: in-degree 0 (source)")
    print(f"   - Node 4: in-degree 2 (from 1,2)")
    print(f"   ✓ Sources: {result_set}")

def test_edge_cases():
    """Test edge cases: single node, chain, isolated nodes"""
    print("\n" + "=" * 70)
    print("TEST 2: Edge Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Single node (no edges)
    n = 1
    edges = []
    result = sol.findSmallestSetOfVertices(n, edges)
    print(f"\n1. n = {n}, edges = {edges}")
    print(f"   Result: {result}")
    print(f"   Explanation: Single node with no edges, in-degree 0 → must include it")
    assert result == [0], f"Expected [0], got {result}"
    
    # Test 2: Chain (0->1->2->3)
    n = 4
    edges = [[0,1],[1,2],[2,3]]
    result = sol.findSmallestSetOfVertices(n, edges)
    print(f"\n2. n = {n}, edges = {edges} (chain)")
    print(f"   Result: {result}")
    print(f"   Explanation: Only node 0 has in-degree 0, can reach all others")
    assert result == [0], f"Expected [0], got {result}"
    
    # Test 3: All isolated nodes (no edges)
    n = 3
    edges = []
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    print(f"\n3. n = {n}, edges = {edges} (all isolated)")
    print(f"   Result: {result_set}")
    print(f"   Explanation: All nodes have in-degree 0, must include all")
    assert result_set == {0, 1, 2}, f"Expected all nodes, got {result_set}"
    
    # Test 4: Star pattern (all point to center)
    n = 4
    edges = [[0,3],[1,3],[2,3]]
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    expected = {0, 1, 2}
    print(f"\n4. n = {n}, edges = {edges} (star pattern)")
    print(f"   Result: {result_set}")
    print(f"   Explanation: Nodes 0,1,2 are sources, node 3 has in-degree 3")
    assert result_set == expected, f"Expected {expected}, got {result_set}"

def test_complex_cases():
    """Test more complex graph structures"""
    print("\n" + "=" * 70)
    print("TEST 3: Complex Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Two disconnected components
    n = 5
    edges = [[0,1],[3,4]]
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    expected = {0, 2, 3}
    print(f"\n1. n = {n}, edges = {edges} (two components)")
    print(f"   Result: {result_set}")
    print(f"   Explanation:")
    print(f"   - Component 1: 0->1 (source: 0)")
    print(f"   - Component 2: 3->4 (source: 3)")
    print(f"   - Isolated: node 2 (source: 2)")
    print(f"   ✓ Sources: {result_set}")
    assert result_set == expected, f"Expected {expected}, got {result_set}"
    
    # Test 2: Diamond pattern
    n = 4
    edges = [[0,1],[0,2],[1,3],[2,3]]
    result = sol.findSmallestSetOfVertices(n, edges)
    print(f"\n2. n = {n}, edges = {edges} (diamond)")
    print(f"   Result: {result}")
    print(f"   Explanation: Only node 0 has in-degree 0, can reach all")
    assert result == [0], f"Expected [0], got {result}"
    
    # Test 3: Multiple sources pointing to same target
    n = 4
    edges = [[0,3],[1,3],[2,3]]
    result = sol.findSmallestSetOfVertices(n, edges)
    result_set = set(result)
    expected = {0, 1, 2}
    print(f"\n3. n = {n}, edges = {edges}")
    print(f"   Result: {result_set}")
    print(f"   Explanation: Nodes 0,1,2 are sources, node 3 has in-degree 3")
    assert result_set == expected, f"Expected {expected}, got {result_set}"

def visualize_graph(n: int, edges: List[List[int]], sources: List[int]):
    """Helper function to visualize the graph structure"""
    print(f"\nGraph Visualization:")
    print(f"  Nodes: {list(range(n))}")
    print(f"  Edges: {edges}")
    print(f"  In-degrees:")
    
    in_degree = [0] * n
    for from_node, to_node in edges:
        in_degree[to_node] += 1
    
    for i in range(n):
        status = " (SOURCE)" if i in sources else ""
        print(f"    Node {i}: in-degree = {in_degree[i]}{status}")
    
    print(f"  Sources (must include): {sources}")

# Run all tests
if __name__ == "__main__":
    test_basic_cases()
    test_edge_cases()
    test_complex_cases()
    
    # Visualize example
    print("\n" + "=" * 70)
    print("VISUALIZATION")
    print("=" * 70)
    sol = Solution()
    n, edges = 6, [[0,1],[0,2],[2,5],[3,4],[4,2]]
    result = sol.findSmallestSetOfVertices(n, edges)
    visualize_graph(n, edges, result)

# %%

