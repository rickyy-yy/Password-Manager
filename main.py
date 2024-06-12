import string
import random
from cryptography.fernet import Fernet
import os
import time
import json
import importlib.util

pc_user = os.getlogin()
users_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\users.py"
passwords_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\passwords.json"
key_file = f"C:\\Users\\{pc_user}\\Documents\\Password Manager\\key.txt"

key: str
logged_in_user: str
logged_in_password: str


def check_storage():
    if not os.path.isfile(users_file):
        with open(users_file, 'x') as file:
            file.write("registered_users_dict = {}")

    if not os.path.isfile(passwords_file):
        with open(passwords_file, 'x') as file:
            file.write("{}")

    if not os.path.isfile(key_file):
        with open(key_file, 'x') as file:
            generate_new_key()


def is_password_unique(password):
    data = get_password_json()
    encrypted_passwords = []
    decrypted_passwords = []
    for item in data[logged_in_user]:
        encrypted_passwords += list(item.values())

    for encrypted in encrypted_passwords:
        decrypted_passwords.append((decrypt(encrypted)))

    if password in decrypted_passwords:
        return False
    return True


def is_note_unique(note):
    data = get_password_json()
    for item in data[logged_in_user]:
        if note in item:
            return False

    return True


def check_username_exist(username):
    global registered_user_dict
    spec = importlib.util.spec_from_file_location("users", users_file)
    users_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(users_module)
    registered_users_dict = users_module.registered_users_dict
    usernames = list(registered_users_dict.keys())
    if username in usernames:
        return True
    else:
        return False


def check_user_has_passwords():
    data = get_password_json()
    if logged_in_user in data:
        return True
    return False


def check_login_match(username, password):
    global key
    global registered_user_dict
    spec = importlib.util.spec_from_file_location("users", users_file)
    users_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(users_module)
    registered_users_dict = users_module.registered_users_dict
    usernames = list(registered_users_dict.keys())
    encrypted_passwords = list(registered_users_dict.values())
    index = usernames.index(username)

    real_password = encrypted_passwords[index]
    print(real_password)
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


def get_password_json():
    with open(passwords_file, 'r') as file:
        data = json.load(file)

    return data


def write_password_json(json_data):
    with open(passwords_file, 'w') as file:
        file.write(json.dumps(json_data, indent=4))


def register_user(username, password):
    with open(users_file, 'r') as file:
        existing_users = file.readline().rstrip('\n')
        if len(str(existing_users)) > 26:
            line_to_push = f", \"{username}\": \"{encrypt(password).decode()}\"" + "}"
        else:
            line_to_push = f"\"{username}\": \"{encrypt(password).decode()}\"" + "}"

        existing_users = str(existing_users)[0:-1] + line_to_push

    with open(users_file, 'w') as file:
        file.write(existing_users)


def signup():
    username = ""
    password = ""
    valid = False
    print("Sign Up Page")
    print("============")
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
    print("Log In Page")
    print("===========")

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
            global logged_in_password
            global logged_in_user
            logged_in_password = password
            logged_in_user = username
            main_menu()
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


def login_or_signup():
    valid = False
    print("Welcome to the app. Before we proceed, you need to log in or sign up.")
    print("")
    print("1. Log In")
    print("2. Sign Up")
    print("3. Exit Program")
    print("")

    while not valid:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            while 0 > choice > 4:
                choice = int(input("Enter your choice (1/2/3): "))
            valid = True
        except ValueError:
            pass

    match choice:
        case 1:
            login()
        case 2:
            signup()
        case 3:
            exit()


def main_menu():
    global logged_in_password
    global logged_in_user
    valid = False
    print("")
    print("Would you like to:")
    print("")
    print("1. Manage Passwords")
    print("2. Generate a Random Password")
    print("3. Log Out")
    print("")

    while not valid:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            while 0 > choice > 3:
                choice = int(input("Enter your choice (1/2/3): "))
            valid = True
        except ValueError:
            pass

    match choice:
        case 1:
            passwords_manager()
        case 2:
            generate_rand_password()
        case 3:
            logged_in_user = ""
            logged_in_password = ""
            print("You have been logged out...")
            time.sleep(1)
            login_or_signup()


