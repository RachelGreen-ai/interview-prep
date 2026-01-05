# LeetCode 341: Flatten Nested List Iterator
#%%
"""
Problem Statement:
Given a nested list of integers, implement an iterator to flatten it.
Each element is either an integer or a list whose elements may also be integers or other lists.

Example:
Input: [[1,1],2,[1,1]]
Output: [1,1,2,1,1]

Input: [1,[4,[6]]]
Output: [1,4,6]

INTERVIEW EXPLANATION: Why Stack for Nested List Iterator?

1. **Problem Structure**: We have a nested structure (like folders and subfolders)
   that needs to be flattened. The depth can be arbitrary, so we need a way to
   track where we are in the nested structure.

2. **Why Stack?**
   - **LIFO Nature**: When we encounter a nested list, we need to process it
     completely before moving to the next element at the current level.
     Stack's LIFO property matches this perfectly.
   
   - **Lazy Evaluation**: We don't pre-flatten everything. Instead, we flatten
     on-the-fly as we iterate, which is more memory efficient.
   
   - **Time Complexity**: 
     * Constructor: O(1) - just store the list
     * hasNext(): O(1) amortized - each element is processed once
     * next(): O(1) amortized - just pop from stack
     * Overall: O(N) where N is total number of integers
   
   - **Space Complexity**: O(D) where D is maximum depth, but worst case O(N)
     if all elements are nested.

3. **Key Insight**: Store the nested list in reverse order on the stack.
   When we encounter a list, pop it, reverse its elements, and push them back.
   This ensures we process elements in the correct order (left to right).
"""

from typing import List, Union


class NestedInteger:
    """Helper class to represent nested integers"""
    
    def __init__(self, value: Union[int, List] = None):
        """
        If value is an integer, holds a single integer.
        If value is a list, holds a list of NestedInteger.
        """
        if isinstance(value, int):
            self._integer = value
            self._list = None
        elif isinstance(value, list):
            self._integer = None
            # Ensure each element is NestedInteger
            self._list = [
                x if isinstance(x, NestedInteger) else NestedInteger(x)
                for x in value
            ]
        else:
            self._integer = None
            self._list = []
    
    def isInteger(self) -> bool:
        return self._integer is not None
    
    def getInteger(self) -> int:
        return self._integer
    
    def getList(self) -> List['NestedInteger']:
        return self._list
    
    def __repr__(self):
        if self.isInteger():
            return str(self._integer)
        return "[" + ", ".join(repr(x) for x in self._list) + "]"


class NestedIterator:
    """
    Iterator that flattens a nested list of integers.
    Uses stack-based approach for lazy evaluation.
    """
    
    def __init__(self, nestedList: List[NestedInteger]):
        # Store in reverse order so we can pop from the end
        self.stack = list(reversed(nestedList))
    
    def next(self) -> int:
        """Returns the next integer in the nested list"""
        self.hasNext()  # Ensure stack is ready
        return self.stack.pop().getInteger()
    
    def hasNext(self) -> bool:
        """
        Returns true if there are more integers, false otherwise.
        Flattens nested lists on-the-fly.
        """
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True
            # Top is a list, flatten it
            self.stack.pop()
            # Push elements in reverse order
            self.stack.extend(reversed(top.getList()))
        return False


def test_nested_iterator():
    """Test cases for Nested List Iterator"""
    # Test case 1: [[1,1],2,[1,1]]
    nested1 = NestedInteger([
        NestedInteger([1, 1]),
        2,
        NestedInteger([1, 1])
    ])
    iterator1 = NestedIterator(nested1.getList())
    result1 = []
    while iterator1.hasNext():
        result1.append(iterator1.next())
    assert result1 == [1, 1, 2, 1, 1], f"Expected [1,1,2,1,1], got {result1}"
    print(f"✓ Test 1: {result1}")
    
    # Test case 2: [1,[4,[6]]]
    nested2 = NestedInteger([1, [4, [6]]])
    iterator2 = NestedIterator(nested2.getList())
    result2 = []
    while iterator2.hasNext():
        result2.append(iterator2.next())
    assert result2 == [1, 4, 6], f"Expected [1,4,6], got {result2}"
    print(f"✓ Test 2: {result2}")
    
    # Test case 3: Empty list
    nested3 = NestedInteger([])
    iterator3 = NestedIterator(nested3.getList())
    result3 = []
    while iterator3.hasNext():
        result3.append(iterator3.next())
    assert result3 == [], f"Expected [], got {result3}"
    print(f"✓ Test 3 (empty): {result3}")
    
    # Test case 4: Single integer
    nested4 = NestedInteger([1])
    iterator4 = NestedIterator(nested4.getList())
    result4 = []
    while iterator4.hasNext():
        result4.append(iterator4.next())
    assert result4 == [1], f"Expected [1], got {result4}"
    print(f"✓ Test 4 (single): {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_nested_iterator()
    
    # Example usage
    print("\nExample usage:")
    nested = NestedInteger([1, [4, [6]]])
    print(f"Input: {nested}")
    iterator = NestedIterator(nested.getList())
    result = []
    while iterator.hasNext():
        result.append(iterator.next())
    print(f"Output: {result}")
# %%

