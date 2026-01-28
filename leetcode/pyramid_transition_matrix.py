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
                """
                Generate all possible next rows by processing pairs in the current row.
                
                WHAT IS INDEX?
                --------------
                The 'index' parameter represents the STARTING POSITION of the current pair
                we're processing in the current row.
                
                Example with row = "BCD":
                - index=0: We're looking at pair (B, C) at positions [0, 1]
                - index=1: We're looking at pair (C, D) at positions [1, 2]
                - index=2: We've processed all pairs (base case: index == len(row)-1)
                
                Visual representation:
                Row:     B  C  D
                Index:   0  1  2
                Pairs:   [0,1]  [1,2]
                         (B,C)  (C,D)
                
                How it works:
                1. At index=0: Look at pair (row[0], row[1]) = (B, C)
                   - Find all possible blocks that can go on top: allowed_map[(B, C)]
                   - For each possibility, add it to path and recurse with index+1
                
                2. At index=1: Look at pair (row[1], row[2]) = (C, D)
                   - Find all possible blocks: allowed_map[(C, D)]
                   - For each, add to path and recurse with index+1
                
                3. At index=2: Base case (index == len(row)-1)
                   - We've processed all pairs, return the complete path
                
                Args:
                    index: Starting position of the current pair being processed
                           (0 <= index < len(row)-1)
                    path: List of blocks chosen so far for the next row
                
                Returns:
                    List of all possible next rows (strings)
                """
                # Base case: we've processed all pairs
                # When index == len(row)-1, we've looked at the last possible pair
                # (which ends at position len(row)-1)
                if index == len(row) - 1:
                    return [''.join(path)]
                
                # Get the pair starting at 'index': (row[index], row[index + 1])
                # Example: if row="BCD" and index=0, pair = (B, C)
                #          if row="BCD" and index=1, pair = (C, D)
                pair = (row[index], row[index + 1])
                if pair not in allowed_map:
                    return []
                
                results = []
                # Try each possible block that can go on top of this pair
                for c in allowed_map[pair]:
                    path.append(c)  # Add this block to our path
                    # Move to next pair (index + 1) and continue building the row
                    
                    # WHAT IS results.extend()?
                    # ------------------------
                    # generate_next(index + 1, path) returns a LIST of strings (possible next rows)
                    # Example: It might return ['GE', 'GF'] (two different ways to complete the row)
                    #
                    # results.extend() ADDS ALL ELEMENTS from that list to results
                    # This is different from results.append() which would add the entire list as one element
                    #
                    # Example:
                    #   results = []
                    #   recursive_result = ['GE', 'GF']  # from generate_next()
                    #   results.extend(recursive_result)  # results becomes ['GE', 'GF']
                    #   # vs results.append(recursive_result) would make results = [['GE', 'GF']]
                    #
                    # Why extend()?
                    # - We want to FLATTEN the results: collect all possible complete rows
                    # - Each recursive call returns multiple possibilities (a list)
                    # - We want to combine all possibilities into one flat list
                    #
                    # Visual example with row="BCD", allowed_map[(B,C)] = {'G', 'H'}:
                    #   1. Try c='G': path=['G']
                    #      - generate_next(1, ['G']) might return ['GE', 'GF']
                    #      - results.extend(['GE', 'GF']) → results = ['GE', 'GF']
                    #   2. Try c='H': path=['H']
                    #      - generate_next(1, ['H']) might return ['HE']
                    #      - results.extend(['HE']) → results = ['GE', 'GF', 'HE']
                    #   Final return: ['GE', 'GF', 'HE'] (all possible next rows)
                    results.extend(generate_next(index + 1, path))
                    path.pop()  # Backtrack: remove this block to try next option
                
                return results
            
            next_rows = generate_next(0, [])
            for next_row in next_rows:
                if dfs(next_row):
                    memo[row] = True
                    return True
            
            memo[row] = False
            return False
        
        return dfs(bottom)

#%%

from itertools import pairwise, product

