# LeetCode 622: Design Circular Queue
#%%
"""
Problem Statement:
Design your implementation of the circular queue. The circular queue is a linear data structure
in which the operations are performed based on FIFO (First In First Out) principle and the last
position is connected back to the first position to make a circle. It is also called "Ring Buffer".

One of the benefits of the circular queue is that we can make use of the spaces in front of the
queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if
there is a space in front of the queue. But using the circular queue, we can use the space to
store new values.

Implement the MyCircularQueue class:
- MyCircularQueue(int k) Initializes the object with the size of the queue to be k.
- boolean enQueue(int value) Inserts an element into the circular queue. Return true if the
  operation is successful.
- boolean deQueue() Deletes an element from the circular queue. Return true if the operation
  is successful.
- int Front() Gets the front item from the queue. If the queue is empty, return -1.
- int Rear() Gets the last item from the queue. If the queue is empty, return -1.
- boolean isEmpty() Returns true if the queue is empty.
- boolean isFull() Returns true if the queue is full.

Example 1:
Input:
["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
Output: [null, true, true, true, false, 3, true, true, true, 4]

Explanation:
MyCircularQueue myCircularQueue = new MyCircularQueue(3);
myCircularQueue.enQueue(1); // return True
myCircularQueue.enQueue(2); // return True
myCircularQueue.enQueue(3); // return True
myCircularQueue.enQueue(4); // return False, the queue is full
myCircularQueue.Rear();     // return 3
myCircularQueue.isFull();   // return True
myCircularQueue.deQueue();  // return True
myCircularQueue.enQueue(4); // return True
myCircularQueue.Rear();     // return 4

INTERVIEW EXPLANATION: Why Array with Two Pointers for Circular Queue?

1. **Problem Structure**: We need a FIFO queue with fixed size that wraps around.
   When the queue reaches the end, it should continue from the beginning.

2. **Why Array with Two Pointers?**
   - **Fixed Size**: Array provides fixed-size storage
   - **Circular Wrapping**: Use modulo arithmetic to wrap indices
   - **Two Pointers**: front (head) and rear (tail) track queue boundaries
   - **Efficient**: O(1) for all operations

3. **Implementation Details**:
   - Use array of size k
   - front: index of first element
   - rear: index of last element
   - size: current number of elements (to distinguish full from empty)
   - Enqueue: add at (rear + 1) % k
   - Dequeue: remove from front, move front = (front + 1) % k

4. **Key Insights**:
   - Use size counter to distinguish full (size == k) from empty (size == 0)
   - Modulo arithmetic handles wrapping: (index + 1) % k
   - Empty: size == 0
   - Full: size == k

5. **Time Complexity**: O(1) for all operations
   
6. **Space Complexity**: O(k) for the array
"""


class MyCircularQueue:
    """Design Circular Queue"""
    
    def __init__(self, k: int):
        """
        Initialize circular queue with size k.
        
        Args:
            k: Maximum size of queue
        """
        self.k = k
        self.queue = [0] * k
        self.front = 0  # Index of front element
        self.rear = -1  # Index of rear element
        self.size = 0  # Current number of elements
    
    def enQueue(self, value: int) -> bool:
        """
        Insert element into circular queue.
        
        Args:
            value: Value to insert
            
        Returns:
            True if successful, False if queue is full
        """
        if self.isFull():
            return False
        
        # Move rear pointer and insert
        self.rear = (self.rear + 1) % self.k
        self.queue[self.rear] = value
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        """
        Delete element from circular queue.
        
        Returns:
            True if successful, False if queue is empty
        """
        if self.isEmpty():
            return False
        
        # Move front pointer
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True
    
    def Front(self) -> int:
        """
        Get front item from queue.
        
        Returns:
            Front item, or -1 if empty
        """
        if self.isEmpty():
            return -1
        return self.queue[self.front]
    
    def Rear(self) -> int:
        """
        Get last item from queue.
        
        Returns:
            Last item, or -1 if empty
        """
        if self.isEmpty():
            return -1
        return self.queue[self.rear]
    
    def isEmpty(self) -> bool:
        """Check if queue is empty."""
        return self.size == 0
    
    def isFull(self) -> bool:
        """Check if queue is full."""
        return self.size == self.k


def test_circular_queue():
    """Test cases for Circular Queue"""
    # Test case 1: Example from problem
    queue = MyCircularQueue(3)
    assert queue.enQueue(1) == True, "Enqueue 1"
    assert queue.enQueue(2) == True, "Enqueue 2"
    assert queue.enQueue(3) == True, "Enqueue 3"
    assert queue.enQueue(4) == False, "Queue full"
    assert queue.Rear() == 3, "Rear should be 3"
    assert queue.isFull() == True, "Queue should be full"
    assert queue.deQueue() == True, "Dequeue"
    assert queue.enQueue(4) == True, "Enqueue 4"
    assert queue.Rear() == 4, "Rear should be 4"
    print("✓ Test 1: Example from problem")
    
    # Test case 2: Empty queue
    queue2 = MyCircularQueue(2)
    assert queue2.isEmpty() == True, "Should be empty"
    assert queue2.Front() == -1, "Front should be -1"
    assert queue2.Rear() == -1, "Rear should be -1"
    print("✓ Test 2: Empty queue")
    
    # Test case 3: Single element
    queue3 = MyCircularQueue(1)
    assert queue3.enQueue(5) == True, "Enqueue"
    assert queue3.Front() == 5, "Front should be 5"
    assert queue3.Rear() == 5, "Rear should be 5"
    assert queue3.isFull() == True, "Should be full"
    print("✓ Test 3: Single element")
    
    # Test case 4: Wrap around
    queue4 = MyCircularQueue(2)
    queue4.enQueue(1)
    queue4.enQueue(2)
    queue4.deQueue()
    queue4.enQueue(3)
    assert queue4.Front() == 2, "Front after wrap"
    assert queue4.Rear() == 3, "Rear after wrap"
    print("✓ Test 4: Wrap around")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_circular_queue()
    
    # Example usage
    print("\nExample usage:")
    queue = MyCircularQueue(3)
    
    print(f"Enqueue 1: {queue.enQueue(1)}")
    print(f"Enqueue 2: {queue.enQueue(2)}")
    print(f"Enqueue 3: {queue.enQueue(3)}")
    print(f"Is full: {queue.isFull()}")
    print(f"Front: {queue.Front()}")
    print(f"Rear: {queue.Rear()}")
    print(f"Dequeue: {queue.deQueue()}")
    print(f"Enqueue 4: {queue.enQueue(4)}")
    print(f"Rear: {queue.Rear()}")
# %%

