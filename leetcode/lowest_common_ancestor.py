# LeetCode 236: Lowest Common Ancestor of a Binary Tree
#%%
"""
Problem Statement:
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between
two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow
a node to be a descendant of itself)."

Example 1:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself
according to the LCA definition.

Example 3:
Input: root = [1,2], p = 1, q = 2
Output: 1

INTERVIEW EXPLANATION: Why DFS for Lowest Common Ancestor?

1. **Problem Structure**: We need to find the deepest node that is an ancestor of both p and q.
   This requires traversing the tree and tracking where we find p and q.

2. **Why DFS?**
   - **Tree Traversal**: Need to explore the tree to find p and q
   - **Bottom-Up**: After finding p and q, propagate information upward
   - **Recursive Structure**: Natural fit for tree problems
   - **Single Pass**: Can find LCA in one traversal

3. **Algorithm**:
   a. DFS from root
   b. If current node is None, return None
   c. If current node is p or q, return current node
   d. Recursively search left and right subtrees
   e. If both left and right return non-None, current node is LCA
   f. Otherwise, return whichever subtree found a node (or None)

4. **Key Insights**:
   - If we find p in left subtree and q in right subtree, current node is LCA
   - If both p and q in same subtree, LCA is in that subtree
   - If current node is p or q, it might be the LCA (if other is in subtree)

5. **Time Complexity**: O(n) - visit each node at most once
   
6. **Space Complexity**: O(h) where h is height (recursion stack)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    """Solution for Lowest Common Ancestor"""
    
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Find lowest common ancestor of p and q.
        
        Args:
            root: Root of binary tree
            p: First node
            q: Second node
            
        Returns:
            Lowest common ancestor node
        """
        # Base cases
        if root is None:
            return None
        
        # If we found p or q, return it
        if root == p or root == q:
            return root
        
        # Search in left and right subtrees
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        
        # If both subtrees return non-None, current node is LCA
        if left and right:
            return root
        
        # Otherwise, return whichever subtree found a node
        return left if left else right
    
    def lowestCommonAncestor_verbose(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        More verbose version with detailed comments.
        """
        # Base case: empty tree
        if not root:
            return None
        
        # Case 1: Current node is one of p or q
        # This node might be the LCA if the other node is in its subtree
        if root == p or root == q:
            return root
        
        # Recursively search in left and right subtrees
        left_result = self.lowestCommonAncestor_verbose(root.left, p, q)
        right_result = self.lowestCommonAncestor_verbose(root.right, p, q)
        
        # Case 2: p and q are in different subtrees
        # Current node is the LCA
        if left_result and right_result:
            return root
        
        # Case 3: Both p and q are in the same subtree
        # Return the result from that subtree (which is the LCA)
        if left_result:
            return left_result
        if right_result:
            return right_result
        
        # Case 4: Neither p nor q found in this subtree
        return None


def test_lowest_common_ancestor():
    """Test cases for Lowest Common Ancestor"""
    # Note: Creating full test cases requires building trees
    # This is a simplified test structure
    
    sol = Solution()
    
    # Test case 1: Example 1 structure
    # Tree: [3,5,1,6,2,0,8,null,null,7,4]
    # p = 5, q = 1, LCA = 3
    root1 = TreeNode(3)
    root1.left = TreeNode(5)
    root1.right = TreeNode(1)
    root1.left.left = TreeNode(6)
    root1.left.right = TreeNode(2)
    root1.right.left = TreeNode(0)
    root1.right.right = TreeNode(8)
    root1.left.right.left = TreeNode(7)
    root1.left.right.right = TreeNode(4)
    
    p1 = root1.left  # 5
    q1 = root1.right  # 1
    result1 = sol.lowestCommonAncestor(root1, p1, q1)
    assert result1 == root1, f"Expected root (3), got {result1.val if result1 else None}"
    print(f"✓ Test 1: p=5, q=1, LCA={result1.val}")
    
    # Test case 2: Example 2
    # p = 5, q = 4, LCA = 5
    p2 = root1.left  # 5
    q2 = root1.left.right.right  # 4
    result2 = sol.lowestCommonAncestor(root1, p2, q2)
    assert result2 == p2, f"Expected 5, got {result2.val if result2 else None}"
    print(f"✓ Test 2: p=5, q=4, LCA={result2.val}")
    
    # Test case 3: Example 3
    # Tree: [1,2]
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    p3 = root3  # 1
    q3 = root3.left  # 2
    result3 = sol.lowestCommonAncestor(root3, p3, q3)
    assert result3 == root3, f"Expected 1, got {result3.val if result3 else None}"
    print(f"✓ Test 3: p=1, q=2, LCA={result3.val}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_lowest_common_ancestor()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    # Build example tree
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    
    p = root.left  # 5
    q = root.right  # 1
    lca = sol.lowestCommonAncestor(root, p, q)
    print(f"LCA of {p.val} and {q.val} is {lca.val}")
# %%

