import os
import hashlib

def hash_password(password: str):
    """
    Hash the provided password with a randomly-generated 32 byte salt and return the salt and hash to store in the database.
    """
    #Generate random salt value of length 32 bytes
    salt = os.urandom(32) 

    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # Store them as:
    salt_hash = salt + pw_hash 

    # Retrieving the values from password file
    salt_from_db = salt_hash[:32] # 32 is the length of the salt
    pw_hash_from_db = salt_hash[32:]
    print("Length:",len(pw_hash))
    print("Length:",len(salt_hash))
    print("Salt",salt)
    print("PW_hash",pw_hash, "\n")
    
    return salt, pw_hash

def is_correct_password(salt: bytes, pw_hash: bytes, pword: str):
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    print("Salt",salt)
    print("PW_HAsH", pw_hash)
    print("Password:", pword)

    new_hash = hashlib.pbkdf2_hmac('sha256', pword.encode(), salt, 100000)

    if new_hash == pw_hash:
        print("Password check success:", pword)
        return True
    else:
        print("Password check failed:", pword)
        print(new_hash, "Entered Type:",type(new_hash))
        print(pw_hash, "Database Type:", type(pw_hash))
        return False

# salt, pw_hash = hash_password('Test123!')
# is_correct_password(salt, pw_hash, 'Password123')
# is_correct_password(salt, pw_hash, 'Test123!')