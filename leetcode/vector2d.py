# LeetCode 251: Flatten 2D Vector
#%%
"""
Problem Statement:
Implement an iterator to flatten a 2D vector. It should support the following operations:
- next() and hasNext()

Example:
Input: vec2d = [[1,2], [3], [4,5,6]]
Output: [1, 2, 3, 4, 5, 6]

INTERVIEW EXPLANATION: Why On-the-Fly Flattening?

1. **Problem Structure**: We have a 2D vector (like a spreadsheet) that we want
   to iterate over row by row, as if it were flattened into a 1D array.

2. **Why On-the-Fly (Lazy) Approach?**
   - **Memory Efficiency**: Instead of pre-flattening the entire 2D vector into
     a 1D list (which uses O(N) extra space), we track row and column indices
     and access elements on-demand. This uses O(1) extra space.
   
   - **Time Complexity**: 
     * Constructor: O(1) - just store reference
     * hasNext(): O(1) amortized - skip empty rows, each row checked at most once
     * next(): O(1) - just access element and increment column
     * Overall: O(N) where N is total number of elements
   
   - **Space Complexity**: O(1) extra space (just two pointers: row and col)

3. **Key Insight**: Use two pointers (row, col) to track current position.
   In hasNext(), skip empty rows by advancing row until we find a row with
   available elements. This handles edge cases like empty rows gracefully.

4. **Alternative Approach**: Pre-flatten at initialization
   - Pros: Simpler implementation, O(1) hasNext() and next()
   - Cons: O(N) extra space, not ideal for large or sparse 2D vectors
   - For interviews, on-the-fly is preferred (demonstrates space optimization)
"""

from typing import List


class Vector2D:
    """
    Iterator that flattens a 2D vector.
    Uses on-the-fly (lazy) flattening for O(1) space complexity.
    """
    
    def __init__(self, vec2d: List[List[int]]):
        # Store the 2D vector
        self.vec = vec2d
        self.row = 0
        self.col = 0
    
    def hasNext(self) -> bool:
        """
        Returns true if there are more elements.
        Skips empty rows automatically.
        """
        # Move row forward until we find a valid element
        while self.row < len(self.vec) and self.col >= len(self.vec[self.row]):
            self.row += 1
            self.col = 0
        return self.row < len(self.vec)
    
    def next(self) -> int:
        """
        Returns the next element in the flattened 2D vector.
        Raises StopIteration if no more elements.
        """
        if not self.hasNext():
            raise StopIteration("No more elements")
        
        # Fetch element and move col forward
        result = self.vec[self.row][self.col]
        self.col += 1
        return result


def test_vector2d():
    """Test cases for Vector2D"""
    # Test case 1: Basic example
    vec2d1 = [[1, 2], [3], [4, 5, 6]]
    i1 = Vector2D(vec2d1)
    output1 = []
    while i1.hasNext():
        output1.append(i1.next())
    assert output1 == [1, 2, 3, 4, 5, 6], f"Expected [1,2,3,4,5,6], got {output1}"
    print(f"✓ Test 1: {output1}")
    
    # Test case 2: With empty rows
    vec2d2 = [[], [1, 2], [], [3], []]
    i2 = Vector2D(vec2d2)
    output2 = []
    while i2.hasNext():
        output2.append(i2.next())
    assert output2 == [1, 2, 3], f"Expected [1,2,3], got {output2}"
    print(f"✓ Test 2 (with empty rows): {output2}")
    
    # Test case 3: Empty vector
    vec2d3 = []
    i3 = Vector2D(vec2d3)
    output3 = []
    while i3.hasNext():
        output3.append(i3.next())
    assert output3 == [], f"Expected [], got {output3}"
    print(f"✓ Test 3 (empty): {output3}")
    
    # Test case 4: Single element
    vec2d4 = [[1]]
    i4 = Vector2D(vec2d4)
    output4 = []
    while i4.hasNext():
        output4.append(i4.next())
    assert output4 == [1], f"Expected [1], got {output4}"
    print(f"✓ Test 4 (single element): {output4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_vector2d()
    
    # Example usage
    print("\nExample usage:")
    vec2d = [[1, 2], [3], [4, 5, 6]]
    print(f"Input: {vec2d}")
    i = Vector2D(vec2d)
    output = []
    while i.hasNext():
        output.append(i.next())
    print(f"Output: {output}")
# %%
