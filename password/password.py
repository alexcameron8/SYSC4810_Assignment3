import os
from xml.dom import minidom
from pathlib import Path
from dotenv import load_dotenv
import re
import sys
sys.path.append('./password')
import cryptpass

def passwordChecker(username, password):
    '''
    Problem 3 b)
    Password Checker based on provided password policy outlined by Finvest Holdings. 
    Password requirements include: 
    1. 8-12 characters in length 
    2. Password must include at least:
        * one upper-case letter;
        * one lower-case letter;
        * one numerical digit, and
        * one special character from the set: {!, @, #, $, %, ?, ∗}
    3. Passwords found on a list of common weak passwords (e.g., Password1, Qwerty123, or Qaz123wsx)
        must be prohibited (Must be flexible)
    4. Passwords matching the format of calendar dates, license plate numbers, telephone numbers, or other
        common numbers must be prohibited
    5. Passwords matching the user ID must be prohibited 
    '''
    # If all conditions are satisfied then isVerified will return true and password is valid.
    isVerified = False
    message = ""

    #Additional check: Check if username is unique to database of users
    if not isUsernameUnique(username):
        message = "Invalid username: Username already exists, please choose a different username."
        isVerified = False
        return isVerified, message

    # Condition Check #1: 8-12 characters in length 
    # Condition Check #2: Must contain one upper-case letter; one lower-case letter;one numerical digit, and one special character from the set: {!, @, #, $, %, ?, ∗}
    #Regex expression
    regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@$#$%?*-])[A-Za-z\d@$!#%*?&]{8,12}$"

    passwordCheck = re.search(re.compile(regular_expression),password)
    if not passwordCheck:
        message = "Invalid Password: Password must be 8-12 characters and contain one upper-case letter,one lower-case letter,one numerical digit, and one special character from the set: {!, @, #, $, %, ?, ∗}"
        isVerified = False
        return isVerified, message

    # Condition Check #3: Passwords found on a list of common weak passwords (e.g., Password1, Qwerty123, or Qaz123wsx) must be prohibited (Must be flexible)
    #Retrieve prohibited passwords list
    prohibitedPasswordsList = getProhibitedPasswords()

    for illegalPasswords in prohibitedPasswordsList:
        if illegalPasswords == password:
            message = "Invalid Password: Prohibited password selected. Please try a different password."
            isVerified = False
            return isVerified, message

    # Condition Check #4: Passwords matching the format of calendar dates, license plate numbers, telephone numbers, or other common numbers must be prohibited
    # Regex pattern to check for calendar date format: 'dd-MM-YYYY'
    regex_date1 = "^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$"
    isDate = re.search(regex_date1,password)
    if isDate:
        message = "Invalid password: Illegal format: 'dd-mm-YYYY'"
        isVerified = False
        return isVerified, message

    # Regex pattern for license plate numbers. Example format: AAAA123
    regex_license_plate = r"^[A-Z]{4}\d{1,3}$"
    isLicensePlate = re.compile(regex_license_plate).search(password)
    if isLicensePlate:
        message = "Invalid password: Illegal format: License plate"
        isVerified = False
        return isVerified, message
    
    # Regex pattern for telephone numbers in format: ###-###-###
    regex_phone = r"\d\d\d-\d\d\d-\d\d\d\d"
    isPhone = re.compile(regex_phone).search(password)
    if isPhone:
        message = "Invalid password: Illegal format: Telephone format"
        isVerified = False
        return isVerified, message

    #Regex pattern to check for Canadian postal codes. Example format: K3B7V9 
    regex_ca = "^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d$"
    isPostal = re.search(re.compile(regex_ca),password)

    if isPostal:
        message = "Invalid password: Illegal format: Postal Code"
        isVerified = False
        return isVerified, message

    # Condition Check #5: Passwords matching the user ID must be prohibited 
    if username == password:
        message = "Invalid Password: Password cannot match username."
        isVerified = False
        return isVerified, message

    isVerified = True
    if isVerified:
        message = "Valid Password"
    return isVerified, message

