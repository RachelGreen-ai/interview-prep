# LeetCode 253: Meeting Rooms II
#%%
"""
Problem Statement:
Given an array of meeting time intervals where intervals[i] = [start_i, end_i],
return the minimum number of conference rooms required.

Example 1:
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
Explanation: We need two meeting rooms:
- Room 1: [0,30]
- Room 2: [5,10], [15,20]

Example 2:
Input: intervals = [[7,10],[2,4]]
Output: 1
Explanation: Meetings don't overlap, so one room is enough.

INTERVIEW EXPLANATION: Why Min-Heap for Meeting Rooms II?

1. **Problem Structure**: We need to find the minimum number of rooms needed
   to schedule all meetings without conflicts. When a meeting starts, we need
   to check if any previous meeting has ended.

2. **Why Min-Heap (Priority Queue)?**
   - **Key Insight**: Track the end times of ongoing meetings using a min-heap.
     The heap always gives us the earliest ending meeting.
   
   - **Algorithm**:
     * Sort meetings by start time
     * For each meeting:
       - If earliest ending meeting finishes before current starts → reuse room (pop heap)
       - Otherwise → need new room (push to heap)
     * Heap size = number of rooms in use
   
   - **Time Complexity**: O(n log n)
     * Sorting: O(n log n)
     * Heap operations: O(n log n) worst case
   
   - **Space Complexity**: O(n) for heap

3. **Alternative: Two Pointers**
   - Separate start and end times, sort them
   - Use two pointers to track ongoing meetings
   - Time: O(n log n), Space: O(n)
   - Min-heap is more intuitive and commonly used

4. **Key Insight**: The min-heap efficiently tracks which room becomes available
   first. When a new meeting starts, we check if we can reuse a room that just
   became available.
"""

import heapq
from typing import List


class Interval:
    """Interval class for meeting times"""
    def __init__(self, start, end):
        self.start = start
        self.end = end


class MeetingRooms:
    """Solution for Meeting Rooms II"""
    
    def __init__(self, intervals):
        self.intervals = intervals
    
    def minMeetingRooms(self) -> int:
        """
        Find minimum number of conference rooms required.
        
        Returns:
            Minimum number of rooms needed
        """
        if not self.intervals:
            return 0
        
        # Sort by start time
        self.intervals.sort(key=lambda x: x.start)
        
        # Min-heap stores end times of ongoing meetings
        heap = []
        
        for meeting in self.intervals:
            # If earliest ending meeting finishes before current starts, reuse room
            if heap and meeting.start >= heap[0]:
                heapq.heappop(heap)
            
            # Add current meeting's end time
            heapq.heappush(heap, meeting.end)
        
        # Heap size = number of rooms needed
        return len(heap)
    
    def minMeetingRooms_two_pointers(self) -> int:
        """
        Alternative solution using two pointers.
        
        Returns:
            Minimum number of rooms needed
        """
        if not self.intervals:
            return 0
        
        # Separate and sort start/end times
        starts = sorted([i.start for i in self.intervals])
        ends = sorted([i.end for i in self.intervals])
        
        s_ptr = 0
        e_ptr = 0
        rooms = 0
        max_rooms = 0
        
        while s_ptr < len(self.intervals):
            if starts[s_ptr] < ends[e_ptr]:
                # New meeting starts before one ends → need new room
                rooms += 1
                max_rooms = max(max_rooms, rooms)
                s_ptr += 1
            else:
                # A meeting ends → free a room
                rooms -= 1
                e_ptr += 1
        
        return max_rooms



def test_minrooms(inp, expected):
    result = MeetingRooms(inp).minMeetingRooms()
    assert result == expected, (
        f"\n[TEST FAILED]\n"
        f"Input:      {[(x.start, x.end) for x in inp]}\n"
        f"Expected:   {expected}\n"
        f"Got:        {result}\n"
    )


# Add script line for running directly
if __name__ == "__main__":
    test_minrooms([Interval(1,3), Interval(2,6)], 2)
    print("Manual test ran successfully.")

