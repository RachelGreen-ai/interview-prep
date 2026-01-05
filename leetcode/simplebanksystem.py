"""
LeetCode 2043: Simple Bank System
==================================

PROBLEM STATEMENT:
------------------
Design a bank system with n accounts numbered from 1 to n. Each account has an initial balance.
Implement the Bank class:
1. Bank(balance): Initialize with balance array where balance[i] is initial balance of account (i+1)
2. transfer(account1, account2, money): Transfer money from account1 to account2
   - Returns True if successful, False if account doesn't exist or insufficient funds
3. deposit(account, money): Deposit money into account
   - Returns True if successful, False if account doesn't exist
4. withdraw(account, money): Withdraw money from account
   - Returns True if successful, False if account doesn't exist or insufficient funds

KEY CONSTRAINTS:
- Account numbers are 1-indexed (accounts are numbered 1, 2, 3, ..., n)
- Array indices are 0-indexed (balance[0] is account 1, balance[1] is account 2, etc.)
- All operations must validate account existence
- Transfer and withdraw must check for sufficient funds

APPROACH:
---------
1. Store balance array and number of accounts (n) in constructor
2. For each operation:
   - Validate account number (must be <= n and > 0, but problem guarantees > 0)
   - Check sufficient funds (for transfer and withdraw)
   - Perform the operation atomically
   - Return success/failure

TIME COMPLEXITY:
- transfer: O(1) - constant time array access and update
- deposit: O(1) - constant time array access and update
- withdraw: O(1) - constant time array access and update

SPACE COMPLEXITY:
- O(n) - storing balance array of size n

INTERVIEW TIPS:
---------------
1. Clarify account numbering (1-indexed vs 0-indexed) - this is a common gotcha!
2. Always validate inputs first (account existence, sufficient funds)
3. Consider edge cases:
   - Invalid account numbers (too large, negative, zero)
   - Negative money amounts (usually not allowed)
   - Zero money transfers (usually allowed)
4. In real systems, you'd want:
   - Transaction logging
   - Locking mechanisms for concurrent access
   - Atomic operations (database transactions)
   - Better error messages/exceptions
5. Discuss trade-offs: array vs dictionary (array is more space-efficient if accounts are sequential)

BUGS TO WATCH FOR:
-----------------
- Off-by-one errors: account numbers are 1-indexed, arrays are 0-indexed
- Not checking both accounts in transfer
- Not checking sufficient funds before modifying balance
- Modifying balance even when operation should fail
"""

#leetcode 2043 Bank System 
#%% 
from typing import List

class Bank:
    def __init__(self, balance: List[int]):
        """
        Initialize bank with balance array.
        balance[i] represents the initial balance of account (i+1)
        """
        self.balance = balance
        self.n = len(balance)  # Number of accounts

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        """
        Transfer money from account1 to account2.
        
        Steps:
        1. Validate both accounts exist (account numbers are 1-indexed)
        2. Check if account1 has sufficient funds
        3. Perform transfer atomically (debit from account1, credit to account2)
        
        Returns True if successful, False otherwise.
        """
        # Validate account numbers (accounts are 1-indexed, so valid range is [1, n])
        if account1 > self.n or account2 > self.n or account1 < 1 or account2 < 1:
            return False
        
        # Check if source account has sufficient funds
        if self.balance[account1-1] < money:  # account1-1 converts to 0-indexed
            return False
        
        # Perform transfer: debit from account1, credit to account2
        self.balance[account1-1] -= money
        self.balance[account2-1] += money
        return True
    
    def deposit(self, account: int, money: int) -> bool:
        """
        Deposit money into account.
        
        Steps:
        1. Validate account exists
        2. Add money to account balance
        
        Returns True if successful, False otherwise.
        """
        # Validate account number
        if account > self.n or account < 1:
            return False
        
        # Add money to account (account-1 converts to 0-indexed)
        self.balance[account-1] += money
        return True
    
    def withdraw(self, account: int, money: int) -> bool:
        """
        Withdraw money from account.
        
        Steps:
        1. Validate account exists
        2. Check if account has sufficient funds
        3. Deduct money from account balance
        
        Returns True if successful, False otherwise.
        """
        # Validate account number
        if account > self.n or account < 1:
            return False
        
        # Check if account has sufficient funds
        if self.balance[account-1] < money:  # account-1 converts to 0-indexed
            return False
        
        # Deduct money from account
        self.balance[account-1] -= money
        return True 
    
#%% TEST CASES WITH EXPLANATIONS

