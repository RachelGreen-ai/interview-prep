# LeetCode 76: Minimum Window Substring
#%%
"""
Problem Statement:
Given two strings s and t, return the minimum window substring of s such that every character
in t (including duplicates) is included in the window. If there is no such substring, return "".

Examples:
- s = "ADOBECODEBANC", t = "ABC" -> "BANC"
- s = "a", t = "a" -> "a"
- s = "a", t = "aa" -> ""

INTERVIEW EXPLANATION: Why Sliding Window?

1. **We need a contiguous substring**: This screams "two pointers / sliding window".
2. **We need counts**: t can contain duplicates (e.g., "AABC"), so we track required counts.
3. **Greedy shrink**:
   - Expand right pointer until the window is valid (contains all required counts).
   - Then shrink left pointer as much as possible while keeping it valid.
   - Record the best (smallest) valid window seen.

Key idea:
- Maintain `need[c]` counts from t.
- Maintain `have[c]` counts in current window.
- Track `formed`: how many distinct chars currently satisfy `have[c] >= need[c]`.
- When `formed == required_distinct`, the window is valid.

Complexities:
- Time: O(len(s) + len(t)) (each pointer moves at most len(s) times)
- Space: O(|alphabet|) for count maps
"""

from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # Preferred approach: track remaining required chars via `missing`.
        if not s or not t:
            return ""

        need = Counter(t)
        missing = len(t)

        left = start = 0
        end = float("inf")

        for right, c in enumerate(s):
            if c in need:
                if need[c] > 0:
                    missing -= 1
                need[c] -= 1

            while missing == 0:
                if right - left < end - start:
                    start, end = left, right

                if s[left] in need:
                    need[s[left]] += 1
                    if need[s[left]] > 0:
                        missing += 1
                left += 1

        return "" if end == float("inf") else s[start : end + 1]


def test_minimum_window_substring():
    sol = Solution()

    # Example 1
    assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"

    # Example 2
    assert sol.minWindow("a", "a") == "a"

    # Example 3
    assert sol.minWindow("a", "aa") == ""

    # Edge: duplicates in t
    assert sol.minWindow("AAABBC", "AABC") == "AABBC"

    # Edge: exact match
    assert sol.minWindow("abc", "abc") == "abc"

    # Edge: t longer than s
    assert sol.minWindow("ab", "abc") == ""

    print("All tests passed!")


if __name__ == "__main__":
    test_minimum_window_substring()
# %%

