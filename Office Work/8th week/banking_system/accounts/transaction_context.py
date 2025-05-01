# accounts/transaction_context.py
class TransactionContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def execute(self, sender, receiver, amount):
        return self._strategy.execute_transaction(sender, receiver, amount)
