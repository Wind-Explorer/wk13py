import re
from datetime import datetime
import shelve
from uuid import uuid4


class Account:
    """
    Represents a user account.

    Attributes:
        id (str): The unique identifier of the account.
        first_name (str): The first name of the account holder.
        last_name (str): The last name of the account holder.
        date_of_birth (datetime): The date of birth of the account holder.
        email (str): The email address of the account holder.
        password (str): The password of the account.
        gender (int): The gender of the account holder (0 for male, 1 for female, 2 for other).
        receive_newsletters (bool): Indicates whether the account holder wants to receive newsletters.

    Methods:
        validate(): Validates the account information.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: datetime,
        email: str,
        password: str,
        gender: int,
        receive_newsletters: bool,
    ):
        self.id = str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = password
        self.gender = gender
        self.receive_newsletters = receive_newsletters

    def validate(self) -> bool:
        """
        Validates the account information.

        Returns:
            bool: True if the account information is valid, False otherwise.
        """
        if not self.id or len(self.id) == 0:
            print("ID is missing or empty")
            return False
        if not self.first_name or len(self.first_name) == 0:
            print("First name is missing or empty")
            return False
        if not self.last_name or len(self.last_name) == 0:
            print("Last name is missing or empty")
            return False
        if not self.email or len(self.email) == 0:
            print("Email is missing or empty")
            return False
        if not self.password or len(self.password) == 0:
            print("Password is missing or empty")
            return False
        if not self._validate_email_format():
            print("Email format is invalid")
            return False
        if self.gender not in [0, 1, 2]:
            print("gender is " + str(self.gender))
            print("Gender is invalid")
            return False
        if not self._validate_birth_datetime():
            print("Birth datetime is not before current datetime")
            return False
        return True

    def _validate_birth_datetime(self) -> bool:
        """
        Validates if the birth datetime is before the current datetime.

        Returns:
            bool: True if the birth datetime is before the current datetime, False otherwise.
        """
        current_datetime = datetime.now()
        return self.date_of_birth < current_datetime

    def _validate_email_format(self) -> bool:
        """
        Validates the email format.

        Returns:
            bool: True if the email format is valid, False otherwise.
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, self.email) is not None

    def __eq__(self, other):
        if isinstance(other, Account):
            return (
                self.id == other.id
                and self.first_name == other.first_name
                and self.last_name == other.last_name
                and self.date_of_birth == other.date_of_birth
                and self.email == other.email
                and self.password == other.password
                and self.gender == other.gender
                and self.receive_newsletters == other.receive_newsletters
            )
        return False


class AccountsManagement:
    """
    Manage user accounts.

    Attributes:
        db_path (str): The path to the database file.

    Methods:
        create_account(): Create a new account.
        get_account_by_id(): Get an account by its ID.
        update_account(): Update an existing account.
        delete_account(): Delete an account.
        login(): Perform login with email and password.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_account(self, account: Account) -> bool:
        """
        Create a new account.

        Args:
            account (Account): The account object to be created.

        Returns:
            bool: True if the account is created successfully, False otherwise.
        """
        if not account.validate():
            print("account validation failed")
            return False

        with shelve.open(self.db_path) as db:
            if account.email in db:
                print("account with email already exists")
                return False
            db[account.email] = account
            print("account created without problem")
        return True

    def get_account_by_id(self, account_id: str) -> Account:
        """
        Get an account by its ID.

        Args:
            account_id (str): The ID of the account.

        Returns:
            Account: The account object if found, None otherwise.
        """
        with shelve.open(self.db_path) as db:
            for account in db.values():
                if account.id == account_id:
                    return account
        return None

    def update_account(self, account_id: str, account: Account) -> bool:
        """
        Update an existing account.

        Args:
            account_id (str): The ID of the account to be updated.
            account (Account): The updated account object.

        Returns:
            bool: True if the account is updated successfully, False otherwise.
        """
        if not account.validate():
            return False

        with shelve.open(self.db_path) as db:
            for key, value in db.items():
                if value.id == account_id:
                    db[key] = account
                    return True
        return False

    def delete_account(self, account_id: str) -> bool:
        """
        Delete an account.

        Args:
            account_id (str): The ID of the account to be deleted.

        Returns:
            bool: True if the account is deleted successfully, False otherwise.
        """
        with shelve.open(self.db_path) as db:
            for key, value in db.items():
                if value.id == account_id:
                    del db[key]
                    return True
        return False

    def login(self, email: str, password: str) -> str:
        """
        Perform login with email and password.

        Args:
            email (str): The email of the account.
            password (str): The password of the account.

        Returns:
            str: The ID of the account if login is successful, None otherwise.
        """
        with shelve.open(self.db_path) as db:
            for account in db.values():
                if account.email == email and account.password == password:
                    return account.id
        return None
