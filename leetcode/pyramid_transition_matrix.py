# LeetCode 756: Pyramid Transition Matrix
#%%
"""
Problem Statement:
We are stacking blocks to form a pyramid. Each block has a color which is a one-letter string.
We are allowed to place any color block C on top of two adjacent blocks of colors A and B,
if and only if ABC is an allowed triple (we may represent this as a string "ABC").

For example, "ABC" represents that we can place a block C on top of two adjacent blocks
of colors A and B. Note that this is equivalent to "ABC" being in the list allowed.

We start with a bottom row of blocks, represented as a string bottom, given as the last row
of the starting pyramid.

Return true if we can build the pyramid all the way to the top such that every allowed triple
is used at least once, or false otherwise.

Example 1:
Input: bottom = "BCD", allowed = ["BCG", "CDE", "GEA", "FFF"]
Output: true
Explanation:
We can stack the pyramid as follows:
    A
   / \
  G   E
 / \ / \
B   C   D

This is possible because:
- "BCG" allows G on top of (B, C)
- "CDE" allows E on top of (C, D)
- "GEA" allows A on top of (G, E)

Example 2:
Input: bottom = "AABA", allowed = ["AAA", "AAB", "ABA", "ABB", "BAC"]
Output: false
Explanation:
We cannot build the pyramid to the top. Note that there could be multiple ways to build
the pyramid but it won't be possible to build it to the top.

INTERVIEW EXPLANATION: Why Backtracking/DFS for Pyramid Transition?

1. **Problem Structure**: We need to build a pyramid level by level, where each level
   has one fewer block than the level below. We need to find if there exists a valid
   assignment of colors that satisfies all allowed triples.

2. **Why Backtracking?**
   - **Search Problem**: We need to explore all possible ways to build the pyramid
   - **Constraint Satisfaction**: Each block placement must satisfy allowed triples
   - **Exponential Search Space**: Multiple choices at each level
   - **Early Termination**: We can stop as soon as we find one valid solution

3. **Algorithm**:
   - Start with the bottom row
   - For each level above:
     a. Generate all possible next rows based on allowed triples
     b. For each possible next row, recursively try to build the rest
     c. If we reach the top (single block), return true
     d. If no valid path found, backtrack and try next option
   
4. **Key Insights**:
   - Build from bottom to top (one level at a time)
   - For a row of length n, the next row has length n-1
   - Each position in the next row depends on two adjacent positions in current row
   - Use memoization to avoid recomputing the same subproblems
   
5. **Time Complexity**: O(A^N) where A is number of allowed triples and N is pyramid height
   - In worst case, we explore all possible combinations
   
6. **Space Complexity**: O(N) for recursion stack and memoization
"""

from collections import defaultdict
from functools import lru_cache


