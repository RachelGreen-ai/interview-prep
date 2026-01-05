# LeetCode 385: Mini Parser
#%%
"""
Problem Statement:
Given a string s represents the serialization of a nested list, implement a parser
to deserialize it and return the deserialized NestedInteger.

Each element is either an integer or a list whose elements may also be integers
or other lists.

Example 1:
Input: s = "324"
Output: 324
Explanation: You should return a NestedInteger object which contains a single integer 324.

Example 2:
Input: s = "[123,[456,[789]]]"
Output: [123,[456,[789]]]
Explanation: Return a NestedInteger object containing a nested list with 2 elements:
1. An integer containing value 123.
2. A nested list containing two elements:
   - An integer containing value 456.
   - A nested list with one element:
     - An integer containing value 789.

Example 3:
Input: s = "[123,456,[788,799,833],[[]],10,[]]"
Output: [123,456,[788,799,833],[[]],10,[]]

INTERVIEW EXPLANATION: Why Stack for Mini Parser?

1. **Problem Structure**: We need to parse a string representation of nested lists.
   The structure can be arbitrarily nested, and we need to build the corresponding
   NestedInteger object. This is similar to parsing JSON or nested parentheses.

2. **Why Stack?**
   - **Nested Structure**: When we encounter '[', we start a new list. When we
     encounter ']', we close the current list and add it to the parent list.
     Stack naturally handles this nested structure.
   
   - **State Management**: We need to track:
     * Current list being built
     * Parent lists (for nesting)
     * Current number being parsed (may span multiple digits)
     * Negative sign handling
   
   - **Algorithm**:
     * Use stack to store NestedInteger objects (current lists)
     * When we see '[', push a new NestedInteger (list) onto stack
     * When we see a digit, accumulate the number
     * When we see ',' or ']', if we have a number, add it to current list
     * When we see ']', pop the current list and add it to parent (if exists)
   
   - **Time Complexity**: O(n) where n is length of string
     * Single pass through the string
   
   - **Space Complexity**: O(d) where d is maximum nesting depth
     * Stack stores at most d NestedInteger objects

3. **Key Insights**:
   - Handle negative numbers (check for '-' before digits)
   - Accumulate multi-digit numbers character by character
   - Empty lists: "[]" should create an empty NestedInteger list
   - Single integer (no brackets): Return NestedInteger with that integer
   - When closing a list, add it to parent before popping

4. **Edge Cases**:
   - Single integer: "324" (no brackets)
   - Empty list: "[]"
   - Nested empty lists: "[[]]"
   - Negative numbers: "-123"
   - Multiple digits: "12345"
"""

from typing import List, Union


class NestedInteger:
    """
    Helper class to represent nested integers.
    This is a simplified version for the problem.
    """
    
    def __init__(self, value: Union[int, List['NestedInteger']] = None):
        """
        Initialize a NestedInteger.
        If value is int, it's a single integer.
        If value is None, it's an empty list.
        If value is List[NestedInteger], it's a nested list.
        """
        if isinstance(value, int):
            self._integer = value
            self._list = None
            self._is_integer = True
        elif value is None:
            self._integer = None
            self._list = []
            self._is_integer = False
        else:
            self._integer = None
            self._list = value
            self._is_integer = False
    
    def isInteger(self) -> bool:
        """Return True if this NestedInteger holds a single integer"""
        return self._is_integer
    
    def getInteger(self) -> int:
        """Return the single integer if this holds a single integer"""
        return self._integer
    
    def getList(self) -> List['NestedInteger']:
        """Return the nested list if this holds a nested list"""
        return self._list if self._list is not None else []
    
    def add(self, elem: 'NestedInteger') -> None:
        """Add a NestedInteger to this list"""
        if self._list is None:
            self._list = []
            self._is_integer = False
            self._integer = None
        self._list.append(elem)
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        if self.isInteger():
            return str(self.getInteger())
        else:
            return '[' + ','.join(str(x) for x in self.getList()) + ']'


