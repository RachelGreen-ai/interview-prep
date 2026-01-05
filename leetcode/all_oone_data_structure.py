# LeetCode 432: All O`one Data Structure
#%%
"""
Problem Statement:
Design a data structure to store the counts of strings with the ability to return the strings
with minimum and maximum counts.

Implement the AllOne class:
- AllOne() Initializes the object of the data structure.
- void inc(String key) Increments the count of the string key by 1. If key does not exist
  in the data structure, insert it with count 1.
- void dec(String key) Decrements the count of the string key by 1. If the count of key is 0
  after the decrement, remove it from the data structure. It is guaranteed that key exists
  in the data structure before the decrement.
- String getMaxKey() Returns one of the keys with the maximal count. If no element exists,
  return an empty string "".
- String getMinKey() Returns one of the keys with the minimal count. If no element exists,
  return an empty string "".

Note that each function must run in O(1) average time.

Example:
Input:
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["world"], [], []]
Output: [null, null, null, "hello", "hello", null, "hello", "world"]

Explanation:
AllOne allOne = new AllOne();
allOne.inc("hello");
allOne.inc("hello");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "hello"
allOne.inc("world");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "world"

INTERVIEW EXPLANATION: Why Doubly Linked List + HashMap for All O`one?

1. **Problem Structure**: We need O(1) operations for:
   - Increment/decrement counts
   - Get max/min key
   - This requires tracking keys by their count values

2. **Why Doubly Linked List + HashMap?**
   - **Count Buckets**: Group keys by their count in linked list nodes
   - **Fast Access**: HashMap from key -> node for O(1) lookup
   - **Ordered Structure**: DLL maintains order of counts (min to max)
   - **O(1) Operations**: All operations can be done in O(1) with proper structure

3. **Data Structure Design**:
   - HashMap: key -> (count, node reference)
   - Doubly Linked List: nodes containing (count, set of keys)
   - Head points to node with minimum count
   - Tail points to node with maximum count
   - Each node has set of keys with that count

4. **Algorithm**:
   - inc(key): Find node for current count, move key to next count node (or create)
   - dec(key): Find node for current count, move key to previous count node (or create)
   - getMaxKey(): Return any key from tail node's set
   - getMinKey(): Return any key from head node's set

5. **Key Insights**:
   - Use DLL to maintain sorted order of counts
   - Each node stores a set of keys with the same count
   - When count changes, move key between nodes
   - Remove empty nodes to maintain structure

6. **Time Complexity**: O(1) for all operations
   
7. **Space Complexity**: O(n) where n is number of keys
"""

from collections import defaultdict


class Node:
    """Node in doubly linked list representing a count bucket."""
    def __init__(self, count: int):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None


