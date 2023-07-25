from appJar import gui
import json


def set_screen(screen_index):
    if screen_index == "0":
        win.selectFrame("Screens", 0)
    elif screen_index == "1":
        win.selectFrame("Screens", 1)
    elif screen_index == "2":
        win.selectFrame("Screens", 2)
        validate_new_username()
        validate_new_password()
    else:
        print("something has gone wrong")


def validate_login():
    username = win.getEntry("Username: ")
    password = win.getEntry("Password: ")
    accounts = read_accounts()
    if username in accounts:
        if password == accounts[username]:
            win.infoBox("ls", "Login successful!")
            set_screen("1")
        else:
            win.errorBox("pi", "Password incorrect!")
    else:
        win.errorBox("ude", "Username doesn't exist!")


def validate_new_username():
    accounts = read_accounts()
    username = win.getEntry("New Username: ")

    if len(username) == 0:
        win.setValidationEntry("New Username: ", state="wait")
    elif username in accounts:
        win.setValidationEntry("New Username: ", state="invalid")
    else:
        win.setValidationEntry("New Username: ", state="valid")

    if win.getCurrentFrame("Screens") == 2:
        win.after(500, validate_new_username)


def validate_new_password():
    new_pass = win.getEntry("New Password: ")
    confirm_pass = win.getEntry("Confirm Password: ")

    if len(new_pass) == 0 and len(confirm_pass) == 0:
        win.setValidationEntry("New Password: ", state="wait")
        win.setValidationEntry("Confirm Password: ", state="wait")
    elif len(new_pass) == 0 and len(confirm_pass) > 0:
        win.setValidationEntry("New Password: ", state="wait")
        win.setValidationEntry("Confirm Password: ", state="valid")
    elif len(new_pass) > 0 and len(confirm_pass) == 0:
        win.setValidationEntry("New Password: ", state="valid")
        win.setValidationEntry("Confirm Password: ", state="wait")
    elif new_pass != confirm_pass:
        win.setValidationEntry("New Password: ", state="invalid")
        win.setValidationEntry("Confirm Password: ", state="invalid")
    else:
        win.setValidationEntry("New Password: ", state="valid")
        win.setValidationEntry("Confirm Password: ", state="valid")

    if win.getCurrentFrame("Screens") == 2:
        win.after(500, validate_new_password)


def create_account():
    accounts = read_accounts()
    username = win.getEntry("New Username: ")
    new_pass = win.getEntry("New Password: ")
    confirm_pass = win.getEntry("Confirm Password: ")
    if username not in accounts and new_pass == confirm_pass:
        win.infoBox("acs", "Account created successfully!")
        accounts[username] = new_pass
        write_accounts(accounts)
        set_screen("1")
    elif username in accounts:
        win.errorBox("uat", "Username already taken!")
    elif new_pass != confirm_pass:
        win.errorBox("pdm", "Passwords dont match!")


def read_accounts():
    try:
        with open("accounts.json", "r") as saved_accounts:
            return json.load(saved_accounts)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}


def write_accounts(new_accounts):
    with open("accounts.json", "w") as saved_accounts:
        json.dump(new_accounts, saved_accounts, indent=4)


win = gui("Account Manager")

with win.frameStack("Screens", start=0, rowspan=5, colspan=5):
    win.setBg("grey")
    win.setFg("black")
    win.setSize("500x300")

    with win.frame("0"):
        win.resizable = False
        win.startLabelFrame("Login Details")
        win.setPadX(100)
        win.addLabelEntry("Username: ", 1, 0)
        win.addSecretLabelEntry("Password: ", 2, 0)
        win.setFocus("Username: ")
        win.addButton("Submit", validate_login, 3, 0)
        win.addNamedButton("Sign up", "2", set_screen, 4, 0)
        win.stopLabelFrame()

    with win.frame("1"):
        win.addLabel("LogIn", "Welcome User!")

    with win.frame("2"):
        win.setSticky("")
        win.addNamedButton("Return", "0", set_screen)
        win.addLabelValidationEntry("New Username: ", 1, 0)
        win.addLabelValidationEntry("New Password: ", 2, 0)
        win.addLabelValidationEntry("Confirm Password: ", 3, 0)
        win.addButton("Create", create_account)

win.go()
