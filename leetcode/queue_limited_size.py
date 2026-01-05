# Design Queue with Limited Size of Array
#%%
"""
Problem Statement:
Implement a queue (FIFO: first-in, first-out) with a restriction:
- Instead of one big dynamic array (like Python's list)
- We must store elements in fixed-size arrays (blocks), say length ≤ 5 or ≤ 10
- The queue itself has no limit in length — we just chain multiple blocks together
- This models memory allocation with limited-size blocks

INTERVIEW EXPLANATION: Why Linked List of Blocks?

1. **Problem Structure**: We need a queue that can grow/shrink, but each block
   has a fixed size. This simulates real-world memory allocation where memory
   is allocated in fixed-size pages/blocks.

2. **Why Linked List of Blocks?**
   - **Fixed Block Size**: Each block has a fixed capacity, preventing one
     large contiguous allocation. This is more memory-efficient and realistic.
   
   - **Dynamic Growth**: When a block is full, we allocate a new block and
     link it. When a block is empty, we can free it.
   
   - **Time Complexity**: 
     * Enqueue: O(1) amortized (O(1) to add to current block, O(1) to allocate new block)
     * Dequeue: O(1) amortized (O(1) to remove from current block, O(1) to free empty block)
   
   - **Space Complexity**: O(n) where n is number of elements, but memory is
     allocated in fixed-size chunks rather than one large array.

3. **Key Design Decisions**:
   - Use two pointers: head (for dequeue) and tail (for enqueue)
   - Each block tracks: data array, start index, end index, next pointer
   - When tail block is full → allocate new block
   - When head block is empty → free it and move to next block
"""

from typing import Optional, Any


class Block:
    """A fixed-size block that holds queue elements"""
    
    def __init__(self, capacity: int = 5):
        self.data: list = [None] * capacity
        self.capacity: int = capacity
        self.start: int = 0  # First valid element index
        self.end: int = 0    # Next free position
        self.next: Optional['Block'] = None
    
    def is_full(self) -> bool:
        """Check if block is full"""
        return self.end == self.capacity
    
    def is_empty(self) -> bool:
        """Check if block is empty"""
        return self.start == self.end
    
    def add(self, val: Any) -> None:
        """Add element to block"""
        if self.is_full():
            raise IndexError("Block is full")
        self.data[self.end] = val
        self.end += 1
    
    def remove(self) -> Any:
        """Remove and return element from block"""
        if self.is_empty():
            raise IndexError("Block is empty")
        val = self.data[self.start]
        self.data[self.start] = None  # Clear reference
        self.start += 1
        return val


class Queue:
    """Queue implemented using linked list of fixed-size blocks"""
    
    def __init__(self, block_size: int = 5):
        self.block_size: int = block_size
        self.head: Block = Block(block_size)
        self.tail: Block = self.head
    
    def enqueue(self, val: Any) -> None:
        """
        Add element to queue.
        If tail block is full, allocate a new block.
        """
        if self.tail.is_full():
            new_block = Block(self.block_size)
            self.tail.next = new_block
            self.tail = new_block
        self.tail.add(val)
    
    def dequeue(self) -> Any:
        """
        Remove and return element from queue.
        If head block becomes empty, free it and move to next block.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        val = self.head.remove()
        
        # Free empty block if it's not the only block
        if self.head.is_empty() and self.head.next is not None:
            # Move head to next block (old block will be garbage collected)
            self.head = self.head.next
        
        return val
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return self.head.is_empty() and self.head.next is None
    
    def size(self) -> int:
        """Get approximate size (for debugging)"""
        count = 0
        current = self.head
        while current:
            count += current.end - current.start
            current = current.next
        return count


def test_queue():
    """Test cases for Queue with Limited Size"""
    # Test basic operations
    q = Queue(block_size=3)
    
    # Enqueue 10 elements
    for i in range(10):
        q.enqueue(i)
    
    # Dequeue all elements
    result = []
    for _ in range(10):
        result.append(q.dequeue())
    
    assert result == list(range(10)), f"Expected [0..9], got {result}"
    assert q.is_empty(), "Queue should be empty"
    print(f"✓ Basic operations: {result}")
    
    # Test with block size 5
    q2 = Queue(block_size=5)
    for i in range(20):
        q2.enqueue(i * 2)
    
    result2 = []
    while not q2.is_empty():
        result2.append(q2.dequeue())
    
    expected = [i * 2 for i in range(20)]
    assert result2 == expected, f"Expected {expected}, got {result2}"
    print(f"✓ Large queue (20 elements, block_size=5): {len(result2)} elements")
    
    # Test empty queue
    q3 = Queue()
    try:
        q3.dequeue()
        assert False, "Should raise IndexError"
    except IndexError:
        print("✓ Empty queue dequeue raises IndexError")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_queue()
    
    # Example usage
    print("\nExample usage:")
    q = Queue(block_size=3)
    print("Enqueueing: 0, 1, 2, 3, 4, 5")
    for i in range(6):
        q.enqueue(i)
        print(f"  Enqueued {i}, queue size: {q.size()}")
    
    print("\nDequeueing:")
    while not q.is_empty():
        val = q.dequeue()
        print(f"  Dequeued {val}, queue size: {q.size()}")
# %%

