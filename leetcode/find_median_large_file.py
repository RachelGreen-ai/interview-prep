# Find Median in Large File of Integers
#%%
"""
Problem Statement:
You are given a very large file containing integers (could be millions or billions),
too large to load entirely into memory. You need to find the median value.

Median definition:
- If n is odd → the middle element in the sorted order
- If n is even → average of the two middle elements

Constraints:
- The integers are not sorted
- The file is too large to fit in memory (so no read all → sort → index)
- You may assume you can only read chunks of the file at a time

INTERVIEW EXPLANATION: Why Binary Search on Value Range?

1. **Problem Structure**: We cannot load all numbers into memory, so traditional
   sorting approaches won't work. However, we know the integer range.

2. **Why Binary Search on Value Range?**
   - **Key Insight**: Instead of binary search on array indices (which we don't have),
     we do binary search on the VALUE RANGE (e.g., [-2^31, 2^31-1])
   
   - **Approach**:
     * Pick a guess value in the numeric range
     * Count how many numbers in file are ≤ guess (one pass through file)
     * If count == k (target position) → found it
     * If count < k → median is larger → search higher
     * If count > k → median is smaller → search lower
   
   - **Time Complexity**: 
     * O(log(range) * file_size) where range = max - min
     * For 32-bit integers: O(32 * file_size) = O(file_size)
     * Each binary search iteration requires one full file pass
   
   - **Space Complexity**: O(1) - only track count and max_leq

3. **Key Details**:
   - max_leq: Track the maximum number ≤ guess to ensure correctness
   - When count == k: Return max_leq (not guess) to handle duplicates
   - When count < k: Move left = max(max_leq + 1, guess + 1)
   - When count > k: Move right = max_leq

4. **Why This Works**:
   - Each iteration narrows the search range
   - Eventually left == right → we've found the exact k-th smallest value
   - Never need to store all numbers, just count them
"""

from typing import Tuple, Optional


def count_leq(file_path: str, guess: int) -> Tuple[int, int]:
    """
    Count how many numbers in the file are <= guess.
    Also track the maximum number <= guess.
    
    Args:
        file_path: Path to the file containing integers (one per line)
        guess: The value to compare against
        
    Returns:
        Tuple of (count, max_leq) where:
        - count: number of integers <= guess
        - max_leq: maximum integer <= guess (or -inf if none)
    """
    count = 0
    max_leq = float('-inf')
    
    with open(file_path, "r") as f:
        for line in f:
            num = int(line.strip())
            if num <= guess:
                count += 1
                max_leq = max(max_leq, num)
    
    return count, max_leq


def find_kth(file_path: str, k: int, left: int = -2**31, right: int = 2**31 - 1) -> int:
    """
    Find the k-th smallest number in the file using binary search on value range.
    
    Args:
        file_path: Path to the file containing integers
        k: Target position (1-indexed, so k=1 means smallest)
        left: Minimum possible value in range
        right: Maximum possible value in range
        
    Returns:
        The k-th smallest number
    """
    while left < right:
        guess = left + (right - left) // 2
        count, max_leq = count_leq(file_path, guess)
        
        if count == k:
            # Found exactly k numbers <= guess
            # Return max_leq to handle duplicates correctly
            return max_leq
        elif count < k:
            # Fewer than k numbers <= guess
            # k-th smallest must be larger than guess
            left = max(max_leq + 1, guess + 1)
        else:
            # More than k numbers <= guess
            # k-th smallest must be <= max_leq
            right = max_leq
    
    return left


def find_median(file_path: str) -> float:
    """
    Find median from a large file using value-space binary search.
    
    Args:
        file_path: Path to the file containing integers (one per line)
        
    Returns:
        Median value (float for even n, int for odd n)
    """
    # First pass: count total numbers
    with open(file_path, "r") as f:
        n = sum(1 for _ in f)
    
    if n == 0:
        raise ValueError("File is empty")
    
    if n % 2 == 1:
        # Odd: return middle element
        k = n // 2 + 1
        return float(find_kth(file_path, k))
    else:
        # Even: return average of two middle elements
        left_med = find_kth(file_path, n // 2)
        right_med = find_kth(file_path, n // 2 + 1)
        return (left_med + right_med) / 2.0


def create_test_file(file_path: str, numbers: list) -> None:
    """Helper function to create a test file"""
    with open(file_path, "w") as f:
        for num in numbers:
            f.write(f"{num}\n")


def test_find_median():
    """Test cases for Find Median"""
    import tempfile
    import os
    
    # Test case 1: Odd number of elements
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_file1 = f.name
        numbers1 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        for num in numbers1:
            f.write(f"{num}\n")
    
    try:
        median1 = find_median(test_file1)
        expected1 = 4.0  # Sorted: [1,1,2,3,4,5,5,6,9], median = 4
        assert abs(median1 - expected1) < 0.01, f"Expected {expected1}, got {median1}"
        print(f"✓ Test 1 (odd): median = {median1}")
    finally:
        os.unlink(test_file1)
    
    # Test case 2: Even number of elements
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_file2 = f.name
        numbers2 = [3, 1, 4, 1, 5, 9]
        for num in numbers2:
            f.write(f"{num}\n")
    
    try:
        median2 = find_median(test_file2)
        expected2 = (3 + 4) / 2.0  # Sorted: [1,1,3,4,5,9], median = (3+4)/2
        assert abs(median2 - expected2) < 0.01, f"Expected {expected2}, got {median2}"
        print(f"✓ Test 2 (even): median = {median2}")
    finally:
        os.unlink(test_file2)
    
    # Test case 3: Single element
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_file3 = f.name
        f.write("42\n")
    
    try:
        median3 = find_median(test_file3)
        assert median3 == 42.0, f"Expected 42.0, got {median3}"
        print(f"✓ Test 3 (single): median = {median3}")
    finally:
        os.unlink(test_file3)
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_find_median()
    
    # Example usage with a larger file
    print("\nExample usage:")
    import tempfile
    import os
    import random
    
    # Create a test file with random numbers
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_file = f.name
        numbers = [random.randint(1, 1000) for _ in range(100)]
        for num in numbers:
            f.write(f"{num}\n")
    
    try:
        median = find_median(test_file)
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        if n % 2 == 1:
            expected = sorted_nums[n // 2]
        else:
            expected = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0
        
        print(f"File has {n} numbers")
        print(f"Computed median: {median}")
        print(f"Expected median: {expected}")
        print(f"Match: {'✓' if abs(median - expected) < 0.01 else '✗'}")
    finally:
        os.unlink(test_file)
# %%

