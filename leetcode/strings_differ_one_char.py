# LeetCode 1554: Strings Differ by One Character
#%%
"""
Problem Statement:
------------------
Given a list of strings dict where all strings are of the same length, return true 
if there are two strings that differ by exactly one character in the same position; 
otherwise, return false.

Example 1:
Input: dict = ["abcd", "acbd", "aacd"]
Output: true
Explanation: "abcd" and "aacd" differ only by one character at index 1.

Example 2:
Input: dict = ["ab", "cd", "yz"]
Output: false

Example 3:
Input: dict = ["abcd", "cccc", "abyd", "abab"]
Output: true
Explanation: "abcd" and "abyd" differ only by one character at index 2.

KEY DIFFERENCES FROM "ONE EDIT DISTANCE" (LeetCode 161):
-------------------------------------------------------
1. **Problem Type**: 
   - 1554: Find if ANY TWO strings in a list differ by one char
   - 161: Check if TWO SPECIFIC strings are one edit apart

2. **Allowed Operations**:
   - 1554: ONLY substitution (strings must be same length)
   - 161: Insert, delete, OR replace (strings can differ in length)

3. **Position Requirement**:
   - 1554: Difference must be at the SAME position
   - 161: Can insert/delete anywhere

4. **Example**:
   - 1554: "abc" vs "adc" → True (differ at index 1)
   - 161: "abc" vs "ac" → True (delete 'b'), "ab" vs "acb" → True (insert 'c')

APPROACH:
---------
There are several approaches:

1. **Brute Force (O(n² * m))**:
   - Compare every pair of strings
   - Check if they differ by exactly one character
   - Time: O(n² * m) where n = strings, m = length
   - Space: O(1)

2. **Hash Set with Wildcards (O(n * m²))**:
   - For each string, generate all "wildcard" versions
   - Replace each position with '*' and check if seen before
   - Example: "abcd" → "*bcd", "a*cd", "ab*d", "abc*"
   - If any wildcard seen twice → found pair
   - Time: O(n * m) for generating, O(1) lookup
   - Space: O(n * m) for storing wildcards

3. **Trie Approach**:
   - Build trie with all strings
   - For each string, check if changing one char matches another
   - More complex, similar time complexity

BEST APPROACH: Hash Set with Wildcards
- Most efficient: O(n * m) time
- Easy to understand and implement
- Space: O(n * m) but practical

TIME COMPLEXITY: O(n * m) where n = number of strings, m = string length
SPACE COMPLEXITY: O(n * m) for storing wildcard patterns

INTERVIEW TIPS:
--------------
1. Key insight: Use wildcard pattern matching
2. For each string, generate patterns with one char replaced by '*'
3. If same pattern seen twice → found pair
4. Edge cases:
   - Empty list → False
   - Single string → False
   - All strings identical → False
   - Strings of different lengths (problem guarantees same length)
"""

from typing import List

class Solution:
    def differByOne(self, dict: List[str]) -> bool:
        """
        Check if there are two strings that differ by exactly one character.
        
        Strategy: Hash Set with Wildcards
        - For each string, generate all wildcard patterns (replace each char with '*')
        - Store pattern -> (word, index) to track which word created it
        - If pattern seen before with different word, we found a pair
        
        Args:
            dict: List of strings (all same length)
            
        Returns:
            True if two strings differ by exactly one character, False otherwise
        """
        # Map: pattern -> (word, index) that created it
        seen = {}
        
        for word in dict:
            # Generate all wildcard patterns for this word
            # Replace each character at position i with '*'
            for i in range(len(word)):
                # Create wildcard pattern: replace char at index i with '*'
                pattern = word[:i] + '*' + word[i+1:]
                
                # If we've seen this pattern before
                if pattern in seen:
                    prev_word, prev_idx = seen[pattern]
                    # Check if it's from a different word (not the same string)
                    # and the characters at that position are different
                    if prev_word != word and prev_word[prev_idx] != word[i]:
                        return True
                
                # Store pattern with current word and index
                seen[pattern] = (word, i)
        
        # No pair found
        return False

#%% ALTERNATIVE APPROACHES

class SolutionBruteForce:
    """Brute force approach - compare every pair"""
    
    def differByOne(self, dict: List[str]) -> bool:
        """
        Brute force: Compare every pair of strings.
        Time: O(n² * m), Space: O(1)
        """
        n = len(dict)
        
        for i in range(n):
            for j in range(i + 1, n):
                if self._differByOneChar(dict[i], dict[j]):
                    return True
        
        return False
    
    def _differByOneChar(self, s1: str, s2: str) -> bool:
        """Check if two strings differ by exactly one character"""
        if len(s1) != len(s2):
            return False
        
        diff_count = 0
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff_count += 1
                if diff_count > 1:
                    return False
        
        return diff_count == 1

#%% TEST CASES WITH EXPLANATIONS