class pyramidTransition_iterative:
    """Iterative version of Pyramid Transition Matrix"""
    
    def __init__(self, allowed: list[str]):
        self.allowed_map = defaultdict(set)
        for triple in allowed:
            a, b, c = triple[0], triple[1], triple[2]
            self.allowed_map[(a, b)].add(c)
        

    def pyramidTransition(self, bottom: str) -> bool:
        return self._can_build_pyramid_from_current_row(bottom)

    @lru_cache(maxsize=None)
    def _can_build_pyramid_from_current_row(self, current_row: str) -> bool:
        """
        Generate all possible next rows from current row.
        
        IS THIS TOP-DOWN OR BOTTOM-UP DFS?
        -----------------------------------
        This is **TOP-DOWN DFS** (also called "divide and conquer" or "recursive descent").
        
        Why TOP-DOWN?
        - We start with the FULL problem (the entire bottom row)
        - We break it down into SMALLER subproblems (rows above, which are shorter)
        - We recurse DOWN the call stack: larger problem → smaller problem → base case
        - Base case: when we reach the top (len < 2)
        
        Visual representation:
        Call stack (top-down recursion):
        Level 0: _can_build("BCD")      ← Full problem (bottom row)
           ↓
        Level 1: _can_build("GE")        ← Smaller subproblem (row above)
           ↓
        Level 2: _can_build("A")         ← Base case (top reached)
        
        Physical pyramid (what we're building):
            A          ← Top (reached last)
           / \
          G   E        ← Middle (built second)
         / \ / \
        B   C   D      ← Bottom (started here)
        
        Key insight:
        - Algorithmically: TOP-DOWN (start with full problem, break down)
        - Physically: Building from BOTTOM to TOP of pyramid
        - These are different perspectives!
        
        If it were BOTTOM-UP DFS:
        - We would start with the base case (top block)
        - Build up row by row
        - Return the full solution at the end
        - This would be iterative/DP style
        
        Args:
            current_row: Current row
            
        Returns:
            True if pyramid can be built from this row to the top
        """
        # Base case: reached the top of pyramid (single block or empty)
        if len(current_row) < 2:
            return True

        # Generate all possible choices for the next row above
        # For each pair in current_row, get all possible blocks that can go on top
        next_rows = []
        for pair in pairwise(current_row):
            if pair not in self.allowed_map:
                return False  # Can't continue, no valid rule for this pair
            next_rows.append(self.allowed_map[pair])  # List of sets of possible blocks
        
        # Generate all combinations of next row using Cartesian product
        # Example: if pairs allow {G,H} and {E,F}, product gives: GE, GF, HE, HF
        for next_row_combination in product(*next_rows):
            next_row = ''.join(next_row_combination)
            # Recursively check if we can build from this next row (TOP-DOWN recursion)
            if self._can_build_pyramid_from_current_row(next_row):
                return True
        return False


