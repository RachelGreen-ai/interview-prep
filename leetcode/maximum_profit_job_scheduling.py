# LeetCode 1235: Maximum Profit in Job Scheduling
#%%
"""
Problem Statement:
We have n jobs, where every job is scheduled to be done from startTime[i] to
endTime[i], obtaining a profit of profit[i].

You're given the startTime, endTime and profit arrays, return the maximum profit
you can take such that there are no two jobs in the subset with overlapping time
range.

If you choose a job that ends at time X, you will be able to start another job
that starts at time X.

Example 1:
Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
Explanation: The subset chosen is the first and fourth job.
Time range [1-3]+[3-6] , we get profit 50 + 70 = 120.

Example 2:
Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
Explanation: The subset chosen is the first, fourth and fifth job.
Profit obtained 20 + 70 + 60 = 150.

INTERVIEW EXPLANATION: Why DP + Binary Search for Job Scheduling?

1. **Problem Structure**: This is a weighted interval scheduling problem. We need
   to select non-overlapping jobs to maximize profit. This is similar to the
   classic "Activity Selection" but with weights (profits).

2. **Why DP + Binary Search?**
   - **Key Insight**: Sort jobs by end time. For each job, we can either:
     * Take it: profit = job.profit + max_profit of jobs ending before job.start
     * Skip it: profit = max_profit of previous jobs
   
   - **DP State**: dp[i] = maximum profit we can get from first i jobs
   
   - **Recurrence**: 
     * dp[i] = max(take job i, skip job i)
     * take job i = profit[i] + dp[j] where j is last job ending before start[i]
     * Use binary search to find j efficiently
   
   - **Time Complexity**: 
     * Sorting: O(n log n)
     * DP with binary search: O(n log n)
     * Total: O(n log n)
   
   - **Space Complexity**: O(n) for DP array

3. **Key Insight**: By sorting by end time, we ensure that when considering
   job i, all previous jobs have end times <= end[i]. We can use binary search
   to find the last non-overlapping job efficiently.

4. **Alternative Approach**: 
   - Can also use DP with linear search: O(n²)
   - Binary search optimization is preferred for interviews
"""

from typing import List
import bisect


class Solution:
    """Solution for Maximum Profit in Job Scheduling"""
    
    def jobScheduling(self, startTime: List[int], endTime: List[int], 
                     profit: List[int]) -> int:
        """
        Find maximum profit from non-overlapping jobs.
        
        Args:
            startTime: Start times of jobs
            endTime: End times of jobs
            profit: Profit of each job
            
        Returns:
            Maximum profit achievable
        """
        n = len(startTime)
        
        # Combine and sort by end time
        jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
        
        # Extract sorted arrays
        ends = [job[1] for job in jobs]
        profits = [job[2] for job in jobs]
        starts = [job[0] for job in jobs]
        
        # dp[i] = max profit from first i jobs
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            # Option 1: Skip job i-1
            skip_profit = dp[i - 1]
            
            # Option 2: Take job i-1
            # Find last job ending before start[i-1]
            # Binary search for rightmost position where end <= start[i-1]
            last_job_idx = bisect.bisect_right(ends, starts[i - 1]) - 1
            
            take_profit = profits[i - 1] + dp[last_job_idx + 1]
            
            dp[i] = max(skip_profit, take_profit)
        
        return dp[n]
    
    def jobScheduling_linear(self, startTime: List[int], endTime: List[int],
                            profit: List[int]) -> int:
        """
        Alternative: DP with linear search (simpler but O(n²)).
        Good for understanding, but slower.
        """
        n = len(startTime)
        jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
        
        dp = [0] * n
        dp[0] = jobs[0][2]  # First job
        
        for i in range(1, n):
            # Skip current job
            skip_profit = dp[i - 1]
            
            # Take current job - find last non-overlapping job
            take_profit = jobs[i][2]
            for j in range(i - 1, -1, -1):
                if jobs[j][1] <= jobs[i][0]:
                    take_profit += dp[j]
                    break
            
            dp[i] = max(skip_profit, take_profit)
        
        return dp[n - 1]


def test_job_scheduling():
    """Test cases for Maximum Profit in Job Scheduling"""
    sol = Solution()
    
    # Test case 1: Example 1
    start1, end1, profit1 = [1,2,3,3], [3,4,5,6], [50,10,40,70]
    result1 = sol.jobScheduling(start1, end1, profit1)
    assert result1 == 120, f"Expected 120, got {result1}"
    print(f"✓ Test 1: {result1}")
    
    # Test case 2: Example 2
    start2, end2, profit2 = [1,2,3,4,6], [3,5,10,6,9], [20,20,100,70,60]
    result2 = sol.jobScheduling(start2, end2, profit2)
    assert result2 == 150, f"Expected 150, got {result2}"
    print(f"✓ Test 2: {result2}")
    
    # Test case 3: Single job
    start3, end3, profit3 = [1], [2], [10]
    result3 = sol.jobScheduling(start3, end3, profit3)
    assert result3 == 10, f"Expected 10, got {result3}"
    print(f"✓ Test 3: {result3}")
    
    # Test case 4: All overlapping
    start4, end4, profit4 = [1,1,1], [3,3,3], [10,20,30]
    result4 = sol.jobScheduling(start4, end4, profit4)
    assert result4 == 30, f"Expected 30 (take best), got {result4}"
    print(f"✓ Test 4: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_job_scheduling()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    startTime = [1,2,3,3]
    endTime = [3,4,5,6]
    profit = [50,10,40,70]
    result = sol.jobScheduling(startTime, endTime, profit)
    print(f"Jobs: start={startTime}, end={endTime}, profit={profit}")
    print(f"Maximum profit: {result}")
    print("Explanation: Choose jobs 0 and 3 → 50 + 70 = 120")
# %%

