import json


def main():
    print("1. Login")
    print("2. Sign Up")
    user_input = input("Which would you like to do, use the number index: ")
    if user_input == "1":
        login()
    elif user_input == "2":
        sign_up_set_username()
    else:
        print("Not a valid option, please try again")
        main()


def login():
    login_username = input("Please enter your username: ")
    accounts = read_accounts()
    if login_username in accounts:
        login_username_found(login_username)
    else:
        login_username_incorrect(login_username)


def login_username_found(username):
    print("username was found")
    remaining_attempts = 3
    while True:
        attempted_password = input("Enter password: ")
        accounts = read_accounts()
        if attempted_password == accounts[username]:
            print("successful login!")
            successful_login(username)
            break
        else:
            remaining_attempts = remaining_attempts - 1
            if remaining_attempts <= 0:
                print("login attempts exceeded, returning home.")
                main()
                break
            else:
                print(f"Incorrect password please try again. {remaining_attempts} attempts left.")


def login_username_incorrect(invalid_username):
    print(f"{invalid_username} not found, would you like to ")
    print("1. Try a different username")
    print("2. sign up with username")
    user_input = input("Please use numerical index: ")
    if user_input == "1":
        login()
    elif user_input == "2":
        sign_up_set_password(invalid_username)
    else:
        print("Not a valid option, please try again")
        login_username_incorrect(invalid_username)


def sign_up_set_username():
    new_username = input("Set username: ")
    accounts = read_accounts()
    if new_username in accounts:
        print(f"{new_username} already exist, please choose another username")
        sign_up_set_username()
    else:
        sign_up_set_password(new_username)


def sign_up_set_password(username):
    new_password = input("Set password: ")
    confirm_password = input("Confirm password: ")

    if new_password != confirm_password:
        print("passwords do not match, please try again")
        sign_up_set_password(username)
    else:
        accounts = read_accounts()
        accounts[username] = new_password
        save_accounts(accounts)
        print(f"congratulations {username}, your account was created successfully!")
        successful_login(username)


def read_accounts():
    try:
        with open("accounts.json", "r") as saved_accounts:
            return json.load(saved_accounts)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}


def save_accounts(accounts):
    with open("accounts.json", "w") as saved_accounts:
        json.dump(accounts, saved_accounts, indent=4)


def successful_login(username):
    print(f"welcome {username}!")
    print("1. logout")
    print("2. delete account")
    user_action = input("What would you like to do?: ")
    if user_action == "1":
        main()
    elif user_action == "2":
        accounts = read_accounts()
        try:
            accounts.pop(username)
            save_accounts(accounts)
            main()
        except KeyError:
            print("Account doesnt exist")
    else:
        print("Not a valid option, please try again")
        successful_login(username)


main()

