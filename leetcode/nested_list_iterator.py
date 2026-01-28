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

VISUAL EXPLANATION:

Example 1: [[1,2],3,[4,5]]
─────────────────────────────────────────────────────────────

Tree Structure:
    [root]
     /|\
    / | \
   /  |  \
 [1,2] 3 [4,5]

Key Insight: Python list as stack
- We use list[-1] to check the "top" (last element of list)
- We use list.pop() to remove and return the "top" (last element)
- We reverse the initial list so the FIRST element becomes the LAST
- When we pop, we get elements in original order!

Step-by-Step Execution:

Initial State:
  Input: [[1,2], 3, [4,5]]
  Original order: [1,2], 3, [4,5]  (index 0, 1, 2)
  After reversing: Stack = [[4,5], 3, [1,2]]
                   (index 0)  (index 1)  (index 2 = stack[-1])
  
  Why reverse? 
  - Original first element [1,2] is now at stack[-1] (last position)
  - stack[-1] checks the "top" = [1,2] ✓
  - stack.pop() removes and returns [1,2] first ✓

Call hasNext():
  Check stack[-1] = [1,2] (list) → Pop it
  Elements of [1,2]: [1, 2] (left→right: 1, then 2)
  Reverse: [2, 1] (so 1 will be popped first)
  Extend stack: Stack = [[4,5], 3, 2, 1]
  Check stack[-1] = 1 (integer) → Return True

Call next():
  Pop 1 → Return 1
  Stack = [[4,5], 3, 2]

Call hasNext():
  Check stack[-1] = 2 (integer) → Return True

Call next():
  Pop 2 → Return 2
  Stack = [[4,5], 3]

Call hasNext():
  Check stack[-1] = 3 (integer) → Return True

Call next():
  Pop 3 → Return 3
  Stack = [[4,5]]

Call hasNext():
  Check stack[-1] = [4,5] (list) → Pop it
  Elements of [4,5]: [4, 5] (left→right: 4, then 5)
  Reverse: [5, 4] (so 4 will be popped first)
  Extend stack: Stack = [5, 4]
  Check stack[-1] = 4 (integer) → Return True

Call next():
  Pop 4 → Return 4
  Stack = [5]

Call hasNext():
  Check stack[-1] = 5 (integer) → Return True

Call next():
  Pop 5 → Return 5
  Stack = []

Final Output: [1, 2, 3, 4, 5] ✓

─────────────────────────────────────────────────────────────

Visual Summary:
- Reversing puts first element at end (stack[-1])
- Checking stack[-1] gives us the "next" element to process
- Popping removes from end, maintaining left-to-right order
- For nested lists, reverse their elements before pushing

─────────────────────────────────────────────────────────────

Example 2: [1,[4,[6]]]
─────────────────────────────────────────────────────────────

Tree Structure:
    [root]
     / \
    1  [4,[6]]
          / \
         4  [6]
            |
            6

Step-by-Step Execution:

Initial State:
  Input: [1, [4, [6]]]
  Original order: 1, [4,[6]]  (index 0, 1)
  After reversing: Stack = [[4,[6]], 1]
                   (index 0)  (index 1 = stack[-1])
  
  stack[-1] = 1 (the first element of original) ✓

Call hasNext():
  Check stack[-1] = 1 (integer) → Return True

Call next():
  Pop 1 → Return 1
  Stack = [[4,[6]]]

Call hasNext():
  Check stack[-1] = [4,[6]] (list) → Pop it
  Elements of [4,[6]]: [4, [6]] (left→right: 4, then [6])
  Reverse: [[6], 4] (so 4 will be popped first)
  Extend stack: Stack = [[6], 4]
  Check stack[-1] = 4 (integer) → Return True

Call next():
  Pop 4 → Return 4
  Stack = [[6]]

Call hasNext():
  Check stack[-1] = [6] (list) → Pop it
  Elements of [6]: [6] (left→right: 6)
  Reverse: [6] (single element, no change)
  Extend stack: Stack = [6]
  Check stack[-1] = 6 (integer) → Return True

Call next():
  Pop 6 → Return 6
  Stack = []

Final Output: [1, 4, 6] ✓

But the expected output is [1, 4, 6], meaning 1 should come first!

Unless... oh! Maybe the test case expectation is wrong, or maybe I'm
misunderstanding how the flattening should work. Let me check the actual
test in the code...

Looking at test case 2:
  nested2 = NestedInteger([1, [4, [6]]])
  Expected: [1, 4, 6]

So the expectation is correct. The algorithm must handle this correctly.
Let me re-read the code more carefully...

Ah! I see - when we reverse [4, [6]], we get [[6], 4]. But we want
to process 4 before [6] in the flattened order. So when we push [[6], 4],
the stack becomes: [6] on top, then 4, then 1. So we'd get [6, 4, 1].

But we want [1, 4, 6]. So the initial reversal must be handled differently,
or the nested reversal logic is different.

Actually, wait - I think the issue is that we want to process the ORIGINAL
order left-to-right. So [1, [4,[6]]] should give [1, 4, 6].

If we reverse initially: [[4,[6]], 1], then [4,[6]] is on top.
When we flatten [4,[6]], we reverse to get [[6], 4], push to get stack: [6], 4, 1.
This gives [6, 4, 1] which is backwards.

I think the correct approach is: DON'T reverse the initial list, OR
don't reverse nested list elements. Let me check what the actual working
code does...

Actually, I realize: the code DOES work correctly! The key is understanding
that we reverse initially, so the LAST element of the original list is on top.
When we process from top to bottom (popping), we get elements in original order.

But for nested lists, we also reverse their elements before pushing, so
when we pop them, we get them in their original order too.

Let me trace one more time with this understanding:

Input: [1, [4, [6]]]
Original order (left to right): 1, then [4, [6]]
Reversed: [[4,[6]], 1]  (last element first on stack)

When we pop from stack (LIFO), we get: first [4,[6]], then 1.
But we want: first 1, then [4,[6]].

So the reversal ensures that when we POP (which is LIFO), we get the
FIRST element of the original list first!

Stack after reverse: [[4,[6]], 1]
Pop order (LIFO): 1 comes out first, then [4,[6]] - perfect!

So:
- Initial reverse: puts last element on top
- Pop (LIFO): gets first element first ✓

For nested [4, [6]]:
- Elements: [4, [6]] (left to right: 4, then [6])
- Reverse: [[6], 4] (last element [6] on top)
- Pop order: 4 comes out first, then [6] - perfect!

So the algorithm is correct! Let me rewrite the visual with correct understanding.
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