class Solution:
    """Solution for Mini Parser"""
    
    def deserialize(self, s: str) -> NestedInteger:
        """
        Deserialize string s into a NestedInteger object.
        
        Args:
            s: String representation of nested list
            
        Returns:
            NestedInteger object representing the parsed structure
        """
        # Edge case: single integer (no brackets)
        if s[0] != '[':
            return NestedInteger(int(s))
        
        stack = []
        num = None
        negative = False
        
        for char in s:
            if char == '-':
                negative = True
            elif char.isdigit():
                # Accumulate multi-digit numbers
                num = (num or 0) * 10 + int(char)
            elif char == '[':
                # Start a new list
                stack.append(NestedInteger())
            elif char in ',]':
                # End of number or end of list
                if num is not None:
                    # Add the number to current list
                    if negative:
                        num = -num
                    stack[-1].add(NestedInteger(num))
                    num = None
                    negative = False
                
                if char == ']':
                    # Close current list
                    if len(stack) > 1:
                        # Pop current list and add to parent
                        current = stack.pop()
                        stack[-1].add(current)
                    # If stack has only one element, we're done (it's the root)
        
        return stack[0] if stack else NestedInteger()


def test_mini_parser():
    """Test cases for Mini Parser"""
    sol = Solution()
    
    # Test case 1: Single integer
    s1 = "324"
    result1 = sol.deserialize(s1)
    assert result1.isInteger(), "Should be an integer"
    assert result1.getInteger() == 324, f"Expected 324, got {result1.getInteger()}"
    print(f"✓ Test 1: '{s1}' → {result1.getInteger()}")
    
    # Test case 2: Nested list
    s2 = "[123,[456,[789]]]"
    result2 = sol.deserialize(s2)
    assert not result2.isInteger(), "Should be a list"
    list2 = result2.getList()
    assert len(list2) == 2, f"Expected 2 elements, got {len(list2)}"
    assert list2[0].getInteger() == 123, "First element should be 123"
    print(f"✓ Test 2: '{s2}' → {result2}")
    
    # Test case 3: Complex nested list
    s3 = "[123,456,[788,799,833],[[]],10,[]]"
    result3 = sol.deserialize(s3)
    assert not result3.isInteger(), "Should be a list"
    list3 = result3.getList()
    assert len(list3) == 6, f"Expected 6 elements, got {len(list3)}"
    print(f"✓ Test 3: '{s3}' → {result3}")
    
    # Test case 4: Empty list
    s4 = "[]"
    result4 = sol.deserialize(s4)
    assert not result4.isInteger(), "Should be a list"
    assert len(result4.getList()) == 0, "Should be empty"
    print(f"✓ Test 4: '{s4}' → {result4}")
    
    # Test case 5: Nested empty lists
    s5 = "[[]]"
    result5 = sol.deserialize(s5)
    assert not result5.isInteger(), "Should be a list"
    list5 = result5.getList()
    assert len(list5) == 1, "Should have one element"
    assert len(list5[0].getList()) == 0, "Inner list should be empty"
    print(f"✓ Test 5: '{s5}' → {result5}")
    
    # Test case 6: Negative number
    s6 = "-123"
    result6 = sol.deserialize(s6)
    assert result6.isInteger(), "Should be an integer"
    assert result6.getInteger() == -123, f"Expected -123, got {result6.getInteger()}"
    print(f"✓ Test 6: '{s6}' → {result6.getInteger()}")
    
    # Test case 7: List with negative numbers
    s7 = "[123,-456,[-789]]"
    result7 = sol.deserialize(s7)
    assert not result7.isInteger(), "Should be a list"
    list7 = result7.getList()
    assert list7[0].getInteger() == 123, "First should be 123"
    assert list7[1].getInteger() == -456, "Second should be -456"
    print(f"✓ Test 7: '{s7}' → {result7}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_mini_parser()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    examples = [
        "324",
        "[123,[456,[789]]]",
        "[123,456,[788,799,833],[[]],10,[]]",
        "[]",
        "-123"
    ]
    
    for s in examples:
        result = sol.deserialize(s)
        print(f"Input:  {s}")
        print(f"Output: {result}")
        print()
# %%

