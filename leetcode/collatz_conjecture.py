# Collatz Conjecture
#%%
"""
Problem Statement:
Given a formula: if n is even, divide by 2; if n is odd, multiply by 3 and add 1.
For any positive integer, the mathematical conjecture is that it will eventually reach 1.
Each transformation step counts as 1 step. Given an upper limit, find the number 
in the range that requires the most steps to reach 1.

Example:
For 7, the transformation sequence to 1 is:
7->22->11->34->17->52->26->13->40->20->10->5->16->8->4->2->1
Total steps: 17

INTERVIEW EXPLANATION: Why Memoization/DP for Collatz Conjecture?

1. **Problem Structure**: We need to compute steps for many numbers, and the 
   Collatz sequence for a number n often overlaps with sequences for other numbers.
   For example, computing steps(7) will compute steps(22), steps(11), etc.
   These intermediate values are reused when computing steps for other numbers.

2. **Why Memoization?**
   - **Overlapping Subproblems**: When computing steps(n), we recursively compute
     steps for intermediate values that may have been computed before.
     Memoization avoids recomputing these values.
   
   - **Optimal Substructure**: The steps for n depend on steps for n//2 or 3*n+1,
     which are smaller/larger subproblems. We can build up the solution from
     these subproblems.
   
   - **Time Complexity**: Without memoization: O(2^k) where k is the number of steps.
     With memoization: O(n) where n is the range size, since each number is computed once.
   
   - **Space Complexity**: O(n) for the cache.

3. **Key Insight**: The Collatz sequence forms a tree-like structure where many
   sequences converge. Memoization exploits this by caching results for all
   intermediate values encountered.
"""

from functools import lru_cache
from typing import Tuple, List


@lru_cache(maxsize=10000)
def collatz_steps(n: int) -> int:
    """
    Calculate the number of steps from n to 1 (using memoization optimization).
    
    Args:
        n: Starting number
        
    Returns:
        Number of steps to reach 1
    """
    if n == 1:
        return 0
    if n % 2 == 0:
        return 1 + collatz_steps(n // 2)
    else:
        return 1 + collatz_steps(3 * n + 1)


def collatz_sequence(n: int) -> List[int]:
    """
    Calculate the complete Collatz sequence from n to 1.
    
    Args:
        n: Starting number
        
    Returns:
        List of numbers in the sequence
    """
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


def find_longest_collatz_in_range(max_num: int) -> Tuple[int, int]:
    """
    Find the number in range [1, max_num] that requires the most steps to reach 1.
    Uses memoization for optimization.
    
    Args:
        max_num: Upper limit of the range
        
    Returns:
        Tuple of (number_with_max_steps, max_steps)
    """
    max_steps = 0
    max_num_with_steps = 1
    
    print(f"Computing Collatz steps for range 1 to {max_num}...")
    
    for i in range(1, max_num + 1):
        steps = collatz_steps(i)
        if steps > max_steps:
            max_steps = steps
            max_num_with_steps = i
        
        # Show progress
        if i % 1000 == 0:
            print(f"Computed up to {i}...")
    
    return max_num_with_steps, max_steps


def test_collatz():
    """Test cases for Collatz Conjecture"""
    # Test sequence for 7
    seq = collatz_sequence(7)
    expected = [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    assert seq == expected, f"Expected {expected}, got {seq}"
    print(f"✓ Sequence for 7: {seq}")
    
    # Test steps for 7
    steps = collatz_steps(7)
    assert steps == 16, f"Expected 16 steps, got {steps}"  # 16 steps (not 17, since we count edges)
    print(f"✓ Steps for 7: {steps}")
    
    # Test small range
    num, steps = find_longest_collatz_in_range(10)
    print(f"✓ Longest in range [1, 10]: number={num}, steps={steps}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_collatz()
    
    # Example: Find longest in range [1, 100]
    num, steps = find_longest_collatz_in_range(100)
    print(f"\nNumber with most steps in [1, 100]: {num} with {steps} steps")
    
    # Show the sequence
    print(f"\nSequence for {num}:")
    print(collatz_sequence(num))
# %%

