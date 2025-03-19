import re

from exceptions import CreditCardException, PaymentException, UsernameException


class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.activity = []
        self.friends = set()

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException("Username not valid.")

    def retrieve_feed(self):
        return self.activity

    def add_friend(self, new_friend):
        if new_friend not in self.friends:
            self.friends.add(new_friend)
            new_friend.friends.add(self)
            self.activity.append(
                f"{self.username} and {new_friend.username} are now friends."
            )
            new_friend.activity.append(
                f"{new_friend.username} and {self.username} are now friends."
            )

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException("Only one credit card per user!")

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target, amount, note):
        amount = float(amount)
        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")
        if amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")

        if self.balance >= amount:
            self.balance -= amount
            self.activity.append(
                f"{self.username} paid {target.username} ${amount:.2f} for {note} using balance"
            )
        else:
            if self.credit_card_number is None:
                raise PaymentException("Insufficient funds and no credit card linked.")
            self._charge_credit_card(target, amount, note)

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match("^[A-Za-z0-9_\\-]{4,15}$", username)

    def _charge_credit_card(self, target, amount, note):
        self.activity.append(
            f"{self.username} paid {target.username} ${amount:.2f} for {note} using credit card {self.credit_card_number}"
        )