def test_basic_cases():
    """Test basic cases from examples"""
    print("=" * 70)
    print("TEST 1: Basic Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Example 1
    dict1 = ["abcd", "acbd", "aacd"]
    result1 = sol.differByOne(dict1)
    print(f"\n1. dict = {dict1}")
    print(f"   Expected: True")
    print(f"   Got: {result1}")
    print(f"   Explanation: 'abcd' and 'aacd' differ at index 1 (b vs a)")
    print(f"   Wildcard patterns:")
    print(f"     'abcd' → '*bcd', 'a*cd', 'ab*d', 'abc*'")
    print(f"     'aacd' → '*acd', 'a*cd', 'aa*d', 'aac*'")
    print(f"     Match found: 'a*cd' appears for both!")
    assert result1 == True
    
    # Test 2: Example 2
    dict2 = ["ab", "cd", "yz"]
    result2 = sol.differByOne(dict2)
    print(f"\n2. dict = {dict2}")
    print(f"   Expected: False")
    print(f"   Got: {result2}")
    print(f"   Explanation: No two strings differ by exactly one character")
    assert result2 == False
    
    # Test 3: Example 3
    dict3 = ["abcd", "cccc", "abyd", "abab"]
    result3 = sol.differByOne(dict3)
    print(f"\n3. dict = {dict3}")
    print(f"   Expected: True")
    print(f"   Got: {result3}")
    print(f"   Explanation: 'abcd' and 'abyd' differ at index 2 (c vs y)")
    assert result3 == True

def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 70)
    print("TEST 2: Edge Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Empty list
    dict1 = []
    result1 = sol.differByOne(dict1)
    print(f"\n1. dict = {dict1} (empty)")
    print(f"   Expected: False")
    print(f"   Got: {result1}")
    assert result1 == False
    
    # Test 2: Single string
    dict2 = ["abc"]
    result2 = sol.differByOne(dict2)
    print(f"\n2. dict = {dict2} (single string)")
    print(f"   Expected: False")
    print(f"   Got: {result2}")
    assert result2 == False
    
    # Test 3: All identical
    dict3 = ["abc", "abc", "abc"]
    result3 = sol.differByOne(dict3)
    print(f"\n3. dict = {dict3} (all identical)")
    print(f"   Expected: False")
    print(f"   Got: {result3}")
    print(f"   Explanation: No difference, so no pair differs by one char")
    assert result3 == False
    
    # Test 4: Two strings, differ by one
    dict4 = ["abc", "adc"]
    result4 = sol.differByOne(dict4)
    print(f"\n4. dict = {dict4}")
    print(f"   Expected: True")
    print(f"   Got: {result4}")
    print(f"   Explanation: Differ at index 1 (b vs d)")
    assert result4 == True
    
    # Test 5: Two strings, differ by two
    dict5 = ["abc", "ade"]
    result5 = sol.differByOne(dict5)
    print(f"\n5. dict = {dict5}")
    print(f"   Expected: False")
    print(f"   Got: {result5}")
    print(f"   Explanation: Differ at indices 1 and 2 (more than one)")
    assert result5 == False

def test_complex_cases():
    """Test more complex cases"""
    print("\n" + "=" * 70)
    print("TEST 3: Complex Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Multiple pairs exist
    dict1 = ["abcd", "abce", "abcf", "abxd"]
    result1 = sol.differByOne(dict1)
    print(f"\n1. dict = {dict1}")
    print(f"   Expected: True")
    print(f"   Got: {result1}")
    print(f"   Explanation: Multiple pairs exist (e.g., 'abcd' and 'abce')")
    assert result1 == True
    
    # Test 2: Single character strings
    dict2 = ["a", "b", "c", "d"]
    result2 = sol.differByOne(dict2)
    print(f"\n2. dict = {dict2} (single chars)")
    print(f"   Expected: True")
    print(f"   Got: {result2}")
    print(f"   Explanation: Any two single chars differ by one (at index 0)")
    assert result2 == True
    
    # Test 3: Long strings
    dict3 = ["abcdefgh", "abcdefgi", "abcdefgj"]
    result3 = sol.differByOne(dict3)
    print(f"\n3. dict = {dict3} (long strings)")
    print(f"   Expected: True")
    print(f"   Got: {result3}")
    print(f"   Explanation: First two differ at last position")
    assert result3 == True

def compare_with_one_edit_distance():
    """Compare this problem with One Edit Distance (LeetCode 161)"""
    print("\n" + "=" * 70)
    print("COMPARISON WITH ONE EDIT DISTANCE (LeetCode 161)")
    print("=" * 70)
    
    print("\nKey Differences:")
    print("1. Problem Type:")
    print("   - 1554: Find pair in LIST that differs by one char")
    print("   - 161:  Check if TWO SPECIFIC strings are one edit apart")
    print()
    print("2. Operations Allowed:")
    print("   - 1554: ONLY substitution (same length required)")
    print("   - 161:  Insert, delete, OR replace (different lengths OK)")
    print()
    print("3. Examples:")
    print("   - 1554: 'abc' vs 'adc' → True (differ at index 1)")
    print("   - 161:  'abc' vs 'adc' → True (replace)")
    print("   - 161:  'abc' vs 'ac'  → True (delete 'b')")
    print("   - 161:  'ab' vs 'acb'  → True (insert 'c')")
    print("   - 1554: 'abc' vs 'ac'  → False (different lengths)")
    print("   - 1554: 'ab' vs 'acb'  → False (different lengths)")

# Run all tests
if __name__ == "__main__":
    test_basic_cases()
    test_edge_cases()
    test_complex_cases()
    compare_with_one_edit_distance()
    
    # Performance comparison
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)
    print("\nWildcard Approach (Recommended):")
    print("  Time: O(n * m) where n = strings, m = length")
    print("  Space: O(n * m) for storing patterns")
    print("  Best for: Most cases, efficient and clean")
    print("\nBrute Force Approach:")
    print("  Time: O(n² * m)")
    print("  Space: O(1)")
    print("  Best for: Small inputs, when space is critical")

# %%

