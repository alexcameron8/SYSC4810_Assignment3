import os
from xml.dom import minidom
from pathlib import Path
from dotenv import load_dotenv

def passwordChecker(password):
    '''
    Problem 3 b)
    Password Checker based on provided password policy outlined by Finvest Holdings. 
    '''
    isAllowed = False

    if(password.contains('')):
        isAllowed = True

    return isAllowed


def verifyPassword(username, password):
    '''
    Problem 4 b)
    Password verification mechanism. Verifies password used to login matches password in password file. 
    '''
    isVerified = False
    with open('readme.txt') as f:
        lines = f.readlines()
    if():
        isVerified = True

    return isVerified


def getUserName(userID):
    '''
    Helper Function
    Queries the database of records and retrieves the username, provided a userID
    '''
    #initialize variables
    username = ""

    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    mydoc = minidom.parse(DATABASE_RECORDS)
    items = mydoc.getElementsByTagName('user')
    usernames = mydoc.getElementsByTagName('username')

    # all item attributes
    print('\nAll user ids:')
    for elem in items:
        # print(elem.attributes['id'].value) - debug
        # print("User ID:",userID) - debug
        if(int(userID)==int(elem.attributes['id'].value)):
            username = elem.getElementsByTagName('username')
            # print(username[0].firstChild.nodeValue) - debug
    return username[0].firstChild.nodeValue

getNewUserID()