class pyramidTransition_bottom_up:
    """
    BOTTOM-UP DP implementation - NO MEMOIZATION NEEDED!
    
    Key differences from top-down:
    - Builds from base case (top) up to full solution (bottom)
    - Solves each subproblem exactly ONCE, in order
    - Uses DP table instead of memoization
    - Iterative, not recursive
    """
    
    def __init__(self, allowed: list[str]):
        self.allowed_map = defaultdict(set)
        for triple in allowed:
            a, b, c = triple[0], triple[1], triple[2]
            self.allowed_map[(a, b)].add(c)
    
    def pyramidTransition(self, bottom: str) -> bool:
        """
        Bottom-up DP approach: Build from top to bottom iteratively.
        
        WHY NO MEMOIZATION?
        -------------------
        - We solve each level exactly ONCE, in order
        - No overlapping subproblems (each row at each level is computed once)
        - We use a DP table (dp[i] = set of possible rows at level i)
        - Iterative approach: level 0 → level 1 → ... → top level
        
        Structure:
        - dp[0] = {bottom}  (starting row)
        - dp[1] = all possible rows above bottom
        - dp[2] = all possible rows above dp[1]
        - ... until we reach a row of length 1 (top) or can't continue
        """
        # dp[i] = set of all possible rows at level i
        # Level 0 is the bottom row
        dp = [set([bottom])]
        
        # Build up level by level until we reach the top (row of length 1)
        while len(dp[-1]) > 0:
            current_level_rows = dp[-1]
            
            # Check if any row in current level is the top (single block)
            for row in current_level_rows:
                if len(row) == 1:
                    return True  # Successfully built to the top!
            
            # Generate next level: all possible rows above current level
            next_level_rows = set()
            
            for row in current_level_rows:
                # For each row, generate all possible rows above it
                next_rows_for_this_row = self._generate_next_level(row)
                next_level_rows.update(next_rows_for_this_row)
            
            # If we can't generate any next rows, pyramid can't be built
            if not next_level_rows:
                return False
            
            # Add next level to DP table
            dp.append(next_level_rows)
        
        return False
    
    def _generate_next_level(self, row: str) -> set[str]:
        """
        Generate all possible rows above the given row.
        
        Args:
            row: Current row
            
        Returns:
            Set of all possible rows that can be built above this row
        """
        if len(row) < 2:
            return set()
        
        # For each pair in the row, get all possible blocks that can go on top
        next_row_options = []
        for pair in pairwise(row):
            if pair not in self.allowed_map:
                return set()  # Can't continue from this row
            next_row_options.append(self.allowed_map[pair])
        
        # Generate all combinations using Cartesian product
        next_rows = set()
        for combination in product(*next_row_options):
            next_rows.add(''.join(combination))
        
        return next_rows


def explain_top_down_vs_bottom_up():
    """
    Visual explanation of Top-Down vs Bottom-Up, including memoization differences.
    """
    print("=" * 70)
    print("EXPLANATION: Top-Down vs Bottom-Up DFS + Memoization")
    print("=" * 70)
    
    print("\n1. TOP-DOWN DFS (pyramidTransition_iterative):")
    print("   - Start with FULL problem (entire bottom row)")
    print("   - Break down into SMALLER subproblems (shorter rows)")
    print("   - Recurse DOWN the call stack until base case")
    print("   - Base case: reached top (len < 2)")
    print("\n   Call Stack Visualization:")
    print("   ┌─────────────────────────┐")
    print("   │ _can_build('BCD')       │ ← Level 0: Full problem")
    print("   │   ↓                     │")
    print("   │ _can_build('GE')        │ ← Level 1: Smaller subproblem")
    print("   │   ↓                     │")
    print("   │ _can_build('A')         │ ← Level 2: Base case (top)")
    print("   └─────────────────────────┘")
    print("   Recursion goes: LARGE → SMALL → BASE CASE")
    
    print("\n2. WHY TOP-DOWN NEEDS MEMOIZATION:")
    print("   - Multiple paths can reach the SAME subproblem")
    print("   - Example: _can_build('GE') might be called from:")
    print("     * _can_build('ABCD') → tries 'XY' → _can_build('GE')")
    print("     * _can_build('EFGH') → tries 'XY' → _can_build('GE')  ← Same!")
    print("   - Without memoization: Exponential recomputation")
    print("   - With @lru_cache: Each subproblem solved ONCE")
    
    print("\n3. BOTTOM-UP DP (pyramidTransition_bottom_up):")
    print("   - Build from base case (top) up to full solution (bottom)")
    print("   - Solve each subproblem exactly ONCE, in order")
    print("   - Use DP table: dp[0] = {bottom}, dp[1] = next level, ...")
    print("\n   DP Table Visualization:")
    print("   dp[0] = {'BCD'}              ← Starting row")
    print("   dp[1] = {'GE', 'GF', ...}    ← All possible rows above")
    print("   dp[2] = {'A', 'B', ...}      ← All possible rows above dp[1]")
    print("   ... until we find a row of length 1 (top)")
    
    print("\n4. WHY BOTTOM-UP DOESN'T NEED MEMOIZATION:")
    print("   - Each level is computed exactly ONCE")
    print("   - No overlapping subproblems (we iterate through levels)")
    print("   - DP table stores results, but no need for cache lookup")
    print("   - Structure: dp[i] depends only on dp[i-1]")
    print("   - Example: dp[1] computed once, used to compute dp[2]")
    
    print("\n5. COMPARISON TABLE:")
    print("   ┌─────────────────────┬──────────────────┬──────────────────┐")
    print("   │ Aspect              │ Top-Down DFS     │ Bottom-Up DP     │")
    print("   ├─────────────────────┼──────────────────┼──────────────────┤")
    print("   │ Direction           │ Full → Base      │ Base → Full      │")
    print("   │ Structure           │ Recursive        │ Iterative        │")
    print("   │ Subproblems         │ Can overlap      │ Solved once      │")
    print("   │ Memoization         │ NEEDED ✓         │ NOT NEEDED ✗     │")
    print("   │ Storage             │ Cache + Stack    │ DP table only    │")
    print("   │ Time Complexity     │ O(n) with memo   │ O(n) naturally   │")
    print("   │ Space Complexity    │ O(n) cache       │ O(n) DP table    │")
    print("   └─────────────────────┴──────────────────┴──────────────────┘")
    
    print("\n6. Physical Pyramid (what we're building):")
    print("        A          ← Top (reached last)")
    print("       / \\")
    print("      G   E        ← Middle (built second)")
    print("     / \\ / \\")
    print("    B   C   D      ← Bottom (started here)")
    print("\n   Note: Both approaches build physically from BOTTOM to TOP,")
    print("         but algorithmically use different strategies!")
    
    print("\n7. KEY INSIGHT:")
    print("   - Top-Down: Natural recursion, but needs memoization")
    print("   - Bottom-Up: More structured, naturally avoids recomputation")
    print("   - Both are valid! Choose based on problem structure and preference")