class AllOne:
    """All O`one Data Structure"""
    
    def __init__(self):
        """Initialize the data structure."""
        # HashMap: key -> Node
        self.key_to_node = {}
        
        # Doubly linked list: head (min count) <-> ... <-> tail (max count)
        self.head = Node(0)  # Dummy head
        self.tail = Node(float('inf'))  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node_after(self, node: Node, count: int) -> Node:
        """Add a new node with given count after the given node."""
        new_node = Node(count)
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node
        return new_node
    
    def _remove_node(self, node: Node):
        """Remove a node from the linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _remove_key_from_node(self, node: Node, key: str):
        """Remove key from node's set and remove node if empty."""
        node.keys.discard(key)
        if not node.keys and node.count != 0 and node.count != float('inf'):
            self._remove_node(node)
    
    def inc(self, key: str) -> None:
        """
        Increment count of key by 1.
        
        Args:
            key: String key to increment
        """
        if key not in self.key_to_node:
            # Key doesn't exist, add to count 1 node
            if self.head.next.count != 1:
                # Create count 1 node
                node = self._add_node_after(self.head, 1)
            else:
                node = self.head.next
            node.keys.add(key)
            self.key_to_node[key] = node
        else:
            # Key exists, move to next count
            current_node = self.key_to_node[key]
            new_count = current_node.count + 1
            
            # Remove from current node
            self._remove_key_from_node(current_node, key)
            
            # Add to next count node
            if current_node.next.count == new_count:
                # Next node has the right count
                next_node = current_node.next
            else:
                # Create new node
                next_node = self._add_node_after(current_node, new_count)
            
            next_node.keys.add(key)
            self.key_to_node[key] = next_node
    
    def dec(self, key: str) -> None:
        """
        Decrement count of key by 1.
        
        Args:
            key: String key to decrement (guaranteed to exist)
        """
        current_node = self.key_to_node[key]
        new_count = current_node.count - 1
        
        # Remove from current node
        self._remove_key_from_node(current_node, key)
        
        if new_count == 0:
            # Remove key completely
            del self.key_to_node[key]
        else:
            # Add to previous count node
            if current_node.prev.count == new_count:
                # Previous node has the right count
                prev_node = current_node.prev
            else:
                # Create new node
                prev_node = self._add_node_after(current_node.prev, new_count)
            
            prev_node.keys.add(key)
            self.key_to_node[key] = prev_node
    
    def getMaxKey(self) -> str:
        """
        Get a key with maximum count.
        
        Returns:
            A key with max count, or "" if empty
        """
        if self.tail.prev == self.head:
            return ""
        # Return any key from tail's previous node (max count node)
        return next(iter(self.tail.prev.keys))
    
    def getMinKey(self) -> str:
        """
        Get a key with minimum count.
        
        Returns:
            A key with min count, or "" if empty
        """
        if self.head.next == self.tail:
            return ""
        # Return any key from head's next node (min count node)
        return next(iter(self.head.next.keys))


def test_all_one():
    """Test cases for All O`one Data Structure"""
    # Test case 1: Example from problem
    all_one = AllOne()
    all_one.inc("hello")
    all_one.inc("hello")
    assert all_one.getMaxKey() == "hello", "Max key should be hello"
    assert all_one.getMinKey() == "hello", "Min key should be hello"
    all_one.inc("world")
    assert all_one.getMaxKey() == "hello", "Max key should be hello"
    assert all_one.getMinKey() == "world", "Min key should be world"
    print("✓ Test 1: Example from problem")
    
    # Test case 2: Multiple increments
    all_one2 = AllOne()
    all_one2.inc("a")
    all_one2.inc("a")
    all_one2.inc("b")
    assert all_one2.getMaxKey() == "a", "Max should be a"
    assert all_one2.getMinKey() == "b", "Min should be b"
    print("✓ Test 2: Multiple increments")
    
    # Test case 3: Decrement to zero
    all_one3 = AllOne()
    all_one3.inc("x")
    all_one3.dec("x")
    assert all_one3.getMaxKey() == "", "Should be empty"
    assert all_one3.getMinKey() == "", "Should be empty"
    print("✓ Test 3: Decrement to zero")
    
    # Test case 4: Complex operations
    all_one4 = AllOne()
    all_one4.inc("a")
    all_one4.inc("b")
    all_one4.inc("b")
    all_one4.inc("c")
    all_one4.inc("c")
    all_one4.inc("c")
    assert all_one4.getMaxKey() == "c", "Max should be c"
    assert all_one4.getMinKey() == "a", "Min should be a"
    all_one4.dec("c")
    assert all_one4.getMaxKey() in ["b", "c"], "Max should be b or c"
    print("✓ Test 4: Complex operations")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_all_one()
    
    # Example usage
    print("\nExample usage:")
    all_one = AllOne()
    
    all_one.inc("hello")
    all_one.inc("hello")
    print(f"After inc('hello') twice:")
    print(f"  Max key: {all_one.getMaxKey()}")
    print(f"  Min key: {all_one.getMinKey()}")
    
    all_one.inc("world")
    print(f"After inc('world'):")
    print(f"  Max key: {all_one.getMaxKey()}")
    print(f"  Min key: {all_one.getMinKey()}")
# %%

