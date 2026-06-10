class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited ${amount:.2f}")
        
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"{self.owner} withdrew ${amount:.2f}")


def banking_menu(account):
    print(f"\n--- {account.owner}'s Account ---")
    print(f"Current balance: ${account.balance:.2f}")
    
    choice = input("Do you want to (d)eposit or (w)ithdraw? ").lower()
    
    if choice == 'd':
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)
        
    elif choice == 'w':
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)
        
    else:
        print("Invalid choice")


account1 = BankAccount("Steve", 650)
account2 = BankAccount("Max", 1000)

banking_menu(account1)
banking_menu(account2)

print("\n--- Final Balances ---")
print(f"{account1.owner}: ${account1.balance:.2f}")
print(f"{account2.owner}: ${account2.balance:.2f}")