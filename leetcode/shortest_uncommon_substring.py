# LeetCode 3076: Shortest Uncommon Substring in an Array
#%%
"""
Problem Statement:
You are given an array of strings arr.

A string s is a substring of t if you can remove some (possibly zero) characters from the
beginning and end of t to get s. For example, "abc" is a substring of "aabcde" but not "acb".

A string s is an uncommon substring of arr if it appears at most once as a substring in
any string in arr.

Return an array of strings, where ans[i] is the shortest uncommon substring of arr[i].
If such a substring does not exist, set ans[i] to an empty string.

A substring is a contiguous sequence of characters within a string.

Example 1:
Input: arr = ["cab","ad","bad","c"]
Output: ["ab","","ba",""]
Explanation:
- For arr[0] = "cab", the shortest uncommon substring is "ab" (appears in "cab" but not in others).
- For arr[1] = "ad", there is no uncommon substring (all substrings of "ad" appear in other strings).
- For arr[2] = "bad", the shortest uncommon substring is "ba" (appears in "bad" but not in others).
- For arr[3] = "c", there is no uncommon substring (the substring "c" appears in "cab").

Example 2:
Input: arr = ["abc","bcd","abcd"]
Output: ["","","abc"]

INTERVIEW EXPLANATION: Why Brute Force with Optimization for Shortest Uncommon Substring?

1. **Problem Structure**: For each string in arr, find the shortest substring that appears
   in that string but not in any other string.

2. **Why Brute Force with Optimization?**
   - **Generate Substrings**: For each string, generate all substrings in order of length
   - **Check Uniqueness**: For each substring, check if it appears in other strings
   - **Early Termination**: Stop at first uncommon substring (shortest by construction)
   - **Optimization**: Use set for fast substring lookup in other strings

3. **Algorithm**:
   For each string s in arr:
     a. Generate all substrings of s, starting from shortest
     b. For each substring, check if it appears in any other string
     c. If not found in others, it's the answer for this string
     d. If no uncommon substring found, return empty string

4. **Key Insights**:
   - Generate substrings by length: length 1, then 2, then 3, ...
   - For each length, try all starting positions
   - Use substring sets for fast lookup
   - Early termination when uncommon substring found

5. **Time Complexity**: O(N * M^3) where N is array size, M is max string length
   - For each string: O(M^2) substrings, each checked in O(M * N) time
   
6. **Space Complexity**: O(N * M^2) for storing substring sets
"""


class Solution:
    """Solution for Shortest Uncommon Substring"""
    
    def shortestUncommonSubstring(self, arr: list[str]) -> list[str]:
        """
        Find shortest uncommon substring for each string.
        
        Args:
            arr: Array of strings
            
        Returns:
            Array of shortest uncommon substrings (empty string if none exists)
        """
        n = len(arr)
        result = []
        
        for i in range(n):
            s = arr[i]
            found = False
            
            # Generate all substrings of s, starting from shortest
            for length in range(1, len(s) + 1):
                if found:
                    break
                
                # Try all substrings of this length
                for start in range(len(s) - length + 1):
                    substring = s[start:start + length]
                    
                    # Check if this substring appears in any other string
                    is_uncommon = True
                    for j in range(n):
                        if i != j and substring in arr[j]:
                            is_uncommon = False
                            break
                    
                    if is_uncommon:
                        result.append(substring)
                        found = True
                        break
            
            if not found:
                result.append("")
        
        return result
    
    def shortestUncommonSubstring_optimized(self, arr: list[str]) -> list[str]:
        """
        Optimized version using substring sets for faster lookup.
        """
        n = len(arr)
        
        # Precompute all substrings for each string (except current)
        substring_sets = []
        for i in range(n):
            substrings = set()
            s = arr[i]
            for length in range(1, len(s) + 1):
                for start in range(len(s) - length + 1):
                    substrings.add(s[start:start + length])
            substring_sets.append(substrings)
        
        result = []
        
        for i in range(n):
            s = arr[i]
            found = False
            
            # Generate substrings of s in order of length
            for length in range(1, len(s) + 1):
                if found:
                    break
                
                for start in range(len(s) - length + 1):
                    substring = s[start:start + length]
                    
                    # Check if substring appears in any other string's set
                    is_uncommon = True
                    for j in range(n):
                        if i != j and substring in substring_sets[j]:
                            is_uncommon = False
                            break
                    
                    if is_uncommon:
                        result.append(substring)
                        found = True
                        break
            
            if not found:
                result.append("")
        
        return result


def test_shortest_uncommon_substring():
    """Test cases for Shortest Uncommon Substring"""
    sol = Solution()
    
    # Test case 1: Example 1
    arr1 = ["cab","ad","bad","c"]
    result1 = sol.shortestUncommonSubstring(arr1)
    expected1 = ["ab","","ba",""]
    assert result1 == expected1, f"Expected {expected1}, got {result1}"
    print(f"✓ Test 1: arr={arr1}")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    arr2 = ["abc","bcd","abcd"]
    result2 = sol.shortestUncommonSubstring(arr2)
    expected2 = ["","","abc"]
    assert result2 == expected2, f"Expected {expected2}, got {result2}"
    print(f"✓ Test 2: arr={arr2}")
    print(f"  Result: {result2}")
    
    # Test case 3: All strings same
    arr3 = ["abc","abc","abc"]
    result3 = sol.shortestUncommonSubstring(arr3)
    expected3 = ["","",""]
    assert result3 == expected3, f"Expected {expected3}, got {result3}"
    print(f"✓ Test 3: All strings same")
    print(f"  Result: {result3}")
    
    # Test case 4: Single character strings
    arr4 = ["a","b","c"]
    result4 = sol.shortestUncommonSubstring(arr4)
    assert result4 == ["a","b","c"], f"Expected ['a','b','c'], got {result4}"
    print(f"✓ Test 4: Single characters")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_shortest_uncommon_substring()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    arr = ["cab","ad","bad","c"]
    result = sol.shortestUncommonSubstring(arr)
    print(f"Input: {arr}")
    print(f"Output: {result}")
# %%

