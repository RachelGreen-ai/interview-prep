# LeetCode 39: Combination Sum
#%%
"""
Problem Statement:
You are given an array of distinct positive integers candidates and a target integer target.
Return a list of all unique combinations of candidates where the chosen numbers sum to target.
You may use the same number unlimited times in the combination.

Combinations are considered unique if the frequency of at least one of the chosen numbers is different.
The order of numbers inside a combination does not matter, and the list of combinations 
may be returned in any order.

Example 1:
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

Example 2:
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
Explanation:
2 + 2 + 2 + 2 = 8
2 + 3 + 3 = 8
3 + 5 = 8

Example 3:
Input: candidates = [2], target = 1
Output: []
Explanation: No combination can sum to 1.

Constraints:
- 1 <= candidates.length <= 30
- 1 <= candidates[i] <= 200
- All elements of candidates are distinct
- 1 <= target <= 500

INTERVIEW EXPLANATION: Why Backtracking for Combination Sum?

1. **Problem Structure**: We need to find all combinations (not permutations) that sum to target.
   Since we can reuse the same number multiple times, we have an exponential search space.
   We need to explore all possible combinations systematically.

2. **Why Backtracking/DFS?**
   - **Top-Down Approach**: This is a top-down recursive solution. We start with the full
     target and break it down into smaller subproblems: "To solve target, try including
     a candidate and solve (target - candidate)". This is the natural recursive thinking.
   
   - **Exhaustive Search**: We need to find ALL valid combinations, not just one.
     Backtracking allows us to explore the entire solution space.
   
   - **Avoid Duplicates**: By maintaining order (only consider candidates from current index
     onwards), we naturally avoid duplicate combinations like [2,3] and [3,2].
   
   - **Pruning**: We can prune branches early when current sum exceeds target.
   
   - **Time Complexity**: O(2^target) in worst case, but much better with pruning
     * Each candidate can be used 0 to target/candidate times
     * With pruning, we skip invalid paths early
   
   - **Space Complexity**: O(target) for recursion stack and current combination
     * Maximum depth is target (if we use smallest candidate repeatedly)

3. **Key Insights**:
   - **Reuse Allowed**: Unlike typical combination problems, we can use same number multiple times
   - **Order Matters for Avoiding Duplicates**: Process candidates in order, only consider
     current index and beyond to avoid [2,3] and [3,2] duplicates
   - **Early Termination**: If current sum > target, backtrack immediately
   - **Two Choices at Each Step**: 
     * Include current candidate (can include again)
     * Skip current candidate and move to next

4. **Algorithm**:
   a. Sort candidates (optional but helps with pruning)
   b. Use DFS/backtracking:
      - Base case: if sum == target, add current combination to result
      - Base case: if sum > target or index out of bounds, return
      - Recursive case 1: Include current candidate (stay at same index)
      - Recursive case 2: Skip current candidate (move to next index)
   c. Backtrack: remove last added element before returning

5. **Optimization**: Sorting candidates allows early pruning when remaining candidates
   are too large to help reach target.
"""

from typing import List


