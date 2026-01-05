# LeetCode 337: House Robber III
#%%
"""
Problem Statement:
The thief has found himself a new place for his thievery again. There is only one
entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour, the
smart thief realized that all houses in this place form a binary tree. It will
automatically contact the police if two directly-linked houses were broken into
on the same night.

Given the root of the binary tree, return the maximum amount of money the thief
can rob without alerting the police.

Example:
Tree:
      3
     / \
    2   3
     \   \
      3   1

Output: 7
Explanation: Rob houses 3 (root) + 3 (left.right) + 1 (right.right) = 7.

INTERVIEW EXPLANATION: Why Tree DP with Two States?

1. **Problem Structure**: At each node, we have two choices:
   - Rob this node → cannot rob its children, but can rob grandchildren
   - Skip this node → can rob its children
   
   This is a tree DP problem with recursive structure.

2. **Why Two States Per Node?**
   - **State Definition**: For each node, we return two values:
     * rob_this: max money if we rob this node
     * skip_this: max money if we skip this node
   
   - **Recurrence**:
     * rob_this = node.val + skip(left) + skip(right)
     * skip_this = max(left) + max(right)
     * Where max(child) = max(rob_child, skip_child)
   
   - **Time Complexity**: O(n) - visit each node once
   - **Space Complexity**: O(h) where h = height (recursion stack)
     * Worst case O(n) for skewed tree
     * O(log n) for balanced tree

3. **Key Insight**: By returning both states (rob/skip) from each subtree,
   we can compute the optimal solution for the parent without recomputation.
   This is the elegant DP solution interviewers love.

4. **Base Case**: If node is None, return (0, 0) - no money to rob or skip.
"""

from typing import Optional, Tuple


class TreeNode:
    """Definition for a binary tree node"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Solution for House Robber III"""
    
    def rob(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum amount of money that can be robbed from binary tree.
        
        Args:
            root: Root of the binary tree
            
        Returns:
            Maximum amount that can be robbed
        """
        def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
            """
            DFS to compute max money for subtree.
            
            Returns:
                Tuple of (rob_this, skip_this):
                - rob_this: max money if we rob this node
                - skip_this: max money if we skip this node
            """
            if not node:
                return (0, 0)  # (rob_this, skip_this)
            
            # Get states from left and right children
            left = dfs(node.left)
            right = dfs(node.right)
            
            # If rob this node → skip children
            rob_this = node.val + left[1] + right[1]
            
            # If skip this node → take best of children (can rob or skip)
            skip_this = max(left) + max(right)
            
            return (rob_this, skip_this)
        
        return max(dfs(root))


def test_house_robber_iii():
    """Test cases for House Robber III"""
    sol = Solution()
    
    # Test case 1: Example from problem
    # Tree:
    #      3
    #     / \
    #    2   3
    #     \   \
    #      3   1
    root1 = TreeNode(3)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.right = TreeNode(3)
    root1.right.right = TreeNode(1)
    
    result1 = sol.rob(root1)
    assert result1 == 7, f"Expected 7, got {result1}"
    print(f"✓ Test 1: Result = {result1} (rob root + left.right + right.right)")
    
    # Test case 2: Single node
    root2 = TreeNode(3)
    result2 = sol.rob(root2)
    assert result2 == 3, f"Expected 3, got {result2}"
    print(f"✓ Test 2: Single node → {result2}")
    
    # Test case 3: Two levels
    # Tree:
    #      3
    #     / \
    #    4   5
    root3 = TreeNode(3)
    root3.left = TreeNode(4)
    root3.right = TreeNode(5)
    result3 = sol.rob(root3)
    assert result3 == 9, f"Expected 9, got {result3}"  # Rob root (3) + skip children, or rob children (4+5)
    print(f"✓ Test 3: Two levels → {result3}")
    
    # Test case 4: Empty tree
    root4 = None
    result4 = sol.rob(root4)
    assert result4 == 0, f"Expected 0, got {result4}"
    print("✓ Test 4: Empty tree → 0")
    
    # Test case 5: Linear tree (all left children)
    # Tree:
    #      3
    #     /
    #    2
    #   /
    #  3
    root5 = TreeNode(3)
    root5.left = TreeNode(2)
    root5.left.left = TreeNode(3)
    result5 = sol.rob(root5)
    assert result5 == 6, f"Expected 6, got {result5}"  # Rob root (3) + grandchild (3)
    print(f"✓ Test 5: Linear tree → {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_house_robber_iii()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    # Build example tree
    root = TreeNode(3)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(1)
    
    result = sol.rob(root)
    print(f"Tree structure:")
    print("      3")
    print("     / \\")
    print("    2   3")
    print("     \\   \\")
    print("      3   1")
    print(f"\nMaximum amount: {result}")
    print("Explanation: Rob houses 3 (root) + 3 (left.right) + 1 (right.right) = 7")
# %%

