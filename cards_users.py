import os
import hashlib
from getpass import getpass
import time

def h(word, salt):
    # takes about 5 seconds
    return hashlib.pbkdf2_hmac("sha256", word, salt, 500000, dklen=1024)

def encode(string):
    return string.encode("utf-8")

USERS_DIR = "users"
def users_dir(path=None):
    if path is None:
        if "USERS_DIR" in globals():
            global USERS_DIR
            return USERS_DIR
        else:
            return os.getcwd()
    else:
        return path

class User:
    def __init__(self, name, salt, key):
        assert isinstance(salt, bytes)
        assert isinstance(key, bytes)
        self.name = name
        self.salt = salt
        self.key = key

    def make(name, word):
        # name and word as str
        assert len(name) > 0
        assert len(word) > 0
        name = name
        salt = os.urandom(32)
        key = h(encode(word), salt)
        return User(name, salt, key)

    def find(name, path=None):
        path = users_dir(path)

        if not os.path.isdir(path):
            os.mkdir(path)

        files = os.listdir(path)
        
        path = os.path.join(path, name)

        if name in files:
            if os.path.isfile(path):
                with open(path, "r") as f:
                    try:
                        r = f.read()
                        spl = r.split(",")
                        salt, key = bytes.fromhex(spl[0]), bytes.fromhex(spl[1])
                        return User(name, salt, key)
                    except:
                        return

    def _verify(self, word): return self.key == h(word, self.salt)

    def cli_verify(self):
        word = getpass()
        verified = self._verify(encode(word))
        
        if verified: print("Matched")
        else: print("Didn't match")
        return verified

    def cli_add(self, path=None):
        path = users_dir(path)

        if not os.path.isdir(path):
            os.mkdir(path)

        if self.name not in os.listdir(path):
            path = os.path.join(path, self.name)
            with open(path, mode="w") as f:
                f.write(self.salt.hex() + "," + self.key.hex())
            print("Added account")
            return True

        print("Failed to add account")
        return False
        
    def cli_delete(self, path, word=None):
        path = users_dir(path)

        if not os.path.isdir(path):
            os.mkdir(path)
        
        verified = self.cli_verify() if word is None else self._verify(word)

        if verified:
            path = os.path.join(path, self.name)
            try:
                os.remove(path)
                print("Deleted account")
                return True
            except:
                pass

        print("Failed to delete account")
        return False


def cli_login(path=None):
    print("Login")
    path = users_dir(path)

    name = input("Username: ")
    u = User.find(name)
    
    word = getpass()

    if isinstance(u, User):
        if u._verify(encode(word)):
            print("Matched")
            return u
        else:
            print("Does not match")
            return None
    else:
        print("Does not exist")
        return None

def cli_register(path=None):
    print("Register")
    path = users_dir(path)

    name = input("Username: ")
    word = getpass()
    if len(name) == 0:
        print("Username not long enough")
        return

    if os.path.isfile(os.path.join(path, name)):
        print("Username taken")
        return

    if len(word) == 0:
        print("Password not long enough")
        return

    User.make(name, word).cli_add(path)

def cli_delete(path=None):
    print("Delete")
    path = users_dir(path)

    name = input("Username: ")
    u = User.find(name)
    if isinstance(u, User):
        u.cli_delete(path)
    else:
        print("User not found")