class Solution:
    """Solution for Pyramid Transition Matrix"""
    
    def pyramidTransition(self, bottom: str, allowed: list[str]) -> bool:
        """
        Check if we can build a pyramid from bottom to top.
        
        Args:
            bottom: The bottom row of blocks
            allowed: List of allowed triples "ABC" meaning C can be on top of A and B
            
        Returns:
            True if pyramid can be built, False otherwise
        """
        # Build a map: (A, B) -> set of possible C values
        allowed_map = defaultdict(set)
        for triple in allowed:
            a, b, c = triple[0], triple[1], triple[2]
            allowed_map[(a, b)].add(c)
        
        @lru_cache(maxsize=None)
        def can_build(row: str) -> bool:
            """
            Check if we can build pyramid starting from this row.
            
            Args:
                row: Current row of blocks
                
            Returns:
                True if we can build to the top from this row
            """
            # Base case: if row has only one block, we're at the top
            if len(row) == 1:
                return True
            
            # Generate all possible next rows
            next_rows = self._generate_next_rows(row, allowed_map)
            
            # Try each possible next row
            for next_row in next_rows:
                if can_build(next_row):
                    return True
            
            return False
        
        return can_build(bottom)
    
    def _generate_next_rows(self, row: str, allowed_map: dict) -> list[str]:
        """
        Generate all possible next rows from current row.
        
        Args:
            row: Current row
            allowed_map: Map of (A, B) -> set of possible C values
            
        Returns:
            List of possible next rows
        """
        if len(row) < 2:
            return []
        
        # For each adjacent pair, find possible top blocks
        def backtrack(index: int, current: list[str]) -> list[str]:
            """
            Generate all possible next rows using backtracking.
            
            Args:
                index: Current position in row (looking at pair starting at index)
                current: Current partial next row being built
                
            Returns:
                List of complete next rows
            """
            # Base case: we've processed all pairs
            if index == len(row) - 1:
                return [''.join(current)]
            
            # Get the pair (row[index], row[index+1])
            pair = (row[index], row[index + 1])
            
            # Get all possible top blocks for this pair
            possible_tops = allowed_map.get(pair, set())
            
            if not possible_tops:
                return []  # No valid continuation
            
            # Try each possible top block
            results = []
            for top in possible_tops:
                current.append(top)
                # Recursively generate rest of the row
                results.extend(backtrack(index + 1, current))
                current.pop()
            
            return results
        
        return backtrack(0, [])
    
    def pyramidTransition_optimized(self, bottom: str, allowed: list[str]) -> bool:
        """
        Optimized version using iterative approach with memoization.
        """
        # Build allowed map
        allowed_map = defaultdict(set)
        for triple in allowed:
            a, b, c = triple[0], triple[1], triple[2]
            allowed_map[(a, b)].add(c)
        
        memo = {}
        
        def dfs(row: str) -> bool:
            if len(row) == 1:
                return True
            
            if row in memo:
                return memo[row]
            
            # Generate next row possibilities
            def generate_next(index: int, path: list[str]) -> list[str]:
                if index == len(row) - 1:
                    return [''.join(path)]
                
                pair = (row[index], row[index + 1])
                if pair not in allowed_map:
                    return []
                
                results = []
                for c in allowed_map[pair]:
                    path.append(c)
                    results.extend(generate_next(index + 1, path))
                    path.pop()
                
                return results
            
            next_rows = generate_next(0, [])
            for next_row in next_rows:
                if dfs(next_row):
                    memo[row] = True
                    return True
            
            memo[row] = False
            return False
        
        return dfs(bottom)


def test_pyramid_transition():
    """Test cases for Pyramid Transition Matrix"""
    sol = Solution()
    
    # Test case 1: Example 1
    bottom1 = "BCD"
    allowed1 = ["BCG", "CDE", "GEA", "FFF"]
    result1 = sol.pyramidTransition(bottom1, allowed1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: bottom={bottom1}, allowed={allowed1}")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    bottom2 = "AABA"
    allowed2 = ["AAA", "AAB", "ABA", "ABB", "BAC"]
    result2 = sol.pyramidTransition(bottom2, allowed2)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✓ Test 2: bottom={bottom2}, allowed={allowed2}")
    print(f"  Result: {result2}")
    
    # Test case 3: Simple valid case
    bottom3 = "AB"
    allowed3 = ["ABC"]
    result3 = sol.pyramidTransition(bottom3, allowed3)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✓ Test 3: bottom={bottom3}, allowed={allowed3}")
    print(f"  Result: {result3}")
    
    # Test case 4: Simple invalid case
    bottom4 = "AB"
    allowed4 = ["DEF"]  # No rule for AB
    result4 = sol.pyramidTransition(bottom4, allowed4)
    assert result4 == False, f"Expected False, got {result4}"
    print(f"✓ Test 4: bottom={bottom4}, allowed={allowed4}")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_pyramid_transition()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    bottom = "BCD"
    allowed = ["BCG", "CDE", "GEA", "FFF"]
    result = sol.pyramidTransition(bottom, allowed)
    print(f"Bottom row: {bottom}")
    print(f"Allowed triples: {allowed}")
    print(f"Can build pyramid: {result}")
# %%

