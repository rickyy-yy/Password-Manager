from cryptography.fernet import Fernet
import os
import time

pc_user = os.getlogin()
users_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\users.py"
passwords_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\passwords.py"
key_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\key.txt"

key: str


def check_storage():
    if not os.path.isfile(users_file):
        with open(users_file, 'x') as file:
            file.write("registered_users_dict = {}")

    if not os.path.isfile(passwords_file):
        with open(passwords_file, 'x') as file:
            file.write("password_db = []\n")
            file.write("user_index = {}")

    if not os.path.isfile(key_file):
        with open(key_file, 'x') as file:
            generate_new_key()


def check_note_unique(username, note):
    password_list = password_db[username]

    for pw_pair in password_list:
        if note in pw_pair:
            return False

    return True


def check_username_exist(username):
    usernames = list(registered_users_dict.keys())
    if username in usernames:
        return True
    else:
        return False


def check_login_match(username, password):
    global key
    usernames = list(registered_users_dict.keys())
    encrypted_passwords = list(registered_users_dict.values())
    index = usernames.index(username)

    real_password = bytes(encrypted_passwords[index].encode())
    decrypted_password = decrypt(real_password)

    if password == decrypted_password:
        return True
    else:
        return False


def generate_new_key():
    with open(key_file, 'w') as file:
        key = Fernet.generate_key()
        file.write(key.decode())


def get_key():
    with open(key_file, 'r') as file:
        global key
        key = file.readline().rstrip('\n')


def register_user(username, password):
    with open(users_file, 'r') as file:
        existing_users = file.readline().rstrip('\n')
        if len(existing_users) > 3:
            line_to_push = f", \"{username}\": \"{encrypt(password)}\"" + "}"
        else:
            line_to_push = f"\"{username}\": \"{encrypt(password)}\"" + "}"

        existing_users = str(existing_users)[0:-1] + line_to_push

    with open(users_file, 'w') as file:
        file.write(existing_users)


def signup():
    username = ""
    password = ""
    valid = False
    print("")
    while not (10 > len(username) > 3):
        username = str(input("Enter your username (4 to 9 characters): "))
    time.sleep(1)
    while not (15 > len(password) > 6):
        password = str(input("Enter your password (7 to 14 characters): "))
    time.sleep(1)

    if check_username_exist(username):
        print("")
        print("The username is already in use! Would you like to login instead?")
        time.sleep(1)
        print("")
        print("1. Log In")
        print("2. Try Again")
        print("")

        while not valid:
            try:
                choice = int(input("Enter your choice (1/2): "))
                while 0 > choice > 3:
                    choice = int(input("Enter your choice (1/2): "))
                valid = True
            except ValueError:
                pass

        match choice:
            case 1:
                login()
            case 2:
                signup()
    else:
        register_user(username, password)
        print("")
        print("You have been registered! Sending you to the login page to sign in...")
        time.sleep(2)
        login()


def login():
    username = ""
    password = ""
    valid = False
    print("")

    while not (10 > len(username) > 3):
        username = str(input("Enter your username (4 to 9 characters): "))
    time.sleep(1)
    while not (15 > len(password) > 6):
        password = str(input("Enter your password (7 to 14 characters): "))
    time.sleep(1)

    if check_username_exist(username):
        if check_login_match(username, password):
            print("")
            print("Login successful!")
        else:
            print("")
            print("Incorrect password! Try again!")
            time.sleep(2)
            login()
    else:
        print("")
        print("Username doesn't exist! Would you like to sign up instead?")
        time.sleep(1)
        print("")
        print("1. Sign Up")
        print("2. Try Again")
        print("")

        while not valid:
            try:
                choice = int(input("Enter your choice (1/2): "))
                while 0 > choice > 3:
                    choice = int(input("Enter your choice (1/2): "))
                valid = True
            except ValueError:
                pass

        match choice:
            case 1:
                signup()
            case 2:
                login()


def encrypt(plaintext):
    global key
    fernet = Fernet(key)

    ciphertext = fernet.encrypt(plaintext)
    return ciphertext


def decrypt(ciphertext):
    global key
    fernet = Fernet(key)
    plaintext = fernet.decrypt(ciphertext)
    return plaintext


if __name__ == '__main__':
    check_storage()
    from users import *
    from passwords import *

    get_key()
    login()
