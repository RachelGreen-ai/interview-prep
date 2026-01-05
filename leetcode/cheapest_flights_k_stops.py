# LeetCode 787: Cheapest Flights Within K Stops
#%%
"""
Problem Statement:
There are n cities connected by some number of flights. You are given an array
flights where flights[i] = [from_i, to_i, price_i] indicates that there is a
flight from city from_i to city to_i with cost price_i.

You are also given three integers src, dst, and k, return the cheapest price
from src to dst with at most k stops. If there is no such route, return -1.

Example 1:
Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
       src = 0, dst = 3, k = 1
Output: 700
Explanation: The optimal path is 0 -> 1 -> 3, which costs 100 + 600 = 700.

Example 2:
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]]
       src = 0, dst = 2, k = 1
Output: 200
Explanation: The optimal path is 0 -> 1 -> 2, which costs 100 + 100 = 200.

INTERVIEW EXPLANATION: Why Modified Dijkstra or Bellman-Ford?

1. **Problem Structure**: We need shortest path with a constraint (at most k stops).
   This is similar to shortest path but with an additional dimension (stops).

2. **Why Modified Dijkstra?**
   - **Key Insight**: Classic Dijkstra finds shortest path without stop limits.
     We modify it to track (cost, city, stops_used) in the priority queue.
   
   - **Algorithm**:
     * Use min-heap: (cost_so_far, current_city, stops_used)
     * Always expand lowest cost first
     * Skip if stops > k
     * Track best cost for (city, stops) combination
   
   - **Time Complexity**: O(E log V) where E = edges, V = vertices
     * Each edge processed at most once per stop level
   
   - **Space Complexity**: O(V × K) for tracking best costs

3. **Alternative: Bellman-Ford DP**
   - **DP State**: dp[i][city] = min cost to reach city using at most i flights
   - **Recurrence**: dp[i][v] = min(dp[i-1][u] + cost) for all edges (u, v)
   - **Time**: O(K × E), **Space**: O(V)
   - More intuitive for interviews, easier to explain

4. **Key Insight**: Unlike standard shortest path, we need to consider paths
   with different numbers of stops. We track state as (city, stops) rather
   than just city.
"""

from typing import List
from collections import defaultdict
import heapq


class Solution:
    """Solution for Cheapest Flights Within K Stops"""
    
    def findCheapestPrice_dijkstra(self, n: int, flights: List[List[int]], 
                                   src: int, dst: int, k: int) -> int:
        """
        Solution using modified Dijkstra's algorithm.
        
        Args:
            n: Number of cities
            flights: List of [from, to, price]
            src: Source city
            dst: Destination city
            k: Maximum number of stops allowed
            
        Returns:
            Cheapest price, or -1 if no route exists
        """
        # Build graph
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))
        
        # Min-heap: (cost_so_far, current_city, stops_used)
        heap = [(0, src, 0)]
        # Track best cost for (city, stops) combination
        best = {}
        
        while heap:
            cost, city, stops = heapq.heappop(heap)
            
            # Found destination
            if city == dst:
                return cost
            
            # Too many stops
            if stops > k:
                continue
            
            # Skip if we already have a better path to this (city, stops)
            if (city, stops) in best and best[(city, stops)] < cost:
                continue
            
            # Record best cost for (city, stops)
            best[(city, stops)] = cost
            
            # Explore neighbors
            for neighbor, price in graph[city]:
                new_cost = cost + price
                heapq.heappush(heap, (new_cost, neighbor, stops + 1))
        
        return -1
    
    def findCheapestPrice_bellman_ford(self, n: int, flights: List[List[int]], 
                                       src: int, dst: int, k: int) -> int:
        """
        Solution using Bellman-Ford DP approach (more interview-friendly).
        
        Args:
            n: Number of cities
            flights: List of [from, to, price]
            src: Source city
            dst: Destination city
            k: Maximum number of stops allowed
            
        Returns:
            Cheapest price, or -1 if no route exists
        """
        # Initialize: dp[i][city] = min cost to reach city using at most i flights
        # We only need previous iteration, so use two arrays
        prev = [float('inf')] * n
        prev[src] = 0
        
        # Relax edges (k+1) times (k stops = k+1 flights)
        for _ in range(k + 1):
            curr = prev[:]  # Copy previous iteration
            
            # Relax all edges
            for u, v, w in flights:
                if prev[u] != float('inf'):
                    curr[v] = min(curr[v], prev[u] + w)
            
            prev = curr
        
        return -1 if prev[dst] == float('inf') else int(prev[dst])


def test_cheapest_flights():
    """Test cases for Cheapest Flights Within K Stops"""
    sol = Solution()
    
    # Test case 1: Example 1
    n1, flights1, src1, dst1, k1 = 4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1
    result1_d = sol.findCheapestPrice_dijkstra(n1, flights1, src1, dst1, k1)
    result1_b = sol.findCheapestPrice_bellman_ford(n1, flights1, src1, dst1, k1)
    assert result1_d == 700, f"Dijkstra: Expected 700, got {result1_d}"
    assert result1_b == 700, f"Bellman-Ford: Expected 700, got {result1_b}"
    print(f"✓ Test 1: Both methods return 700")
    
    # Test case 2: Example 2
    n2, flights2, src2, dst2, k2 = 3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1
    result2_d = sol.findCheapestPrice_dijkstra(n2, flights2, src2, dst2, k2)
    result2_b = sol.findCheapestPrice_bellman_ford(n2, flights2, src2, dst2, k2)
    assert result2_d == 200, f"Dijkstra: Expected 200, got {result2_d}"
    assert result2_b == 200, f"Bellman-Ford: Expected 200, got {result2_b}"
    print(f"✓ Test 2: Both methods return 200")
    
    # Test case 3: No route
    n3, flights3, src3, dst3, k3 = 3, [[0,1,100]], 0, 2, 1
    result3_d = sol.findCheapestPrice_dijkstra(n3, flights3, src3, dst3, k3)
    result3_b = sol.findCheapestPrice_bellman_ford(n3, flights3, src3, dst3, k3)
    assert result3_d == -1, f"Dijkstra: Expected -1, got {result3_d}"
    assert result3_b == -1, f"Bellman-Ford: Expected -1, got {result3_b}"
    print(f"✓ Test 3: No route found (correct)")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_cheapest_flights()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    n, flights, src, dst, k = 4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1
    result = sol.findCheapestPrice_bellman_ford(n, flights, src, dst, k)
    print(f"Input: n={n}, src={src}, dst={dst}, k={k}")
    print(f"Flights: {flights}")
    print(f"Output: {result}")
    print("Explanation: Path 0 -> 1 -> 3 costs 100 + 600 = 700")
# %%

