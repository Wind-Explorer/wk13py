from accounts_management import Account, AccountsManagement
from datetime import datetime

def main():
    accounts_management = AccountsManagement('accounts.db')

    while True:
        print('What would you like to do?')
        print('1: Create account')
        print('2: Get account')
        print('3: Update account')
        print('4: Delete account')
        print('9: Exit')

        choice = input('Enter your choice: ')

        if choice == '1':
            # Create account
            id = input('Enter id: ')
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            dob = datetime.fromisoformat(input('Enter date of birth (YYYY-MM-DD): '))
            email = input('Enter email: ')
            password = input('Enter password: ')
            gender = int(input('Enter gender (0: Male, 1: Female, 2: Other): '))
            receive_newsletters = input('Receive newsletters? (Y/N): ').lower() == 'y'
            account = Account(id, first_name, last_name, dob, email, password, gender, receive_newsletters)
            if accounts_management.create_account(account):
                print('Account created successfully.')
            else:
                print('Failed to create account.')
        elif choice == '2':
            # Get account
            email = input('Enter email: ')
            account = accounts_management.get_account(email)
            if account:
                print('Account details:')
                print(f'ID: {account.id}')
                print(f'First Name: {account.first_name}')
                print(f'Last Name: {account.last_name}')
                print(f'Date of Birth: {account.date_of_birth}')
                print(f'Email: {account.email}')
                print(f'Gender: {account.gender}')
                print(f'Receive Newsletters: {account.receive_newsletters}')
            else:
                print('Account not found.')
        elif choice == '3':
            # Update account
            email = input('Enter email of account to update: ')
            id = input('Enter new id: ')
            first_name = input('Enter new first name: ')
            last_name = input('Enter new last name: ')
            dob = datetime.fromisoformat(input('Enter new date of birth (YYYY-MM-DD): '))
            new_email = input('Enter new email: ')
            password = input('Enter new password: ')
            gender = int(input('Enter new gender (0: Male, 1: Female, 2: Other): '))
            receive_newsletters = input('Receive newsletters? (Y/N): ').lower() == 'y'
            account = Account(id, first_name, last_name, dob, new_email, password, gender, receive_newsletters)
            if accounts_management.update_account(email, account):
                print('Account updated successfully.')
            else:
                print('Failed to update account.')
        elif choice == '4':
            # Delete account
            email = input('Enter email of account to delete: ')
            if accounts_management.delete_account(email):
                print('Account deleted successfully.')
            else:
                print('Failed to delete account.')
        elif choice == '9':
            # Exit
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main()