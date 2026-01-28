# LeetCode 1058: Minimize Rounding Error to Meet Target
#%%
"""
Problem Statement:
You are given an array of strings prices where prices[i] is a number with exactly three digits
after the decimal point. You are also given an integer target.

For each price, you must choose either floor(price) or ceil(price).
Your goal is to make the sum of chosen integers equal to target while minimizing the total
rounding error.

Rounding error for one price:
- If choose floor: error = price - floor(price)
- If choose ceil:  error = ceil(price) - price

Return the minimum rounding error as a string with exactly 3 digits after the decimal point.
If it is impossible to reach target, return "-1".

Examples:
prices = ["0.700","2.800","4.900"], target = 8  -> "1.000"
prices = ["1.500","2.500","3.500"], target = 10 -> "-1"
prices = ["1.500","2.500","3.500"], target = 9  -> "1.500"

INTERVIEW EXPLANATION (brief, why greedy + sorting):

- **Feasibility bounds**:
  If you floor everything, you get the minimum possible sum.
  If you ceil everything (only matters for non-integers), you get the maximum possible sum.
  Target must lie within [sum_floor, sum_floor + count_non_integer].

- **Greedy choice**:
  Start by flooring everything (this fixes an easy baseline).
  To increase the sum by 1, we must "round up" a non-integer price.
  For a price with fractional part f (0 < f < 1):
    - floor error = f
    - ceil  error = 1 - f
    Switching it from floor -> ceil changes total error by:
      (1 - f) - f = 1 - 2f
  To minimize total error while rounding up exactly `need` items, pick the items with
  the smallest (1 - 2f), i.e. the largest fractional parts f.

Implementation detail:
- Use **integer thousandths** to avoid floating-point drift (since inputs have 3 decimals
  and output needs 3 decimals).
"""

from typing import List


class Solution:
    def minimizeError(self, prices: List[str], target: int) -> str:
        """
        Cleaner greedy structure:
        - compute floor_sum / ceil_sum bounds
        - compute num_ceil = target - floor_sum
        - sort fractional parts
        - round up the `num_ceil` largest fractions, round down the rest

        Returns:
            Minimum rounding error as a string with 3 decimal places, or "-1" if impossible.
        """
        floor_sum = 0
        ceil_sum = 0
        # store fractional thousandths for all items (0..999)
        fracs: List[int] = []

        for p in prices:
            milli = self._to_milli(p)  # integer thousandths
            integer = milli // 1000
            frac = milli % 1000
            floor_sum += integer
            ceil_sum += integer if frac == 0 else (integer + 1)
            fracs.append(frac)

        # Feasibility check
        if target < floor_sum or target > ceil_sum:
            return "-1"

        # number of values we must round up
        num_ceil = target - floor_sum

        # Sort fractional parts ascending; we'll round up the largest ones.
        fracs.sort()

        err_thousandths = 0
        n = len(fracs)
        cutoff = n - num_ceil  # indices [cutoff..n-1] are rounded up

        for i, frac in enumerate(fracs):
            if i >= cutoff:
                # round up: error = (1 - frac) for non-integers; 0 for integers (frac=0)
                err_thousandths += 0 if frac == 0 else (1000 - frac)
            else:
                # round down: error = frac
                err_thousandths += frac

        return self._format_thousandths(err_thousandths)

    @staticmethod
    def _to_milli(price: str) -> int:
        """Convert a decimal string with 3 digits to integer thousandths."""
        if "." not in price:
            return int(price) * 1000
        whole, frac = price.split(".")
        # Problem states exactly 3 digits after decimal, but keep it robust.
        frac = (frac + "000")[:3]
        return int(whole) * 1000 + int(frac)

    @staticmethod
    def _format_thousandths(x: int) -> str:
        """Format integer thousandths as a string with 3 decimals."""
        # x should be >= 0, but keep sign-safe
        sign = "-" if x < 0 else ""
        x = abs(x)
        return f"{sign}{x // 1000}.{x % 1000:03d}"


def test_minimize_rounding_error():
    sol = Solution()

    # Example 1
    prices = ["0.700", "2.800", "4.900"]
    target = 8
    assert sol.minimizeError(prices, target) == "1.000"

    # Example 2
    prices = ["1.500", "2.500", "3.500"]
    target = 10
    assert sol.minimizeError(prices, target) == "-1"

    # Example 3
    prices = ["1.500", "2.500", "3.500"]
    target = 9
    assert sol.minimizeError(prices, target) == "1.500"

    # Edge: already matches floors
    prices = ["1.000", "2.120", "3.005"]
    target = 6  # floors sum to 6
    assert sol.minimizeError(prices, target) == "0.125"

    # Edge: must ceil all non-integers
    prices = ["0.001", "0.999"]
    target = 2
    # floor error = 0.001 + 0.999 = 1.000; need=2 -> round up both:
    # changes: (1-2*0.001) + (1-2*0.999) in thousandths = 998 + (-998) = 0
    # ceil errors: 0.999 + 0.001 = 1.000
    assert sol.minimizeError(prices, target) == "1.000"

    print("All tests passed!")


if __name__ == "__main__":
    test_minimize_rounding_error()
# %%

