import re
from datetime import datetime
import shelve

class Account:
    def __init__(self, id: str, first_name: str, last_name: str, date_of_birth: datetime, email: str, password: str, gender: int, receive_newsletters: bool):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = password
        self.gender = gender
        self.receive_newsletters = receive_newsletters

    def validate(self) -> bool:
        # Check if all required fields are filled
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
        # Check if email format is valid
        if not self._validate_email_format():
            print("Email format is invalid")
            return False
        # Check if gender is valid
        if self.gender not in [0, 1, 2]:
            print("gender is " + str(self.gender))
            print("Gender is invalid")
            return False
        # Check if birth datetime is before current datetime
        if not self._validate_birth_datetime():
            print("Birth datetime is not before current datetime")
            return False
        return True
    
    def _validate_birth_datetime(self) -> bool:
        current_datetime = datetime.now()
        return self.date_of_birth < current_datetime
    
    def _validate_email_format(self) -> bool:
        # Email format validation using regular expression
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, self.email) is not None
    
    def __eq__(self, other):
        if isinstance(other, Account):
            return (self.id == other.id and
                    self.first_name == other.first_name and
                    self.last_name == other.last_name and
                    self.date_of_birth == other.date_of_birth and
                    self.email == other.email and
                    self.password == other.password and
                    self.gender == other.gender and
                    self.receive_newsletters == other.receive_newsletters)
        return False

class AccountsManagement:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_account(self, account: Account) -> bool:
        if not account.validate():
            print("account validation failed")
            return False
        
        with shelve.open(self.db_path) as db:
            # Check if account with the same email already exists
            if account.email in db:
                print("account with email already exists")
                return False
            # Save the account to the database
            db[account.email] = account
            print("account created without problem")
        return True
    
    def get_account(self, email: str) -> Account:
        with shelve.open(self.db_path) as db:
            # Retrieve the account from the database
            return db.get(email)
    
    def update_account(self, email: str, account: Account) -> bool:
        if not account.validate():
            return False

        with shelve.open(self.db_path) as db:
            # Check if the account to be updated exists
            if email not in db:
                return False
            # Update the account in the database
            db[email] = account
        return True

    def delete_account(self, email: str) -> bool:
        with shelve.open(self.db_path) as db:
            # Check if the account to be deleted exists
            if email not in db:
                return False
            # Delete the account from the database
            del db[email]
        return True
