import os
from xml.dom import minidom, getDOMImplementation
from pathlib import Path
from dotenv import load_dotenv
from dict2xml import dict2xml
import sys
sys.path.append('./password')
import password, cryptpass

def addUser(userName, pword, userRole):

    #Password Validation
    passwordResult, message = password.passwordChecker(userName, pword)
    #If the proactive password checker determines the password is invalid, user not added.
    if not passwordResult:
        return False, message
    
    #Load environment variables (database file)
    load_dotenv()

    # Create new user record to append to database
    #- Create new XML document with its root element
    doc = minidom.parseString("<users/>")
    root = doc.documentElement

    #- Create new element
    user = doc.createElement("user")
    user.setAttribute("id",str(getNewUserID()))

    #- Add new user element to root
    root.appendChild(user)

    #- Create new element username
    username = doc.createElement("username")
    text = doc.createTextNode(userName)
    username.appendChild(text)
    user.appendChild(username)

    # Hash Password before appending to password records
    pass_salt, hashed_pass = cryptpass.hash_password(pword)

    #- Create new element password
    salt_pass = doc.createElement("salt")

    text = doc.createTextNode(pass_salt.hex())
    salt_pass.appendChild(text)
    user.appendChild(salt_pass)

    #- Create new element password
    pass_hash = doc.createElement("password")
    text = doc.createTextNode(hashed_pass.hex())
    pass_hash.appendChild(text)
    user.appendChild(pass_hash)

    #- Create new element password
    passw = doc.createElement("temp_test_pw")
    text = doc.createTextNode(pword)
    passw.appendChild(text)
    user.appendChild(passw)

    #- Create new element user_role
    user_role = doc.createElement("user_role")
    text = doc.createTextNode(','.join(str(item) for item in userRole))
    user_role.appendChild(text)
    user.appendChild(user_role)

    #append new user to existing records
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    records = minidom.parse(DATABASE_RECORDS)
    users_append = records.getElementsByTagName('users')[0]
    
    users_append.appendChild(user)
    new_user_record = users_append.toprettyxml()

    save_path_file = DATABASE_RECORDS
  
    with open(save_path_file, "w") as f:
        f.write(new_user_record) 
    i = 0
    with open(DATABASE_RECORDS, 'r') as r, open('temp.txt', 'w') as o:
        for line in r:
            #strip() function
            if line.strip():
                o.write(line)
    #Removing temporary variable
    if os.path.exists(DATABASE_RECORDS):
        os.remove(DATABASE_RECORDS)
    os.rename("temp.txt",DATABASE_RECORDS)
    if os.path.exists("temp.txt"):
        os.remove("temp.txt")

    message = 'User Successfully Enroled. Please login to continue.'

    return True, message


def getNewUserID():
    '''
    Helper Function
    Queries the database of records and retrieves the next new unique user ID.
    '''
    #initialize variables
    newUserID = -1
    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    mydoc = minidom.parse(DATABASE_RECORDS)
    items = mydoc.getElementsByTagName('user')

    # Iterate through all existing user ID records already assigned to existing users in records
    for elem in items:
        newUserID = int(elem.attributes['id'].value)

    return newUserID+1


def getRecords():
    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    mydoc = minidom.parse(DATABASE_RECORDS)
    users_append = mydoc.getElementsByTagName('users')
    user = mydoc.getElementsByTagName('user')

    for elem in user:
        newUserID = int(elem.attributes['id'].value)
        print(newUserID)
    
    users_append.appendChild()


    return ""
