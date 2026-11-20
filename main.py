import base64
import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet
from getpass import getpass
import json
storage = {}
master_password = getpass("Enter a master password: ")

salt = os.urandom(16)
def key_generation(password):
    pwd = password.encode("utf-8")
    key = hash_secret_raw(
        secret=pwd,
        salt=salt,
        type=Type.ID,
        time_cost=3,
        parallelism=4,
        hash_len=32,
        memory_cost=65536
    )

    fernet_key = base64.urlsafe_b64encode(key)

    return fernet_key

data = key_generation(master_password)
def encryption(password, username):
    credentials = {
        "username":username,
        "password":password
    }

    credentials_json = json.dumps(credentials)
    fernet = Fernet(data)

    encrypted_credentials = fernet.encrypt(credentials_json.encode("utf-8"))
    return encrypted_credentials

#{'github': b'gAAAAABrAD8deM_BClwacebMxSo5E-zQY-a2hAlOpIng4vrUBKxH6xjay4FKMJFTp6HdY3rs2wX06xqlYIAfEpDw_faIQMJHkQ1wUKj3Dl0vMhP3H8v94zYCufOtGarnkB0F4ESP0dg9'}




def decryption(encrypted_credentials):
    fernet = Fernet(data)

    decrypted_credentials = fernet.decrypt(encrypted_credentials)
    return json.loads(decrypted_credentials.decode("utf-8")) #JSON Text into Python Dictionary

def save_info(credential, website):
    storage[website] = credential

def show_storage():
    if len(storage) == 0:
        print("\nThere are no stored passwords.\n")
        return
    print(storage)
    for website, credentials in storage.items():
        decrypted_data = decryption(credentials)
        print(decrypted_data)
        print("Website: ", website)
        print("Username: ", decrypted_data["username"])
        print("Password: ", decrypted_data["password"])


def password_manager():
    while True:
        print("Password Manager | Save Your Passwords and Keep Them Secure!")
        print("Select any of the below choices: ")
        print("---Password Manager---")
        print("1. Add a new Password.")
        print("2. View Saved Passwords.")
        print("3. Exit.")
        choice = input("Enter your Choice: ")
        if choice == "1":
            website = input("Enter the website or app name: ")
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            encrypted_credential = encryption(password, username)
            save_info(encrypted_credential, website)
            print("Your password has been successfully saved.\n\n")
        elif choice == "2":
            show_storage()
        elif choice == "3":
            return

password_manager()
