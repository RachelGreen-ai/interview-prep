# LeetCode 755: Pour Water
#%%
"""
Problem Statement:
We are given an elevation map, heights[i] representing the height of the terrain at that index.
The width at each index is 1. After V units of water fall at index K, how much water is at each index?

Water first drops at index K and rests on top of the highest terrain or water at that index.
Then, it "flows" to the lowest index to its left that can hold it, and if it can't find such an index,
it "flows" to the lowest index to its right that can hold it. If it can't flow to either side,
it stays at the original index.

The height of the water in each unit of the terrain after V units of water have been poured is returned.

Example 1:
Input: heights = [2,1,1,2,1,2,2], V = 4, K = 3
Output: [2,2,2,3,2,2,2]
Explanation:
#       #
#       #
# #   # #
#########
 0123456    <- index

The first drop of water lands at index 3. When the second drop of water lands at index 3,
since there is a 2-unit tall wall at index 3, the water is able to flow to index 1.
The third drop lands at index 3, and since there is a 2-unit tall wall at index 3,
the water is able to flow to index 0. The fourth drop lands at index 3, and since there is
a 1-unit tall wall at index 3, the water is able to flow to index 0.
Note that there was a 2-unit tall wall at index 3 that the water couldn't flow over.
So the final answer is [2,2,2,3,2,2,2].

Example 2:
Input: heights = [1,2,3,4], V = 2, K = 2
Output: [2,3,3,4]
Explanation:
The last drop of water lands at index 1, since that is the lowest left index to the right of index 2.

Example 3:
Input: heights = [3,1,3], V = 5, K = 1
Output: [4,4,4]

INTERVIEW EXPLANATION: Why Simulation for Pour Water?

1. **Problem Structure**: We need to simulate the physical process of water falling and flowing.
   Each unit of water:
   - First tries to stay at index K
   - If it can't (water would overflow), it flows left to the lowest valid position
   - If it can't flow left, it flows right to the lowest valid position
   - If it can't flow either way, it stays at K

2. **Why Simulation?**
   - **Physical Process**: This is a step-by-step simulation of a physical phenomenon
   - **Greedy Approach**: For each drop, we make the locally optimal choice (lowest position)
   - **No Optimal Substructure**: Each drop's behavior depends on the current state, not just
     the original heights

3. **Algorithm**:
   - For each of V units of water:
     a. Start at index K
     b. Try to flow left: find the lowest position to the left where water can rest
     c. If no valid left position, try to flow right: find the lowest position to the right
     d. If neither works, add water at K
     e. Update the heights array

4. **Key Insights**:
   - Water flows to the LOWEST position it can reach (not just any lower position)
   - We need to check if water can "flow over" barriers to reach lower positions
   - The flow direction priority: left first, then right, then stay

5. **Time Complexity**: O(V * W) where V is units of water and W is width
   - For each drop, we may scan left and right up to W positions
   
6. **Space Complexity**: O(1) extra space (modifying input array)
"""


class Solution:
    """Solution for Pour Water"""
    
    def pourWater(self, heights: list[int], V: int, K: int) -> list[int]:
        """
        Simulate pouring V units of water at index K.
        
        Args:
            heights: Initial heights of terrain
            V: Number of units of water to pour
            K: Index where water is poured
            
        Returns:
            Updated heights array after pouring water
        """
        result = heights[:]  # Make a copy
        
        for _ in range(V):
            # Try to place water at K
            pos = K
            
            # Try to flow left first
            # Find the lowest position to the left where water can rest
            left_pos = K
            for i in range(K - 1, -1, -1):
                if result[i] > result[i + 1]:
                    # Can't flow further left (hit a wall)
                    break
                if result[i] < result[left_pos]:
                    # Found a lower position
                    left_pos = i
            
            # If we found a valid left position that's lower than K
            if left_pos < K and result[left_pos] < result[K]:
                pos = left_pos
            else:
                # Try to flow right
                right_pos = K
                for i in range(K + 1, len(result)):
                    if result[i] > result[i - 1]:
                        # Can't flow further right (hit a wall)
                        break
                    if result[i] < result[right_pos]:
                        # Found a lower position
                        right_pos = i
                
                # If we found a valid right position that's lower than K
                if right_pos > K and result[right_pos] < result[K]:
                    pos = right_pos
            
            # Add water at the chosen position
            result[pos] += 1
        
        return result
    
    def pourWater_verbose(self, heights: list[int], V: int, K: int) -> list[int]:
        """
        More verbose version with detailed comments.
        """
        result = heights[:]
        
        for drop in range(V):
            pos = K
            
            # Strategy: Try left first, then right, then stay at K
            
            # Step 1: Check if we can flow left
            # Water can flow left if there's a position to the left that is:
            # - Lower than current position at K
            # - Reachable (no walls blocking the path)
            best_left = K
            for i in range(K - 1, -1, -1):
                # If we hit a wall (higher position), we can't flow further
                if result[i] > result[i + 1]:
                    break
                # Update best left position if we find a lower one
                if result[i] < result[best_left]:
                    best_left = i
            
            # If we found a better left position, use it
            if best_left < K and result[best_left] < result[K]:
                pos = best_left
            else:
                # Step 2: Check if we can flow right
                best_right = K
                for i in range(K + 1, len(result)):
                    # If we hit a wall, we can't flow further
                    if result[i] > result[i - 1]:
                        break
                    # Update best right position if we find a lower one
                    if result[i] < result[best_right]:
                        best_right = i
                
                # If we found a better right position, use it
                if best_right > K and result[best_right] < result[K]:
                    pos = best_right
                # Otherwise, pos stays at K
            
            # Step 3: Add water at the chosen position
            result[pos] += 1
        
        return result


def test_pour_water():
    """Test cases for Pour Water"""
    sol = Solution()
    
    # Test case 1: Example 1
    heights1 = [2,1,1,2,1,2,2]
    V1, K1 = 4, 3
    result1 = sol.pourWater(heights1, V1, K1)
    expected1 = [2,2,2,3,2,2,2]
    assert result1 == expected1, f"Expected {expected1}, got {result1}"
    print(f"✓ Test 1: heights={heights1}, V={V1}, K={K1}")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    heights2 = [1,2,3,4]
    V2, K2 = 2, 2
    result2 = sol.pourWater(heights2, V2, K2)
    expected2 = [2,3,3,4]
    assert result2 == expected2, f"Expected {expected2}, got {result2}"
    print(f"✓ Test 2: heights={heights2}, V={V2}, K={K2}")
    print(f"  Result: {result2}")
    
    # Test case 3: Example 3
    heights3 = [3,1,3]
    V3, K3 = 5, 1
    result3 = sol.pourWater(heights3, V3, K3)
    expected3 = [4,4,4]
    assert result3 == expected3, f"Expected {expected3}, got {result3}"
    print(f"✓ Test 3: heights={heights3}, V={V3}, K={K3}")
    print(f"  Result: {result3}")
    
    # Test case 4: Simple case - water stays at K
    heights4 = [1,2,1]
    V4, K4 = 3, 1
    result4 = sol.pourWater(heights4, V4, K4)
    print(f"✓ Test 4: heights={heights4}, V={V4}, K={K4}")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_pour_water()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    heights = [2,1,1,2,1,2,2]
    V, K = 4, 3
    result = sol.pourWater(heights, V, K)
    print(f"Initial heights: {heights}")
    print(f"Pouring {V} units at index {K}")
    print(f"Final heights: {result}")
# %%

