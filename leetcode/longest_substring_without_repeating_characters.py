# LeetCode 3: Longest Substring Without Repeating Characters
#%%
"""
Problem Statement:
Given a string s, find the length of the longest substring without repeating characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. Notice that the answer must be
a substring, "pwke" is a subsequence and not a substring.

INTERVIEW EXPLANATION: Why Sliding Window for Longest Substring Without Repeating?

1. **Problem Structure**: We need to find the longest contiguous substring with all unique
   characters. This is a classic sliding window problem.

2. **Why Sliding Window?**
   - **Contiguous Substring**: We're looking for a contiguous segment
   - **Expand Right**: Add characters to window
   - **Shrink Left**: Remove characters when we see a duplicate
   - **Track Characters**: Use set or map to track characters in current window

3. **Algorithm**:
   a. Use two pointers: left and right
   b. Expand right: add s[right] to window
   c. If s[right] already in window, shrink left until duplicate removed
   d. Update maximum length
   e. Continue until right reaches end

4. **Key Insights**:
   - Use set for O(1) lookup of characters in window
   - When duplicate found, move left pointer past the duplicate
   - Track maximum window size seen so far

5. **Time Complexity**: O(n) - each character visited at most twice
   
6. **Space Complexity**: O(min(n, m)) where m is character set size
"""


class Solution:
    """Solution for Longest Substring Without Repeating Characters"""
    
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find length of longest substring without repeating characters.
        
        Args:
            s: Input string
            
        Returns:
            Length of longest substring without repeating characters
        """
        if not s:
            return 0
        
        char_set = set()
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # If current character is in set, shrink window from left
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            
            # Add current character to set
            char_set.add(s[right])
            
            # Update maximum length
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def lengthOfLongestSubstring_optimized(self, s: str) -> int:
        """
        Optimized version using HashMap to track last seen position.
        """
        if not s:
            return 0
        
        char_map = {}  # character -> last seen index
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # If character seen before and within current window
            if s[right] in char_map and char_map[s[right]] >= left:
                left = char_map[s[right]] + 1
            
            char_map[s[right]] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length


def test_longest_substring():
    """Test cases for Longest Substring Without Repeating Characters"""
    sol = Solution()
    
    # Test case 1: Example 1
    result1 = sol.lengthOfLongestSubstring("abcabcbb")
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: 'abcabcbb' -> {result1}")
    
    # Test case 2: Example 2
    result2 = sol.lengthOfLongestSubstring("bbbbb")
    assert result2 == 1, f"Expected 1, got {result2}"
    print(f"✓ Test 2: 'bbbbb' -> {result2}")
    
    # Test case 3: Example 3
    result3 = sol.lengthOfLongestSubstring("pwwkew")
    assert result3 == 3, f"Expected 3, got {result3}"
    print(f"✓ Test 3: 'pwwkew' -> {result3}")
    
    # Test case 4: Empty string
    result4 = sol.lengthOfLongestSubstring("")
    assert result4 == 0, f"Expected 0, got {result4}"
    print(f"✓ Test 4: '' -> {result4}")
    
    # Test case 5: Single character
    result5 = sol.lengthOfLongestSubstring("a")
    assert result5 == 1, f"Expected 1, got {result5}"
    print(f"✓ Test 5: 'a' -> {result5}")
    
    # Test case 6: All unique
    result6 = sol.lengthOfLongestSubstring("abcdef")
    assert result6 == 6, f"Expected 6, got {result6}"
    print(f"✓ Test 6: 'abcdef' -> {result6}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_longest_substring()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    test_strings = ["abcabcbb", "bbbbb", "pwwkew", "abcdef"]
    for s in test_strings:
        result = sol.lengthOfLongestSubstring(s)
        print(f"'{s}' -> longest substring length: {result}")
# %%

