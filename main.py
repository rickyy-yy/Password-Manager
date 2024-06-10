from cryptography.fernet import Fernet
import os
import time


pc_user = os.getlogin()
users_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\users.py"
passwords_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\passwords.py"


def check_storage():
    if not os.path.isfile(users_file):
        file = open(users_file, 'x')
        file.write("users_dict = {}")
        file.close()

    if not os.path.isfile(passwords_file):
        file = open(passwords_file, 'x')
        file.write("passwords_dict = {}")
        file.close()


def main_menu():
    user_selection: int
    valid_input = False

    print("Welcome to the Password Manager. We have currently have the following options for you to choose from:")
    print("")
    print("1. Manage Passwords")
    print("2. Generate a Random Password")
    print("3. More Info")
    print("4. Quit")
    print("")

    while not valid_input:
        try:
            user_selection = int(input("Enter your choice (1/2/3/4): "))
            print("")

            while not (0 < user_selection < 5):
                print("")
                print("You entered an invalid selection! Please try again.")
                user_selection = int(input("Enter your choice (1/2/3/4): "))

            valid_input = True
        except ValueError:
            pass

    match user_selection:
        case 1:
            login_or_signup()
        case 2:
            generate_password()
        case 3:
            info_page()
        case 4:
            exit()


def login_or_signup():
    user_selection: int
    valid_input = False

    print("")
    print("Before you retrieve your passwords, you must log in!")
    print("")
    print("1. Login to existing user")
    print("2. Sign up for new user")
    print("3. Go back")
    print("")

    while not valid_input:
        try:
            user_selection = int(input("Enter your choice (1/2/3): "))
            print("")

            while not (0 < user_selection < 4):
                print("")
                print("You entered an invalid selection! Please try again.")
                user_selection = int(input("Enter your choice (1/2/3): "))

            valid_input = True
        except ValueError:
            pass

    match user_selection:
        case 1:
            login_page()
        case 2:
            signup_page()
        case 3:
            main_menu()


def generate_password():
    pass


def info_page():
    print("")
    print("Info Page")
    print("=========")
    print("The first option lets you manage your passwords. You can either store a new password or retrieve them. This program lets you access passwords associated with your own account.")
    print("If you do not have an account, you can sign up for one. ")
    print("")
    print("The second option will generate a random secure password for you. You will then have the option to associate it with your account. ")
    print("Each password in your account can be assigned a note, perhaps you can use this feature to keep track of which passwords are for which sites.")
    print("=========")

    time.sleep(5)
    print("")
    print("Sending you back to the main menu...")
    time.sleep(1)
    main_menu()


def login_page():
    user_selection: int
    username: str
    password: str
    valid_input = False

    print("")

    username = str(input("Please enter your username: "))
    while len(username) < 4:
        print("")
        print("Your username must have at least 4 characters!")
        print("")
        username = str(input("Please enter your username: "))

    password = str(input("Please enter your password: "))
    while len(password) < 7:
        print("")
        print("Your password must have at least 7 characters!")
        print("")
        password = str(input("Please enter your password: "))

    if check_user(username, password):
        show_passwords(username, password)
    else:
        print("")
        print("Username/password is incorrect! Would you like to: ")
        print("")
        print("1. Try again")
        print("2. Go back")
        print("")

        while not valid_input:
            try:
                user_selection = int(input("Enter your choice (1/2): "))
                print("")

                while not (0 < user_selection < 3):
                    print("")
                    print("You entered an invalid selection! Please try again.")
                    user_selection = int(input("Enter your choice (1/2): "))

                valid_input = True
            except ValueError:
                pass

        match user_selection:
            case 1:
                login_page()
            case 2:
                login_or_signup()


def signup_page():
    user_selection: int
    username: str
    password: str
    valid_input = False

    print("")

    username = str(input("Please enter a username: "))
    while len(username) < 4:
        print("")
        print("Your username must have at least 4 characters!")
        print("")
        username = str(input("Please enter a username: "))

    password = str(input("Please enter a password: "))
    while len(password) < 7:
        print("")
        print("Your password must have at least 7 characters!")
        print("")
        password = str(input("Please enter a password: "))

    if unique_username(username):
        register_account(username, password)
    else:
        print("")
        print("Username is taken! Would you like to: ")
        print("")
        print("1. Try again")
        print("2. Go back")
        print("")

        while not valid_input:
            try:
                user_selection = int(input("Enter your choice (1/2): "))
                print("")

                while not (0 < user_selection < 3):
                    print("")
                    print("You entered an invalid selection! Please try again.")
                    user_selection = int(input("Enter your choice (1/2): "))

                valid_input = True
            except ValueError:
                pass

        match user_selection:
            case 1:
                signup_page()
            case 2:
                login_or_signup()


def check_user(username, password):
    registered_users = list(users_dict.keys())
    registered_passwords = list(users_dict.values())


def show_passwords(username, password):
    pass


def unique_username(username):
    pass


def register_account(username, password):
    pass


def decrypt(value, password):
    key = password
    fernet = Fernet(key)

    plaintext = fernet.decrypt(value).decode()
    return plaintext


def encrypt(value, password):
    key = password
    fernet = Fernet(key)

    ciphertext = fernet.encrypt(value.encode())
    return ciphertext


if __name__ == '__main__':
    check_storage()
    from passwords import *
    from users import *
    main_menu()
