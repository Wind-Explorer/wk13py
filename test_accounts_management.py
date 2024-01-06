import unittest
import shelve
from datetime import datetime

from accounts_management import AccountsManagement, Account

class TestAccountsManagement(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_db.db"
        self.accounts_management = AccountsManagement(self.db_path)

    def tearDown(self):
        with shelve.open(self.db_path) as db:
            db.clear()

    def test_create_account(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        result = self.accounts_management.create_account(account)
        self.assertTrue(result)

    def test_create_account_duplicate_email(self):
        account1 = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        account2 = Account("John", "Smith", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        self.accounts_management.create_account(account1)
        result = self.accounts_management.create_account(account2)
        self.assertFalse(result)

    def test_get_account(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        self.accounts_management.create_account(account)
        retrieved_account = self.accounts_management.get_account("john@example.com")
        self.assertEqual(account, retrieved_account)

    def test_update_account(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        self.accounts_management.create_account(account)
        updated_account = Account("John", "Smith", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        result = self.accounts_management.update_account("john@example.com", updated_account)
        self.assertTrue(result)
        retrieved_account = self.accounts_management.get_account("john@example.com")
        self.assertEqual(updated_account, retrieved_account)

    def test_update_account_nonexistent(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        result = self.accounts_management.update_account("john@example.com", account)
        self.assertFalse(result)

    def test_delete_account(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "john@example.com", "password123", 1, True)
        self.accounts_management.create_account(account)
        result = self.accounts_management.delete_account("john@example.com")
        self.assertTrue(result)
        retrieved_account = self.accounts_management.get_account("john@example.com")
        self.assertIsNone(retrieved_account)

    def test_delete_account_nonexistent(self):
        result = self.accounts_management.delete_account("john@example.com")
        self.assertFalse(result)

    def test_invalid_email(self):
        account = Account("John", "Doe", datetime(1990, 1, 1), "invalid_email", "password123", 1, True)
        result = self.accounts_management.create_account(account)
        self.assertFalse(result)

    def test_birth_date_before_current_date(self):
        account = Account("John", "Doe", datetime(2099, 1, 1), "john@example.com", "password123", 1, True)
        result = self.accounts_management.create_account(account)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
