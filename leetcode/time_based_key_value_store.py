# LeetCode 981: Time Based Key-Value Store
#%%
"""
Problem Statement:
Design a time-based key-value data structure that can store multiple values for the same key
at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:
- TimeMap() Initializes the object of the data structure.
- void set(String key, String value, int timestamp) Stores the key with the value value
  at the given timestamp.
- String get(String key, int timestamp) Returns a value such that set was called previously,
  with timestamp_prev <= timestamp. If there are multiple such values, it returns the value
  associated with the largest timestamp_prev. If there are no values, it returns "".

Example 1:
Input:
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
Output: [null, null, "bar", "bar", null, "bar2", "bar2"]

Explanation:
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);  // return "bar"
timeMap.get("foo", 3);  // return "bar", since there is no value corresponding to foo at timestamp 3
                         // and the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);  // return "bar2"
timeMap.get("foo", 5);  // return "bar2"

INTERVIEW EXPLANATION: Why Binary Search for Time Based Key-Value Store?

1. **Problem Structure**: For each key, we store multiple (value, timestamp) pairs.
   When querying, we need to find the value with the largest timestamp <= query timestamp.

2. **Why Binary Search?**
   - **Sorted Data**: Timestamps are naturally increasing (set is called in chronological order)
   - **Range Query**: Find largest timestamp <= query timestamp
   - **Efficiency**: O(log n) lookup instead of O(n) linear search
   - **Data Structure**: Use list of (timestamp, value) pairs for each key

3. **Algorithm**:
   - set(key, value, timestamp): Append (timestamp, value) to key's list
   - get(key, timestamp): Binary search in key's list for largest timestamp <= query
   - Since timestamps are increasing, we can use binary search

4. **Key Insights**:
   - Store values in chronological order (timestamps are increasing)
   - Binary search for "largest element <= target"
   - If no valid timestamp found, return ""

5. **Time Complexity**:
   - set: O(1) - append to list
   - get: O(log n) - binary search where n is number of values for the key
   
6. **Space Complexity**: O(n) where n is total number of set operations
"""

from collections import defaultdict


class TimeMap:
    """Time Based Key-Value Store"""
    
    def __init__(self):
        """Initialize the data structure."""
        # Map: key -> list of (timestamp, value) pairs
        # Since set is called in chronological order, timestamps are sorted
        self.store = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Store key-value pair with timestamp.
        
        Args:
            key: Key string
            value: Value string
            timestamp: Timestamp (increasing order)
        """
        self.store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Get value for key at given timestamp.
        
        Args:
            key: Key string
            timestamp: Query timestamp
            
        Returns:
            Value with largest timestamp <= query timestamp, or "" if none
        """
        if key not in self.store:
            return ""
        
        values = self.store[key]
        
        # Binary search for largest timestamp <= query timestamp
        left, right = 0, len(values) - 1
        result = ""
        
        while left <= right:
            mid = (left + right) // 2
            mid_timestamp, mid_value = values[mid]
            
            if mid_timestamp <= timestamp:
                # Valid timestamp, update result and search right
                result = mid_value
                left = mid + 1
            else:
                # Timestamp too large, search left
                right = mid - 1
        
        return result
    
    def get_linear(self, key: str, timestamp: int) -> str:
        """
        Linear search version (for comparison).
        Time: O(n)
        """
        if key not in self.store:
            return ""
        
        values = self.store[key]
        result = ""
        
        # Since timestamps are sorted, iterate from end
        for i in range(len(values) - 1, -1, -1):
            ts, val = values[i]
            if ts <= timestamp:
                return val
        
        return result


def test_time_map():
    """Test cases for Time Based Key-Value Store"""
    # Test case 1: Example from problem
    time_map = TimeMap()
    time_map.set("foo", "bar", 1)
    assert time_map.get("foo", 1) == "bar", "Get at timestamp 1"
    assert time_map.get("foo", 3) == "bar", "Get at timestamp 3"
    time_map.set("foo", "bar2", 4)
    assert time_map.get("foo", 4) == "bar2", "Get at timestamp 4"
    assert time_map.get("foo", 5) == "bar2", "Get at timestamp 5"
    print("✓ Test 1: Example from problem")
    
    # Test case 2: Query before any timestamp
    time_map2 = TimeMap()
    time_map2.set("key", "value", 10)
    assert time_map2.get("key", 5) == "", "Query before any timestamp"
    print("✓ Test 2: Query before any timestamp")
    
    # Test case 3: Multiple values
    time_map3 = TimeMap()
    time_map3.set("a", "v1", 1)
    time_map3.set("a", "v2", 2)
    time_map3.set("a", "v3", 3)
    assert time_map3.get("a", 2) == "v2", "Get at exact timestamp"
    assert time_map3.get("a", 2) == "v2", "Get at timestamp 2"
    assert time_map3.get("a", 4) == "v3", "Get at timestamp 4"
    print("✓ Test 3: Multiple values")
    
    # Test case 4: Non-existent key
    time_map4 = TimeMap()
    assert time_map4.get("nonexistent", 1) == "", "Non-existent key"
    print("✓ Test 4: Non-existent key")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_time_map()
    
    # Example usage
    print("\nExample usage:")
    time_map = TimeMap()
    
    time_map.set("foo", "bar", 1)
    print(f"Set foo=bar at timestamp 1")
    
    print(f"Get foo at timestamp 1: {time_map.get('foo', 1)}")
    print(f"Get foo at timestamp 3: {time_map.get('foo', 3)}")
    
    time_map.set("foo", "bar2", 4)
    print(f"Set foo=bar2 at timestamp 4")
    
    print(f"Get foo at timestamp 4: {time_map.get('foo', 4)}")
    print(f"Get foo at timestamp 5: {time_map.get('foo', 5)}")
# %%