def test_pyramid_transition_iterative():
    """Test cases for Pyramid Transition Matrix (Top-Down)"""
    sol = pyramidTransition_iterative(["BCG", "CDE", "GEA", "FFF"])
    bottom1 = "BCD"
    result1 = sol.pyramidTransition(bottom1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: bottom={bottom1}")
    print(f"  Result: {result1}")
    
    bottom2 = "AABA"
    result2 = sol.pyramidTransition(bottom2)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✓ Test 2: bottom={bottom2}")
    print(f"  Result: {result2}")
    
    # Test with different allowed rules
    sol3 = pyramidTransition_iterative(["ABC"])
    bottom3 = "AB"
    result3 = sol3.pyramidTransition(bottom3)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✓ Test 3: bottom={bottom3}")
    print(f"  Result: {result3}")
    
    # Test with no valid rules
    sol4 = pyramidTransition_iterative(["DEF"])  # No rule for AB
    bottom4 = "AB"
    result4 = sol4.pyramidTransition(bottom4)
    assert result4 == False, f"Expected False, got {result4}"
    print(f"✓ Test 4: bottom={bottom4}")
    print(f"  Result: {result4}")
    
    print("\nAll top-down tests passed!")


def test_pyramid_transition_bottom_up():
    """Test cases for Pyramid Transition Matrix (Bottom-Up)"""
    sol = pyramidTransition_bottom_up(["BCG", "CDE", "GEA", "FFF"])
    bottom1 = "BCD"
    result1 = sol.pyramidTransition(bottom1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: bottom={bottom1}")
    print(f"  Result: {result1}")
    
    bottom2 = "AABA"
    result2 = sol.pyramidTransition(bottom2)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✓ Test 2: bottom={bottom2}")
    print(f"  Result: {result2}")
    
    # Test with different allowed rules
    sol3 = pyramidTransition_bottom_up(["ABC"])
    bottom3 = "AB"
    result3 = sol3.pyramidTransition(bottom3)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✓ Test 3: bottom={bottom3}")
    print(f"  Result: {result3}")
    
    # Test with no valid rules
    sol4 = pyramidTransition_bottom_up(["DEF"])  # No rule for AB
    bottom4 = "AB"
    result4 = sol4.pyramidTransition(bottom4)
    assert result4 == False, f"Expected False, got {result4}"
    print(f"✓ Test 4: bottom={bottom4}")
    print(f"  Result: {result4}")
    
    print("\nAll bottom-up tests passed!")


def compare_top_down_vs_bottom_up():
    """
    Compare top-down and bottom-up implementations side by side.
    Demonstrates that both produce the same results, but use different approaches.
    """
    print("=" * 70)
    print("COMPARISON: Top-Down vs Bottom-Up")
    print("=" * 70)
    
    test_cases = [
        ("BCD", ["BCG", "CDE", "GEA", "FFF"]),
        ("AABA", ["AAA", "AAB", "ABA", "ABB", "BAC"]),
        ("AB", ["ABC"]),
        ("AB", ["DEF"]),  # Should fail
    ]
    
    for i, (bottom, allowed) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: bottom='{bottom}', allowed={allowed}")
        
        # Top-down (with memoization)
        sol_top_down = pyramidTransition_iterative(allowed)
        result_top_down = sol_top_down.pyramidTransition(bottom)
        
        # Bottom-up (no memoization needed)
        sol_bottom_up = pyramidTransition_bottom_up(allowed)
        result_bottom_up = sol_bottom_up.pyramidTransition(bottom)
        
        print(f"  Top-Down (with @lru_cache): {result_top_down}")
        print(f"  Bottom-Up (no memoization): {result_bottom_up}")
        print(f"  Match: {'✓' if result_top_down == result_bottom_up else '✗'}")
        
        assert result_top_down == result_bottom_up, \
            f"Results don't match! Top-down: {result_top_down}, Bottom-up: {result_bottom_up}"
    
    print("\n" + "=" * 70)
    print("✓ Both implementations produce identical results!")
    print("=" * 70)
    print("\nKey Observation:")
    print("  - Top-Down: Uses @lru_cache (memoization) to avoid recomputation")
    print("  - Bottom-Up: No memoization needed - each level computed once")
    print("  - Both are correct and efficient, just different approaches!")

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


def explain_extend_vs_append():
    """
    Visual explanation of results.extend() vs results.append().
    """
    print("=" * 70)
    print("EXPLANATION: results.extend() vs results.append()")
    print("=" * 70)
    
    print("\n1. What does extend() do?")
    print("   - extend() ADDS ALL ELEMENTS from a list to another list")
    print("   - It 'flattens' the list by one level")
    print("\n   Example:")
    print("     results = ['A']")
    print("     new_items = ['B', 'C']")
    print("     results.extend(new_items)")
    print("     # results is now ['A', 'B', 'C']")
    
    print("\n2. What does append() do?")
    print("   - append() ADDS THE ENTIRE LIST as a single element")
    print("   - It creates a nested list")
    print("\n   Example:")
    print("     results = ['A']")
    print("     new_items = ['B', 'C']")
    print("     results.append(new_items)")
    print("     # results is now ['A', ['B', 'C']]  ← nested list!")
    
    print("\n3. Why use extend() in generate_next()?")
    print("   - generate_next() returns a LIST of strings: ['GE', 'GF']")
    print("   - We want to collect ALL possible next rows in ONE flat list")
    print("   - extend() combines all recursive results into one list")
    
    print("\n4. Step-by-step example:")
    print("   Row = 'BCD', allowed_map[(B,C)] = {'G', 'H'}")
    print("   ")
    print("   results = []  # Start empty")
    print("   ")
    print("   Loop iteration 1: c = 'G'")
    print("     path = ['G']")
    print("     recursive_result = generate_next(1, ['G'])")
    print("     # Returns: ['GE', 'GF']  (two ways to complete)")
    print("     results.extend(['GE', 'GF'])")
    print("     # results = ['GE', 'GF']")
    print("   ")
    print("   Loop iteration 2: c = 'H'")
    print("     path = ['H']")
    print("     recursive_result = generate_next(1, ['H'])")
    print("     # Returns: ['HE']  (one way to complete)")
    print("     results.extend(['HE'])")
    print("     # results = ['GE', 'GF', 'HE']  ← all possibilities!")
    print("   ")
    print("   Return: ['GE', 'GF', 'HE']")
    
    print("\n5. What if we used append() instead?")
    print("   results = []")
    print("   ")
    print("   Loop iteration 1: c = 'G'")
    print("     results.append(['GE', 'GF'])")
    print("     # results = [['GE', 'GF']]  ← nested!")
    print("   ")
    print("   Loop iteration 2: c = 'H'")
    print("     results.append(['HE'])")
    print("     # results = [['GE', 'GF'], ['HE']]  ← wrong structure!")
    print("   ")
    print("   This would return nested lists, not flat list of strings!")
    
    print("\n6. Key takeaway:")
    print("   - extend() = 'add all items from this list'")
    print("   - append() = 'add this list as one item'")
    print("   - We use extend() to FLATTEN and COLLECT all recursive results")


def explain_index_parameter():
    """
    Visual explanation of what 'index' means in generate_next function.
    """
    print("=" * 70)
    print("EXPLANATION: What is 'index' in generate_next()?")
    print("=" * 70)
    
    row = "BCD"
    print(f"\nExample row: '{row}'")
    print(f"Length: {len(row)}")
    print(f"\nVisual representation:")
    print(f"  Position:  0  1  2")
    print(f"  Row:       {row[0]}  {row[1]}  {row[2]}")
    print(f"\nPairs we need to process:")
    print(f"  - Pair at index=0: ({row[0]}, {row[1]}) = (B, C)")
    print(f"  - Pair at index=1: ({row[1]}, {row[2]}) = (C, D)")
    print(f"  - When index=2: Base case (no more pairs to process)")
    
    print(f"\nHow generate_next() processes the row:")
    print(f"  1. generate_next(index=0, path=[]):")
    print(f"     - Look at pair starting at position 0: (B, C)")
    print(f"     - Find allowed blocks for (B, C) from allowed_map")
    print(f"     - For each allowed block (e.g., 'G'):")
    print(f"       * Add 'G' to path: path = ['G']")
    print(f"       * Call generate_next(index=1, path=['G'])")
    print(f"")
    print(f"  2. generate_next(index=1, path=['G']):")
    print(f"     - Look at pair starting at position 1: (C, D)")
    print(f"     - Find allowed blocks for (C, D) from allowed_map")
    print(f"     - For each allowed block (e.g., 'E'):")
    print(f"       * Add 'E' to path: path = ['G', 'E']")
    print(f"       * Call generate_next(index=2, path=['G', 'E'])")
    print(f"")
    print(f"  3. generate_next(index=2, path=['G', 'E']):")
    print(f"     - Base case: index == len(row)-1 (2 == 2)")
    print(f"     - Return complete path: ['GE']")
    print(f"")
    print(f"  Result: Next row = 'GE'")
    
    print(f"\nKey insight:")
    print(f"  - 'index' tells us WHERE in the current row we are")
    print(f"  - We process pairs from left to right: index 0, then 1, then 2...")
    print(f"  - Each pair (row[index], row[index+1]) determines one block in next row")
    print(f"  - When index reaches len(row)-1, we've processed all pairs")


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
    
    # Test top-down and bottom-up implementations
    print("\n" + "=" * 70)
    print("Testing Top-Down and Bottom-Up Implementations")
    print("=" * 70)
    test_pyramid_transition_iterative()
    print()
    test_pyramid_transition_bottom_up()
    print()
    compare_top_down_vs_bottom_up()
    
    # Explain index parameter
    print("\n")
    explain_index_parameter()
    
    # Explain extend() vs append()
    print("\n")
    explain_extend_vs_append()
    
    # Explain top-down vs bottom-up and memoization
    print("\n")
    explain_top_down_vs_bottom_up()
# %%