def passwords_manager():
    global logged_in_password
    global logged_in_user

    print("")
    print(f"You are currently signed as in: {logged_in_user}")
    print("Would you like to:")
    print("")
    print("1. View Passwords")
    print("2. Add a Password")
    print("3. Delete a Password")
    print("4. Go Back to Main Menu")
    print("")

    while not valid:
        try:
            choice = int(input("Enter your choice (1/2/3/4): "))
            while 0 > choice > 5:
                choice = int(input("Enter your choice (1/2/3/4): "))
            valid = True
        except ValueError:
            pass

    match choice:
        case 1:
            view_passwords()
        case 2:
            add_password()
        case 3:
            del_password()
        case 4:
            main_menu()


def generate_rand_password():
    global logged_in_password
    global logged_in_user
    valid = False
    rand_password = ""
    print("")
    print("Generating random secure password...")
    time.sleep(2)
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(14):
        rand_password += (random.choice(characters))

    while not is_password_unique(rand_password):
        for i in range(14):
            rand_password += (random.choice(characters))

    print(f"Random Password: {rand_password}")
    print("")
    print("Would you like to save this password to your account? (Y/N)")

    while not valid:
        try:
            choice = str(input("Enter your choice (Y/N): ")).lower()
            while choice != "y" and choice != "n":
                choice = int(input("Enter your choice (Y/N): "))
            valid = True
        except ValueError:
            pass

    match choice:
        case "y":
            save_password(rand_password)
        case "n":
            print("Alright, sending you back to the main menu...")
            time.sleep(2)
            main_menu()


def save_password(password):
    global logged_in_user
    print("")
    print(f"You are saving {password} to your account.")
    note = str(input("Please enter an identifier to assign to this password so you know what it is for: "))

    data_json = get_password_json()

    if logged_in_user in data_json:
        data_json[logged_in_user].append({note: encrypt(password).decode()})
    else:
        data_json[logged_in_user] = [{note: encrypt(password).decode()}]

    if is_note_unique(note):
        write_password_json(data_json)
        time.sleep(1)
        print("")
        print("Password has been saved! Returning you to main menu...")
        time.sleep(1)
        main_menu()
    else:
        print("There is already a password with this note! ")
        save_password(password)


def view_passwords():
    global logged_in_password
    passwords = []
    notes = []
    decrypted_passwords = []
    index = 0

    if check_user_has_passwords():
        print("")
        print("Your Passwords")
        print("==============")
        data = get_password_json()
        for item in data[logged_in_user]:
            notes += item.keys()
            passwords += item.values()
        for encrypted in passwords:
            decrypted_passwords.append(decrypt(encrypted))
        for i in range(len(passwords)):
            print(f"{index + 1}) Identifier: {notes[index]}, Password: {decrypted_passwords[index]}")
            index += 1
    else:
        print("")
        print("You do not have any passwords saved yet! Sending you to main menu...")
        time.sleep(1)
        main_menu()


def add_password():
    global logged_in_user
    password_to_add = str(input("Enter the password you wish to add: "))

    save_password(password_to_add)


def del_password():
    data = get_password_json()
    valid = False

    view_passwords()

    print("")
    note = str(input("Enter the identifier of the password you want to delete: "))

    if is_note_unique(note):
        print("")
        print("The identifier you entered does not exist! Would you like to:")
        print("")
        print("1. Try again")
        print("2. Back to Main Menu")
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
                del_password()
            case 2:
                main_menu()
    else:
        for item in data[logged_in_user]:
            if note in item:
                del item
                break

        write_password_json(data)

        print("")
        print("Password deleted successfully! Would you like to:")
        print("")
        print("1. Delete another password")
        print("2. Back to Main Menu")
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
                del_password()
            case 2:
                main_menu()


def encrypt(plaintext):
    global key
    fernet = Fernet(key)

    ciphertext = fernet.encrypt(plaintext.encode())
    return ciphertext


def decrypt(ciphertext):
    global key
    fernet = Fernet(key)
    plaintext = fernet.decrypt(ciphertext).decode()
    return plaintext


if __name__ == '__main__':
    check_storage()
    get_key()

    login_or_signup()
