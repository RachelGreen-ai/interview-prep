# LeetCode 160: Intersection of Two Linked Lists
#%%
"""
Problem Statement:
Given the heads of two singly linked-lists headA and headB, return the node at
which the two lists intersect. If the two linked lists have no intersection at
all, return null.

The test cases are generated such that there are no cycles anywhere in the
entire linked structure.

Note that the linked lists must retain their original structure after the
function returns.

Example 1:
Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]
       skipA = 2, skipB = 3
Output: Intersected at '8'
Explanation: The two lists intersect at node with value 8.

Example 2:
Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4]
       skipA = 3, skipB = 1
Output: Intersected at '2'

INTERVIEW EXPLANATION: Why Two-Pointer Technique?

1. **Problem Structure**: Two linked lists may have different lengths before
   the intersection point. We need to find where they meet.

2. **Why Two-Pointer Technique?**
   - **Key Insight**: If we traverse both lists simultaneously, the pointers
     will reach the intersection at the same time only if the lists have the
     same length. Otherwise, we need to align them.
   
   - **Approach 1: Calculate Lengths**
     * Find lengths of both lists
     * Move longer list's pointer forward by the difference
     * Then move both pointers together until they meet
     * Time: O(m + n), Space: O(1)
   
   - **Approach 2: Two-Pointer Swap (Elegant)**
     * Use two pointers, one for each list
     * When one pointer reaches end, switch it to the other list's head
     * They will meet at intersection (or both become None)
     * Time: O(m + n), Space: O(1)
     * More elegant and doesn't require length calculation

3. **Key Insight**: The two-pointer swap technique works because:
   - Pointer A travels: listA + listB (if no intersection)
   - Pointer B travels: listB + listA (if no intersection)
   - They cover the same total distance, so they meet at intersection
   - If no intersection, both become None simultaneously

4. **Why This Works**:
   - If lists intersect: both pointers will reach intersection after
     traveling (lenA + lenB - common) nodes
   - If lists don't intersect: both pointers become None after
     traveling (lenA + lenB) nodes
"""

from typing import Optional


class ListNode:
    """Definition for singly-linked list node"""
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    """Solution for Intersection of Two Linked Lists"""
    
    def getIntersectionNode_length(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        """
        Solution by calculating lengths first.
        
        Args:
            headA: Head of first linked list
            headB: Head of second linked list
            
        Returns:
            Intersection node, or None if no intersection
        """
        def get_length(head: ListNode) -> int:
            length = 0
            while head:
                length += 1
                head = head.next
            return length
        
        lenA = get_length(headA)
        lenB = get_length(headB)
        
        # Move longer list's pointer forward
        ptrA, ptrB = headA, headB
        if lenA > lenB:
            for _ in range(lenA - lenB):
                ptrA = ptrA.next
        else:
            for _ in range(lenB - lenA):
                ptrB = ptrB.next
        
        # Move both pointers together
        while ptrA and ptrB:
            if ptrA == ptrB:
                return ptrA
            ptrA = ptrA.next
            ptrB = ptrB.next
        
        return None
    
    def getIntersectionNode_swap(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        """
        Elegant two-pointer solution with swapping.
        More interview-friendly - no length calculation needed.
        
        Args:
            headA: Head of first linked list
            headB: Head of second linked list
            
        Returns:
            Intersection node, or None if no intersection
        """
        ptrA, ptrB = headA, headB
        
        while ptrA != ptrB:
            # Move to next node, or switch to other list's head
            ptrA = ptrA.next if ptrA else headB
            ptrB = ptrB.next if ptrB else headA
        
        # Either both are None (no intersection) or both point to intersection
        return ptrA


def test_intersection():
    """Test cases for Intersection of Two Linked Lists"""
    sol = Solution()
    
    # Test case 1: Example 1
    # Create lists: A = [4,1,8,4,5], B = [5,6,1,8,4,5]
    # Intersect at node with value 8
    common = ListNode(8)
    common.next = ListNode(4)
    common.next.next = ListNode(5)
    
    headA1 = ListNode(4)
    headA1.next = ListNode(1)
    headA1.next.next = common
    
    headB1 = ListNode(5)
    headB1.next = ListNode(6)
    headB1.next.next = ListNode(1)
    headB1.next.next.next = common
    
    result1_l = sol.getIntersectionNode_length(headA1, headB1)
    result1_s = sol.getIntersectionNode_swap(headA1, headB1)
    assert result1_l == common, f"Length method: Expected intersection, got {result1_l}"
    assert result1_s == common, f"Swap method: Expected intersection, got {result1_s}"
    assert result1_l.val == 8, f"Expected value 8, got {result1_l.val}"
    print(f"✓ Test 1: Found intersection at node with value {result1_l.val}")
    
    # Test case 2: No intersection
    headA2 = ListNode(2)
    headA2.next = ListNode(6)
    headA2.next.next = ListNode(4)
    
    headB2 = ListNode(1)
    headB2.next = ListNode(5)
    
    result2_l = sol.getIntersectionNode_length(headA2, headB2)
    result2_s = sol.getIntersectionNode_swap(headA2, headB2)
    assert result2_l is None, f"Length method: Expected None, got {result2_l}"
    assert result2_s is None, f"Swap method: Expected None, got {result2_s}"
    print("✓ Test 2: No intersection (correct)")
    
    # Test case 3: Same list
    headA3 = ListNode(1)
    headA3.next = ListNode(2)
    headB3 = headA3
    
    result3_l = sol.getIntersectionNode_length(headA3, headB3)
    result3_s = sol.getIntersectionNode_swap(headA3, headB3)
    assert result3_l == headA3, f"Length method: Expected head, got {result3_l}"
    assert result3_s == headA3, f"Swap method: Expected head, got {result3_s}"
    print("✓ Test 3: Same list (intersect at head)")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_intersection()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    # Create example lists
    common = ListNode(8)
    common.next = ListNode(4)
    common.next.next = ListNode(5)
    
    headA = ListNode(4)
    headA.next = ListNode(1)
    headA.next.next = common
    
    headB = ListNode(5)
    headB.next = ListNode(6)
    headB.next.next = ListNode(1)
    headB.next.next.next = common
    
    result = sol.getIntersectionNode_swap(headA, headB)
    if result:
        print(f"Lists intersect at node with value: {result.val}")
    else:
        print("Lists do not intersect")
# %%

