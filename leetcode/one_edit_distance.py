# LeetCode 161: One Edit Distance
#%%
"""
Problem Statement:
Given two strings s and t, return true if they are both one edit distance apart,
otherwise return false.

A string s is said to be one distance apart from a string t if you can:
- Insert exactly one character into s to get t
- Delete exactly one character from s to get t
- Replace exactly one character of s to get t

Example 1:
Input: s = "ab", t = "acb"
Output: true
Explanation: We can insert 'c' into s to get t.

Example 2:
Input: s = "", t = ""
Output: false
Explanation: They are the same, so not one edit distance apart.

Example 3:
Input: s = "a", t = ""
Output: true
Explanation: We can delete 'a' from s to get t.

INTERVIEW EXPLANATION: Why Two-Pointer Approach?

1. **Problem Structure**: We need to check if two strings are exactly one edit
   distance apart. This is simpler than general edit distance - we can use
   a more efficient approach.

2. **Why Two-Pointer?**
   - **Key Insight**: If strings differ by exactly one edit, we can find the
     first difference and then check if the rest matches.
   
   - **Cases**:
     * Same length → must differ in exactly one character (replace)
     * Length difference = 1 → can insert/delete one character
     * Length difference > 1 → False (more than one edit needed)
   
   - **Time Complexity**: O(min(m, n)) where m, n are string lengths
     * We only need to check until first difference
     * Much faster than O(m * n) DP approach
   
   - **Space Complexity**: O(1) - no extra space needed

3. **Algorithm**:
   - If |m - n| > 1: return False
   - Ensure s is shorter (swap if needed)
   - Find first difference
   - If same length: check if rest matches (replace case)
   - If different length: check if s[i:] == t[i+1:] (insert/delete case)
   - Edge case: s is prefix of t (all characters match, need one insert)
"""

from typing import Tuple


class Solution:
    """Solution for One Edit Distance problem"""
    
    def isOneEditDistance(self, s: str, t: str) -> bool:
        """
        Check if two strings are exactly one edit distance apart.
        
        Args:
            s: First string
            t: Second string
            
        Returns:
            True if exactly one edit distance apart, False otherwise
        """
        m, n = len(s), len(t)
        
        # Case 1: Length difference > 1 → False
        if abs(m - n) > 1:
            return False
        
        # Case 2: Ensure s is shorter for easier logic
        if m > n:
            return self.isOneEditDistance(t, s)
        
        # Case 3: Same length → must differ in exactly one character
        # Case 4: Length difference = 1 → can insert/delete one character
        
        # Find first difference
        for i in range(m):
            if s[i] != t[i]:
                if m == n:
                    # Replace: rest must match
                    return s[i + 1:] == t[i + 1:]
                else:
                    # Insert/Delete: s[i:] must match t[i+1:]
                    return s[i:] == t[i + 1:]
        
        # Edge case: all characters match, need exactly one insert
        # s is prefix of t, so m + 1 == n means one insert needed
        return m + 1 == n


def test_one_edit_distance():
    """Test cases for One Edit Distance"""
    sol = Solution()
    
    # Test case 1: Insert
    s1, t1 = "ab", "acb"
    result1 = sol.isOneEditDistance(s1, t1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: '{s1}' and '{t1}' → {result1}")
    
    # Test case 2: Same strings (not one edit)
    s2, t2 = "", ""
    result2 = sol.isOneEditDistance(s2, t2)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✓ Test 2: '{s2}' and '{t2}' → {result2}")
    
    # Test case 3: Delete
    s3, t3 = "a", ""
    result3 = sol.isOneEditDistance(s3, t3)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✓ Test 3: '{s3}' and '{t3}' → {result3}")
    
    # Test case 4: Replace
    s4, t4 = "ab", "ac"
    result4 = sol.isOneEditDistance(s4, t4)
    assert result4 == True, f"Expected True, got {result4}"
    print(f"✓ Test 4: '{s4}' and '{t4}' → {result4}")
    
    # Test case 5: More than one edit
    s5, t5 = "abc", "def"
    result5 = sol.isOneEditDistance(s5, t5)
    assert result5 == False, f"Expected False, got {result5}"
    print(f"✓ Test 5: '{s5}' and '{t5}' → {result5}")
    
    # Test case 6: Length difference > 1
    s6, t6 = "a", "abc"
    result6 = sol.isOneEditDistance(s6, t6)
    assert result6 == False, f"Expected False, got {result6}"
    print(f"✓ Test 6: '{s6}' and '{t6}' → {result6}")
    
    # Test case 7: One character difference at end
    s7, t7 = "abc", "abcd"
    result7 = sol.isOneEditDistance(s7, t7)
    assert result7 == True, f"Expected True, got {result7}"
    print(f"✓ Test 7: '{s7}' and '{t7}' → {result7}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_one_edit_distance()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    test_cases = [
        ("ab", "acb", "Insert 'c'"),
        ("", "", "Same strings"),
        ("a", "", "Delete 'a'"),
        ("ab", "ac", "Replace 'b' with 'c'"),
    ]
    
    for s, t, desc in test_cases:
        result = sol.isOneEditDistance(s, t)
        print(f"'{s}' and '{t}' ({desc}): {result}")
# %%

