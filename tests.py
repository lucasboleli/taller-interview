import re
import unittest

from exceptions import PaymentException, UsernameException
from minivenmo import MiniVenmo
from user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user1 = User("Alice")
        self.user2 = User("Bobb")

    def test_username_validation(self):
        with self.assertRaises(UsernameException):
            User("inv@lid")

    def test_add_friend(self):
        self.user1.add_friend(self.user2)
        self.assertIn(self.user2, self.user1.friends)
        self.assertIn(self.user1, self.user2.friends)

    def test_payment_with_balance(self):
        self.user1.add_to_balance(10.00)
        self.user1.pay(self.user2, 5.00, "Lunch")
        self.assertEqual(self.user1.balance, 5.00)
        self.assertEqual(self.user2.balance, 0.00)
        self.assertIn(
            "Alice paid Bobb $5.00 for Lunch using balance", self.user1.retrieve_feed()
        )

    def test_prevent_self_payment(self):
        with self.assertRaises(PaymentException):
            self.user1.pay(self.user1, 5.00, "Test")

    def test_prevent_negative_payment(self):
        with self.assertRaises(PaymentException):
            self.user1.pay(self.user2, -5.00, "Test")


class TestMiniVenmo(unittest.TestCase):
    def setUp(self):
        self.venmo = MiniVenmo()
        self.bobby = self.venmo.create_user("Bobby", 5.00, "4111111111111111")
        self.carol = self.venmo.create_user("Carol", 10.00, "4242424242424242")

    def test_create_user(self):
        self.assertEqual(self.bobby.username, "Bobby")
        self.assertEqual(self.bobby.balance, 5.00)

    def test_add_friend(self):
        self.bobby.add_friend(self.carol)
        self.assertIn(self.carol, self.bobby.friends)
        self.assertIn(self.bobby, self.carol.friends)

    def test_payment_with_balance(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.assertEqual(self.bobby.balance, 0.00)
        self.assertIn(
            "Bobby paid Carol $5.00 for Coffee using balance",
            self.bobby.retrieve_feed(),
        )

    def test_payment_with_credit_card(self):
        self.carol.pay(self.bobby, 15.00, "Lunch")
        self.assertIn(
            "Carol paid Bobby $15.00 for Lunch using credit card 4242424242424242",
            self.carol.retrieve_feed(),
        )

    def test_feed_rendering(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.carol.pay(self.bobby, 15.00, "Lunch")
        feed = self.bobby.retrieve_feed()
        self.assertIn("Bobby paid Carol $5.00 for Coffee using balance", feed)
        feed = self.carol.retrieve_feed()
        self.assertIn(
            "Carol paid Bobby $15.00 for Lunch using credit card 4242424242424242", feed
        )


if __name__ == "__main__":
    unittest.main()