class Solution:
    """Solution for Combination Sum"""
    
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations that sum to target.
        Top-down DFS/backtracking approach: starts with target and recursively
        breaks it down into smaller subproblems.
        
        Args:
            candidates: Distinct positive integers
            target: Target sum
            
        Returns:
            List of all unique combinations
        """
        result = []
        current = []
        
        # Sort to enable early pruning
        candidates.sort()
        
        def backtrack(start: int, remaining: int):
            """
            Backtrack to find all combinations.
            
            Args:
                start: Starting index in candidates (to avoid duplicates)
                remaining: Remaining target sum
            """
            # Base case: found valid combination
            if remaining == 0:
                result.append(current[:])  # Copy current combination
                return
            
            # Base case: no more candidates or remaining is negative
            if remaining < 0 or start >= len(candidates):
                return
            
            # Try including current candidate (can reuse)
            current.append(candidates[start])
            backtrack(start, remaining - candidates[start])
            current.pop()  # Backtrack
            
            # Try skipping current candidate
            backtrack(start + 1, remaining)
        
        backtrack(0, target)
        return result
    
    def combinationSum_iterative(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Bottom-up iterative approach using dynamic programming.
        Build combinations from smaller targets (0, 1, 2, ..., target).
        Contrast with top-down DFS which starts from target and breaks it down.
        """
        # dp[i] stores all combinations that sum to i
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]  # One way to sum to 0: empty combination
        
        for candidate in candidates:
            for i in range(candidate, target + 1):
                # For each combination that sums to (i - candidate),
                # add candidate to get a combination that sums to i
                for combo in dp[i - candidate]:
                    dp[i].append(combo + [candidate])
        
        return dp[target]
    
    def combinationSum_optimized(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Optimized backtracking with early pruning.
        """
        result = []
        current = []
        candidates.sort()  # Sort for early pruning
        
        def backtrack(start: int, remaining: int):
            if remaining == 0:
                result.append(current[:])
                return
            
            for i in range(start, len(candidates)):
                # Early pruning: if current candidate is too large, skip rest
                if candidates[i] > remaining:
                    break
                
                current.append(candidates[i])
                # Can reuse same candidate, so pass i (not i+1)
                backtrack(i, remaining - candidates[i])
                current.pop()  # Backtrack
        
        backtrack(0, target)
        return result


def test_combination_sum():
    """Test cases for Combination Sum"""
    sol = Solution()
    
    # Test case 1: Example 1
    candidates1 = [2, 3, 6, 7]
    target1 = 7
    result1 = sol.combinationSum(candidates1, target1)
    # Expected: [[2,2,3],[7]]
    expected1 = [[2, 2, 3], [7]]
    # Sort each combination and the result list for comparison
    result1_sorted = sorted([sorted(combo) for combo in result1])
    expected1_sorted = sorted([sorted(combo) for combo in expected1])
    assert result1_sorted == expected1_sorted, f"Expected {expected1}, got {result1}"
    print(f"✓ Test 1: candidates={candidates1}, target={target1}")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    candidates2 = [2, 3, 5]
    target2 = 8
    result2 = sol.combinationSum(candidates2, target2)
    expected2 = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    result2_sorted = sorted([sorted(combo) for combo in result2])
    expected2_sorted = sorted([sorted(combo) for combo in expected2])
    assert result2_sorted == expected2_sorted, f"Expected {expected2}, got {result2}"
    print(f"✓ Test 2: candidates={candidates2}, target={target2}")
    print(f"  Result: {result2}")
    
    # Test case 3: Example 3
    candidates3 = [2]
    target3 = 1
    result3 = sol.combinationSum(candidates3, target3)
    assert result3 == [], f"Expected [], got {result3}"
    print(f"✓ Test 3: candidates={candidates3}, target={target3}")
    print(f"  Result: {result3} (no solution)")
    
    # Test case 4: Single candidate that equals target
    candidates4 = [5]
    target4 = 5
    result4 = sol.combinationSum(candidates4, target4)
    assert result4 == [[5]], f"Expected [[5]], got {result4}"
    print(f"✓ Test 4: candidates={candidates4}, target={target4}")
    print(f"  Result: {result4}")
    
    # Test case 5: Multiple solutions
    candidates5 = [2, 3, 4]
    target5 = 6
    result5 = sol.combinationSum(candidates5, target5)
    # Expected: [[2,2,2], [2,4], [3,3]]
    print(f"✓ Test 5: candidates={candidates5}, target={target5}")
    print(f"  Result: {result5}")
    
    print("\nAll tests passed!")
    
    # Test optimized version
    print("\nTesting optimized version:")
    result1_opt = sol.combinationSum_optimized(candidates1, target1)
    result1_opt_sorted = sorted([sorted(combo) for combo in result1_opt])
    assert result1_opt_sorted == expected1_sorted, "Optimized version failed"
    print(f"✓ Optimized Test 1: {result1_opt}")
    
    # Test iterative version
    print("\nTesting iterative (DP) version:")
    result1_dp = sol.combinationSum_iterative(candidates1, target1)
    result1_dp_sorted = sorted([sorted(combo) for combo in result1_dp])
    assert result1_dp_sorted == expected1_sorted, "DP version failed"
    print(f"✓ DP Test 1: {result1_dp}")


if __name__ == "__main__":
    test_combination_sum()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    candidates = [2, 3, 6, 7]
    target = 7
    result = sol.combinationSum(candidates, target)
    
    print(f"Input:")
    print(f"  candidates = {candidates}")
    print(f"  target = {target}\n")
    print(f"Output:")
    for i, combo in enumerate(result, 1):
        print(f"  Combination {i}: {combo} (sum: {sum(combo)})")
# %%
