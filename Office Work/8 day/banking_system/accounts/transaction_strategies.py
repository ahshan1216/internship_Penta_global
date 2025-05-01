# accounts/transaction_strategies.py
from abc import ABC, abstractmethod

class TransactionStrategy(ABC):
    @abstractmethod
    def execute_transaction(self, sender, receiver, amount):
        pass

class BankTransfer(TransactionStrategy):
    def execute_transaction(self, sender, receiver, amount):
        if sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()
            return f"Bank Transfer: {amount} transferred."
        return "Insufficient funds"

class PayPalTransfer(TransactionStrategy):
    def execute_transaction(self, sender, receiver, amount):
        if sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()
            return f"PayPal Transfer: {amount} transferred."
        return "Insufficient funds"

class WireTransfer(TransactionStrategy):
    def execute_transaction(self, sender, receiver, amount):
        if sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()
            return f"Wire Transfer: {amount} transferred."
        return "Insufficient funds"