def verifyCredentials(username, login_pword):
    '''
    Problem 4 b) Implement the password verification mechanism
    '''
    isVerified = False
    message = ""
    
    #Iterate through database records to find if provided username exists in password file.
    userExists, salt, pword = checkUserName(username)
    if userExists:
       # print(bytes.fromhex(pword))
        pwMatch = cryptpass.is_correct_password(bytes.fromhex(salt),bytes.fromhex(pword),login_pword)
        if pwMatch:
            message = "Password matches with provided password."
            isVerified = True
            return isVerified, message
        else:
            message = "Invalid Password"
    else:
        message = "Invalid Username: Username does not exist." 


    return isVerified, message 

def isUsernameUnique(username):
    '''
    Helper Function
    Queries the database of records and checks if the username already exists
    '''
    isUniqueUsername = True
    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')
    mydoc = minidom.parse(DATABASE_RECORDS)
    items = mydoc.getElementsByTagName('user')

    for elem in items: 
        if(username == elem.getElementsByTagName('username')[0].firstChild.nodeValue):
            isUniqueUsername = False
    return isUniqueUsername

def checkUserName(username):
    '''
    Helper Function
    Queries the database of records and retrieves the username, provided a userID
    '''
    #initialize variables
    userExist = False

    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    mydoc = minidom.parse(DATABASE_RECORDS)
    items = mydoc.getElementsByTagName('user')

    # Iterate through all user records and check if provided username exists in password file.
    for elem in items:
        if(username== elem.getElementsByTagName('username')[0].firstChild.nodeValue):
            userExist = True
            salt = elem.getElementsByTagName('salt')[0].firstChild.nodeValue
            password = elem.getElementsByTagName('password')[0].firstChild.nodeValue
            return userExist, salt, password

    return userExist, "", ""

def getProhibitedPasswords():
    '''
    Helper Function
    Queries the database (text file) of prohibited passwords and returns a list of all prohibited passwords. 
    '''
    #initialize variables
    prohibitedPasswordsList = []

    #Load environment variables (prohibited password text file)
    load_dotenv()
    PROHIBITED_PASSWORDS = os.getenv('PROHIBITED_PASSWORDS')
    prohibitedPasswordsList = open(PROHIBITED_PASSWORDS).read().splitlines()
    
    return prohibitedPasswordsList

def addProhibitedPassword(prohibitedPassword):
    '''
    Helper Function
    Adds a new prohibited password to the database (text file) of prohibited passwords. 
    '''
    
    #Load environment variables (prohibited password text file)
    load_dotenv()
    PROHIBITED_PASSWORDS = os.getenv('PROHIBITED_PASSWORDS')

    #Open Prohibited Passwords text file and add new identified password.
    with open(PROHIBITED_PASSWORDS, 'a') as fd:
        fd.write("\n" + prohibitedPassword)


# # Testing all special characters (Valid)
# print("Test 1: user: 'alexjcameron' password: 'Test123!'")
# verifyPassword("alexjcameron", "Test123!")

# # Testing prohibited password checker (Invalid)
# print("\nTest 2: user: 'alexjcameron' password: 'Password123!'")
# verifyPassword("alexjcameron", "Password123!")

# # Testing password length checker (Invalid)
# print("\nTest 3: user: 'alexjcameron' password: 'Test1!'")
# verifyPassword("alexjcameron", "Test1!")

# #The following test cases will be invalid at the special character, length, upper, lower, digit check, so to confirm the logic works, the first case is commented out.
# # Testing calendar dates dd-MM-YYYY (Invalid)
# print("\nTest 4: user: 'alexjcameron' password: '10-12-2000'")
# verifyPassword("alexjcameron", "10-12-2000")

# # The following test cases will be invalid at the special character, length, upper, lower, digit check, so to confirm the logic works, the first case is commented out.
# # Testing phone number (Invalid)
# print("\nTest 5: user: 'alexjcameron' password: '613-555-1234'")
# verifyPassword("alexjcameron", "613-555-1234")

# #The following test cases will be invalid at the special character, length, upper, lower, digit check, so to confirm the logic works, the first case is commented out.
# # Testing license plate (Invalid)
# print("\nTest 6: user: 'alexjcameron' password: 'AHMO 123'")
# verifyPassword("alexjcameron", "AHMO 123")

# # Testing password length checker (Invalid)
# print("\nTest 7: user: 'alexcam12!' password: 'alexcam12!")
# verifyPassword("Alexcam12!", "Alexcam12!")


#Test Cases for verifying new prohibited passwords can be added to the text file storing all prohibited passwords
# getProhibitedPasswords()
# addProhibitedPassword("ThisIsNotAllowed123")
# getProhibitedPasswords()
