# Minimum Vertices to Traverse Directed Graph
#%%
"""
Problem Statement:
Given a directed acyclic graph (DAG) with n nodes labeled from 0 to n-1, and
a list of directed edges, find the smallest set of vertices from which all
nodes in the graph are reachable.

Return the list of vertices in any order.

Example 1:
Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
Output: [0,3]
Explanation:
- From node 0, you can reach nodes [1,2,5]
- From node 3, you can reach nodes [4,2,5]
- So {0,3} is enough to reach every node.

Example 2:
Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
Output: [0,2,3]
Explanation: Nodes 0, 2, 3 have no incoming edges.

INTERVIEW EXPLANATION: Why In-Degree Approach?

1. **Problem Structure**: In a directed graph, to reach all nodes, we need to
   start from nodes that have no incoming edges (sources). Any node with an
   incoming edge can be reached from its predecessor.

2. **Why In-Degree Approach?**
   - **Key Insight**: Nodes with in-degree 0 are "source" nodes - they cannot
     be reached from any other node, so they must be in our starting set.
   
   - **Algorithm**:
     * Count in-degree for each node
     * Return all nodes with in-degree == 0
   
   - **Time Complexity**: O(V + E) where V = vertices, E = edges
     * Single pass through edges to count in-degrees
     * Single pass through nodes to collect sources
   
   - **Space Complexity**: O(V) for in-degree array

3. **Why This Works**:
   - If a node has in-degree > 0, it can be reached from another node
   - If a node has in-degree == 0, it cannot be reached from any other node
   - Therefore, we must include all in-degree-0 nodes
   - These are sufficient because from them we can reach all other nodes

4. **Edge Cases**:
   - Disconnected components: Each component needs at least one source
   - Self-loops: Don't affect in-degree (edge from i to i)
   - Multiple edges: Count all incoming edges
"""

from typing import List


class Solution:
    """Solution for Minimum Vertices to Traverse Graph"""
    
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find smallest set of vertices to reach all nodes.
        
        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [from, to] directed edges
            
        Returns:
            List of source vertices (nodes with in-degree 0)
        """
        # Count in-degree for each node
        in_degree = [0] * n
        
        for from_node, to_node in edges:
            in_degree[to_node] += 1
        
        # Return all nodes with in-degree 0
        return [i for i in range(n) if in_degree[i] == 0]


def test_minimum_vertices():
    """Test cases for Minimum Vertices to Traverse Graph"""
    sol = Solution()
    
    # Test case 1: Example 1
    n1, edges1 = 6, [[0,1],[0,2],[2,5],[3,4],[4,2]]
    result1 = sol.findSmallestSetOfVertices(n1, edges1)
    result1_set = set(result1)
    expected1_set = {0, 3}
    assert result1_set == expected1_set, f"Expected {expected1_set}, got {result1_set}"
    print(f"✓ Test 1: {result1}")
    
    # Test case 2: Example 2
    n2, edges2 = 5, [[0,1],[2,1],[3,1],[1,4],[2,4]]
    result2 = sol.findSmallestSetOfVertices(n2, edges2)
    result2_set = set(result2)
    expected2_set = {0, 2, 3}
    assert result2_set == expected2_set, f"Expected {expected2_set}, got {result2_set}"
    print(f"✓ Test 2: {result2}")
    
    # Test case 3: Single node
    n3, edges3 = 1, []
    result3 = sol.findSmallestSetOfVertices(n3, edges3)
    assert result3 == [0], f"Expected [0], got {result3}"
    print(f"✓ Test 3: {result3}")
    
    # Test case 4: Chain (0->1->2->3)
    n4, edges4 = 4, [[0,1],[1,2],[2,3]]
    result4 = sol.findSmallestSetOfVertices(n4, edges4)
    assert result4 == [0], f"Expected [0], got {result4}"
    print(f"✓ Test 4: {result4}")
    
    # Test case 5: All isolated (no edges)
    n5, edges5 = 3, []
    result5 = sol.findSmallestSetOfVertices(n5, edges5)
    result5_set = set(result5)
    assert result5_set == {0, 1, 2}, f"Expected all nodes, got {result5_set}"
    print(f"✓ Test 5: {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_minimum_vertices()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    n, edges = 6, [[0,1],[0,2],[2,5],[3,4],[4,2]]
    result = sol.findSmallestSetOfVertices(n, edges)
    print(f"Graph: {n} nodes, edges: {edges}")
    print(f"Minimum vertices to reach all: {result}")
    print("Explanation: Nodes 0 and 3 have no incoming edges")
# %%

