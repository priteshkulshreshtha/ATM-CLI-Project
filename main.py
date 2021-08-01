import pickle
import random


class ValueNegative(BaseException):
    pass


class Account:
    def __init__(self, pin: int, account_number: int, initial_balance: int = 0):
        self.PIN = pin
        self._Current_Balance = initial_balance
        self._Account_Number = account_number

    def get_acc_number(self):
        return self._Account_Number

    def display_balance(self) -> int:
        return self._Current_Balance

    def transaction(self, amount: int, credit: bool = True) -> None:
        self._Current_Balance += amount if credit else -amount

    def check_pin(self, input_pin: int) -> bool:
        return self.PIN == input_pin


class ATM:
    def __init__(self):
        self.logged_in = False
        account_info_in = open('private/account.pickle', 'rb')
        self.db = pickle.load(account_info_in)
        account_info_in.close()
        self._current_account = None

    @staticmethod
    def _accept_numeric(input_string="Please Enter a Value", end_string=None, check_negative=True, return_false=None):
        try:
            val = int(input(input_string))
            if val < 0 and check_negative:
                raise ValueNegative
            return val
        except ValueError:
            print("This is not a number")
        except ValueNegative:
            print("Value is Negative")
        if end_string:
            print(end_string)
        return return_false

    def create_account(self, pin: int, initial_balance: int = 0) -> None:
        def _gen_account_number() -> int:
            return random.randint(100, 1000)

        if not len(str(pin).strip('-')) == 4:
            print("Error: Account not created\n"
                  "PIN should be 4 digit only")
            return

        new_acc_num = _gen_account_number()
        self.db[new_acc_num] = Account(pin, new_acc_num, initial_balance)
        self._update_db()

        print(f'New account created with pin {pin} and Account Number: {new_acc_num}')
        print(f"{'Account Created':-^60}")

    def delete_account(self, account_number: int) -> None:
        del self.db[account_number]
        self._update_db()
        print(f"{'Account Deleted':-^60}")

    def clear_db(self):
        self.db = {}
        self._update_db()

    def _get_account_details(self) -> int:
        pay_to = self._accept_numeric("\nEnter the Recipient Account Number: ",
                                      f'{"Transaction Canceled":-^60}')
        if self._check_account_exist(pay_to):
            return pay_to
        else:
            print("Account Does not exist.")

    def transfer_money(self, pay_to: int, amount: int) -> None:
        if self._current_account.display_balance() >= amount:
            self.db[pay_to].transaction(amount)
            self._current_account.transaction(amount, credit=False)
            self._update_db()
            print(f"{'Funds Transferred':-^60}")
        else:
            print(f"{'Insufficient Funds':-^60}")

    def add_money(self) -> None:
        if amount := self._accept_numeric('\nPlease Enter the Amount you want to deposit: ',
                                          f'{"Transaction Canceled":-^60}'):
            self._current_account.transaction(amount)
            self._update_db()
            print(f"{'Money Deposited':-^60}")

    def _update_db(self) -> None:
        account_info_out = open('private/account.pickle', 'wb')
        pickle.dump(self.db, account_info_out)
        account_info_out.close()

    def display_balance(self, account_number: int) -> int:
        return self.db[account_number].display_balance()

    def display_accounts(self) -> None:
        print('\nAccounts Registered with us:\n\t' + '\n\t'.join([str(key) for key in self.db.keys()]))

    def _check_account_exist(self, account_number: int) -> bool:
        return account_number in self.db.keys()

    def login(self) -> bool:
        if account_number := self._get_account_details():
            input_pin = self._accept_numeric('Please Enter your PIN: ')
            if self.db[account_number].check_pin(input_pin):
                self._current_account = self.db[account_number]
                return True
            else:
                print("PIN entered is wrong.")
        else:
            print("Use Create account")
            return False

    def _menu_selection(self, avail_options: list) -> int:
        option = self._accept_numeric('Your Selection: ', check_negative=False)
        if option in avail_options:
            return option
        else:
            print(f"\nInvalid Selection")
            print('Please select again')

    def home(self) -> int:
        print(f"\nPress [1] to Login")
        print(f'Press [2] to Create New Account')
        print(f'Press [0] to Exit')
        return self._menu_selection([1, 2, 0])

    def menu(self) -> int:
        print(f'\n{"Press [1] to deposit money":60}')
        print(f'{"Press [2] to transfer money":60}')
        print(f'{"Press [3] to display balance":60}')
        print(f'{"Press [9] to delete account":60}')
        print(f'{"Press [0] to log out":60}')
        return self._menu_selection([1, 2, 3, 9, 0])

    def _home_login(self) -> None:
        while not self.logged_in:
            option = self.home()
            if option == 1:
                self.logged_in = self.login()
            elif option == 2:
                end_string = "Account Not Created"
                if pin := self._accept_numeric("Please Enter your PIN: ", end_string=end_string, check_negative=False):
                    if init_amount := self._accept_numeric('Please Enter the initial balance for the account: ',
                                                           end_string):
                        self.create_account(pin, init_amount)
            elif option == 0:
                return
            else:
                continue

    def _atm_acc_transactions(self):
        option = self.menu()
        while self.logged_in:

            if option == 0:
                return

            elif option == 1:
                self.add_money()

            elif option == 2:
                if pay_to := self._get_account_details():
                    if amount := self._accept_numeric('Please Enter the Amount you want to Transfer: ',
                                                      f'{"Transaction Canceled":-^60}'):
                        self.transfer_money(pay_to, amount)

            elif option == 3:
                print(f'{"=" * 60}')
                print(f"Balance: {self._current_account.display_balance()}")
                print(f'{"=" * 60}')

            elif option == 9:
                if input("Press 'y' if you want to delete the account: ").strip() == 'y':
                    self.delete_account(self._current_account.get_acc_number())
                    return

            option = self.menu()
            continue

    def run(self):
        self._home_login()
        print(f'\n{"WELCOME USER " + str(self._current_account.get_acc_number()):^60}')
        print(f'{"=" * 60}')
        self._atm_acc_transactions()


atm = ATM()
atm.run()
