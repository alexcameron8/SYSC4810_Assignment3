import os
from xml.dom import minidom, getDOMImplementation
from pathlib import Path
from dotenv import load_dotenv
from dict2xml import dict2xml
import password


def addUser(userName, pword, userRole):
    #Load environment variables (database file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')
    #Open existing file
    records = minidom.parse(DATABASE_RECORDS)


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

    #- Create new element password
    password = doc.createElement("password")
    #Note: Hash Password prior to creating record
    text = doc.createTextNode(pword)
    password.appendChild(text)
    user.appendChild(password)

    #- Create new element user_role
    user_role = doc.createElement("user_role")
    text = doc.createTextNode(userRole)
    user_role.appendChild(text)
    user.appendChild(user_role)

    #append new user to existing records
    XML1 = records.toprettyxml()
    XML2 = doc.toprettyxml()

    impl = getDOMImplementation()
    docs = impl.createDocument(None, "users", None)

    for s in [XML1, XML2]:
        elem = minidom.parseString(s).firstChild
        docs.firstChild.appendChild(elem)

    print(docs.childNodes[0].toprettyxml())   

    docs.childNodes[0].writexml( open('data.xml', 'w'),
               indent="",
               addindent="")

    # print(records.toprettyxml())
    # print(doc.toprettyxml())

    return ""


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

    # print('Newly Generated user id:')
    # print(newUserID+1)
    return newUserID+1

addUser("Alex", "Password", "Admin")