def test_basic_operations():
    """Test basic operations: transfer, deposit, withdraw"""
    print("=" * 60)
    print("TEST 1: Basic Operations")
    print("=" * 60)
    bank = Bank([10, 100, 20, 50, 30])  # Accounts 1-5 with balances [10, 100, 20, 50, 30]
    print(f"Initial balances: {bank.balance}")
    print(f"Account 1: ${bank.balance[0]}, Account 2: ${bank.balance[1]}, "
          f"Account 3: ${bank.balance[2]}, Account 4: ${bank.balance[3]}, "
          f"Account 5: ${bank.balance[4]}")
    
    # Transfer $10 from account 3 to account 4
    result = bank.transfer(3, 4, 10)
    print(f"\ntransfer(3, 4, 10): {result}")
    print(f"  Expected: True (account 3 has $20, transferring $10)")
    print(f"  Account 3 balance: ${bank.balance[2]} (was $20, now $10)")
    print(f"  Account 4 balance: ${bank.balance[3]} (was $50, now $60)")
    
    # Deposit $20 to account 5
    result = bank.deposit(5, 20)
    print(f"\ndeposit(5, 20): {result}")
    print(f"  Expected: True (valid account)")
    print(f"  Account 5 balance: ${bank.balance[4]} (was $30, now $50)")
    
    # Withdraw $10 from account 3
    result = bank.withdraw(3, 10)
    print(f"\nwithdraw(3, 10): {result}")
    print(f"  Expected: True (account 3 has $10, withdrawing $10)")
    print(f"  Account 3 balance: ${bank.balance[2]} (was $10, now $0)")
    
    # Try to transfer $15 from account 3 (insufficient funds)
    result = bank.transfer(3, 4, 15)
    print(f"\ntransfer(3, 4, 15): {result}")
    print(f"  Expected: False (account 3 has $0, cannot transfer $15)")
    print(f"  Account 3 balance: ${bank.balance[2]} (unchanged at $0)")
    print(f"  Account 4 balance: ${bank.balance[3]} (unchanged at $60)")
    
    print(f"\nFinal balances: {bank.balance}")

def test_edge_cases():
    """Test edge cases: invalid accounts, boundary conditions"""
    print("\n" + "=" * 60)
    print("TEST 2: Edge Cases")
    print("=" * 60)
    bank = Bank([100, 200, 300])
    print(f"Initial balances: {bank.balance} (3 accounts)")
    
    # Invalid account numbers
    print(f"\n1. Invalid account (too large):")
    print(f"   transfer(4, 1, 10): {bank.transfer(4, 1, 10)}")  # False - account 4 doesn't exist
    print(f"   deposit(0, 10): {bank.deposit(0, 10)}")  # False - account 0 doesn't exist
    print(f"   withdraw(-1, 10): {bank.withdraw(-1, 10)}")  # False - negative account
    
    # Valid operations
    print(f"\n2. Valid operations:")
    print(f"   deposit(1, 50): {bank.deposit(1, 50)}")  # True
    print(f"   Account 1 balance: ${bank.balance[0]}")
    
    # Insufficient funds
    print(f"\n3. Insufficient funds:")
    print(f"   withdraw(1, 200): {bank.withdraw(1, 200)}")  # False - only has $150
    print(f"   Account 1 balance: ${bank.balance[0]} (unchanged)")
    
    # Transfer to same account (edge case - usually allowed)
    print(f"\n4. Transfer to same account:")
    print(f"   transfer(2, 2, 10): {bank.transfer(2, 2, 10)}")  # True - valid but no net change
    print(f"   Account 2 balance: ${bank.balance[1]} (unchanged at $200)")

def test_complex_scenario():
    """Test a complex scenario with multiple operations"""
    print("\n" + "=" * 60)
    print("TEST 3: Complex Scenario")
    print("=" * 60)
    bank = Bank([1000, 2000, 3000, 4000, 5000])
    print(f"Initial balances: {bank.balance}")
    
    operations = [
        ("deposit", 1, 500),
        ("withdraw", 2, 300),
        ("transfer", 3, 4, 200),
        ("transfer", 5, 1, 1000),
        ("withdraw", 1, 5000),  # Should fail - insufficient funds
        ("transfer", 2, 6, 100),  # Should fail - account 6 doesn't exist
    ]
    
    for op, *args in operations:
        if op == "deposit":
            result = bank.deposit(args[0], args[1])
            print(f"{op}({args[0]}, {args[1]}): {result}")
        elif op == "withdraw":
            result = bank.withdraw(args[0], args[1])
            print(f"{op}({args[0]}, {args[1]}): {result}")
        elif op == "transfer":
            result = bank.transfer(args[0], args[1], args[2])
            print(f"{op}({args[0]}, {args[1]}, {args[2]}): {result}")
    
    print(f"\nFinal balances: {bank.balance}")
    print(f"Expected: Account 1: $2500, Account 2: $1700, Account 3: $2800, "
          f"Account 4: $4200, Account 5: $4000")

# Run all tests
if __name__ == "__main__":
    test_basic_operations()
    test_edge_cases()
    test_complex_scenario()

# %%
