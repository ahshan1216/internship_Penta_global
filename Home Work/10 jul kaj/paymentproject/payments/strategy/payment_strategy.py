from abc import ABC, abstractmethod

# Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Concrete Strategies  subclassing the PaymentStrategy interface
class PaypalPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} using PayPal."

class StripePayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} using Stripe."

class BkashPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} using Bkash."

class NagadPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} using Nagad."

class RocketPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} using Rocket."

# Context
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):  
        # "strategy should be an object that follows the structure of the PaymentStrategy class or interface."
        self._strategy = strategy

    def make_payment(self, amount):
        return self._strategy.pay(amount)
