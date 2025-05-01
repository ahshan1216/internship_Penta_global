from users.strategies import ModeratorRegistrationStrategy, AccountHolderRegistrationStrategy

#  Context to use strategy
class RegistrationContext:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, user, validated_data):
        if not self.strategy:
            raise ValueError('No strategy has been set.')
        self.strategy.register_profile(user, validated_data)

#  Factory function to get strategy by role name
def get_registration_strategy(role_name):
    role_name = role_name.lower()
    if role_name == 'moderator':
        return ModeratorRegistrationStrategy()
    elif role_name == 'account_holder':
        return AccountHolderRegistrationStrategy()
    else:
        raise ValueError('Invalid role provided.')
