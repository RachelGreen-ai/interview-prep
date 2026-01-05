# LeetCode 759: Employee Free Time
#%%
"""
Problem Statement:
We are given a list schedule of employees, which represents the working time for each employee.
Each employee has a list of non-overlapping Intervals in sorted order.
Return a list of finite intervals representing common, positive-length free time for all employees,
also in sorted order.

(Even though we are representing Intervals in [start, end) format, the problem description
and the examples are using closed intervals [start, end]. For example, [1,3] represents
an interval that includes both 1 and 3.)

Example 1:
Input: schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]
Output: [[3,4]]
Explanation:
There are a total of three employees, and all common free time intervals would be [-inf, 1], [3, 4], [10, +inf].
We only care about the finite intervals, so we return [[3,4]].

Example 2:
Input: schedule = [[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]
Output: [[5,6],[7,9]]

INTERVIEW EXPLANATION: Why Merge Intervals for Employee Free Time?

1. **Problem Structure**: We need to find time intervals when ALL employees are free.
   This is equivalent to finding gaps in the union of all working intervals.

2. **Why Merge Intervals?**
   - **Union of Intervals**: First, we need to merge all working intervals from all employees
   - **Gap Finding**: Then find gaps between consecutive merged intervals
   - **Sorted Order**: Intervals are already sorted per employee, making merge efficient

3. **Algorithm**:
   a. Collect all intervals from all employees into one list
   b. Sort all intervals by start time
   c. Merge overlapping intervals
   d. Find gaps between consecutive merged intervals
   e. Return the gaps (these are free times for all employees)

4. **Key Insights**:
   - Free time = gaps in the union of all working intervals
   - If we merge all working intervals, gaps between them represent free time
   - We only care about finite intervals (not [-inf, ...] or [..., +inf])

5. **Time Complexity**: O(N log N) where N is total number of intervals
   - Sorting: O(N log N)
   - Merging: O(N)
   - Gap finding: O(N)

6. **Space Complexity**: O(N) for storing merged intervals
"""

from typing import List


# Definition for an Interval (provided by LeetCode)
class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"[{self.start}, {self.end}]"


class Solution:
    """Solution for Employee Free Time"""
    
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        """
        Find common free time intervals for all employees.
        
        Args:
            schedule: List of employee schedules, each is a list of Intervals
            
        Returns:
            List of free time intervals in sorted order
        """
        # Step 1: Collect all intervals from all employees
        all_intervals = []
        for employee_schedule in schedule:
            all_intervals.extend(employee_schedule)
        
        # Step 2: Sort by start time
        all_intervals.sort(key=lambda x: x.start)
        
        # Step 3: Merge overlapping intervals
        merged = []
        for interval in all_intervals:
            if not merged:
                merged.append(interval)
            else:
                last = merged[-1]
                # If current interval overlaps with last merged interval
                if interval.start <= last.end:
                    # Merge: update end time
                    last.end = max(last.end, interval.end)
                else:
                    # No overlap, add as new interval
                    merged.append(interval)
        
        # Step 4: Find gaps between consecutive merged intervals
        free_time = []
        for i in range(len(merged) - 1):
            # Gap between merged[i].end and merged[i+1].start
            gap_start = merged[i].end
            gap_end = merged[i + 1].start
            
            # Only add finite intervals (with positive length)
            if gap_start < gap_end:
                free_time.append(Interval(gap_start, gap_end))
        
        return free_time
    
    def employeeFreeTime_optimized(self, schedule: List[List[Interval]]) -> List[Interval]:
        """
        Optimized version using heap for merging intervals.
        """
        import heapq
        
        # Collect all intervals with employee index for tracking
        intervals = []
        for emp_idx, emp_schedule in enumerate(schedule):
            for interval in emp_schedule:
                intervals.append((interval.start, interval.end, emp_idx))
        
        # Sort by start time
        intervals.sort()
        
        # Merge overlapping intervals
        merged = []
        for start, end, _ in intervals:
            if not merged:
                merged.append([start, end])
            else:
                last_start, last_end = merged[-1]
                if start <= last_end:
                    # Overlap: merge
                    merged[-1][1] = max(last_end, end)
                else:
                    # No overlap: add new
                    merged.append([start, end])
        
        # Find gaps
        free_time = []
        for i in range(len(merged) - 1):
            gap_start = merged[i][1]
            gap_end = merged[i + 1][0]
            if gap_start < gap_end:
                free_time.append(Interval(gap_start, gap_end))
        
        return free_time


def test_employee_free_time():
    """Test cases for Employee Free Time"""
    sol = Solution()
    
    # Test case 1: Example 1
    schedule1 = [
        [Interval(1, 2), Interval(5, 6)],
        [Interval(1, 3)],
        [Interval(4, 10)]
    ]
    result1 = sol.employeeFreeTime(schedule1)
    expected1 = [Interval(3, 4)]
    assert len(result1) == len(expected1), f"Expected {len(expected1)} intervals, got {len(result1)}"
    assert result1[0].start == 3 and result1[0].end == 4, f"Expected [3,4], got {result1[0]}"
    print(f"✓ Test 1: {len(schedule1)} employees")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    schedule2 = [
        [Interval(1, 3), Interval(6, 7)],
        [Interval(2, 4)],
        [Interval(2, 5), Interval(9, 12)]
    ]
    result2 = sol.employeeFreeTime(schedule2)
    assert len(result2) == 2, f"Expected 2 intervals, got {len(result2)}"
    assert result2[0].start == 5 and result2[0].end == 6, f"Expected [5,6], got {result2[0]}"
    assert result2[1].start == 7 and result2[1].end == 9, f"Expected [7,9], got {result2[1]}"
    print(f"✓ Test 2: {len(schedule2)} employees")
    print(f"  Result: {result2}")
    
    # Test case 3: No free time
    schedule3 = [
        [Interval(1, 10)],
        [Interval(1, 10)]
    ]
    result3 = sol.employeeFreeTime(schedule3)
    assert len(result3) == 0, f"Expected 0 intervals, got {len(result3)}"
    print(f"✓ Test 3: No free time")
    print(f"  Result: {result3}")
    
    # Test case 4: All employees free
    schedule4 = [
        [Interval(1, 2)],
        [Interval(3, 4)]
    ]
    result4 = sol.employeeFreeTime(schedule4)
    assert len(result4) == 1, f"Expected 1 interval, got {len(result4)}"
    assert result4[0].start == 2 and result4[0].end == 3, f"Expected [2,3], got {result4[0]}"
    print(f"✓ Test 4: All employees free between intervals")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_employee_free_time()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    schedule = [
        [Interval(1, 2), Interval(5, 6)],
        [Interval(1, 3)],
        [Interval(4, 10)]
    ]
    result = sol.employeeFreeTime(schedule)
    print(f"Employee schedules: {schedule}")
    print(f"Common free time: {result}")
# %%

