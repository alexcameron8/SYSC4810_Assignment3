from dotenv import load_dotenv
import os
from xml.dom import minidom

#For simplicity, the roles were hardcoded, but a better solution would be to iterate through the access control policy to retrieve all roles
roles = ["Client", "Premium Client", "Financial Advisor", "Financial Planner", "Investment Analyst", "Technical Support", "Teller", "Compliance Officer"]

def getAllRoles():
    roles_list = []
    #Load environment variables (access control policy file)
    load_dotenv()
    ACCESS_CONTROL_POLICY = os.getenv('ACCESS_CONTROL_POLICY')
    mydoc = minidom.parse(ACCESS_CONTROL_POLICY)
    roles = mydoc.getElementsByTagName('role')
    #Iterate through all roles in the access control policy file and append to a list of all roles
    for role in roles:
        roles_list.append(role.attributes['id'].value)
    return roles_list

def getPermissions(user_roles: list):
    #List of user permissions
    user_permissions = []
    
    #Load environment variables (password file)
    load_dotenv()
    ACCESS_CONTROL_POLICY = os.getenv('ACCESS_CONTROL_POLICY')

    mydoc = minidom.parse(ACCESS_CONTROL_POLICY)
    roles = mydoc.getElementsByTagName('role')
    #Iterate through all roles of a given user
    for user_role in user_roles:
        for role in roles:
            #If a user role matches the role in the access control policy file, append the permission to the permissions file.
            if(user_role==role.attributes['id'].value):
                permissions = role.getElementsByTagName('permission')
                i=0
                while i < len(permissions):
                    #Retrieve the permission for the role
                    roles_str = permissions[i].firstChild.nodeValue
                    #Retrieve the access level of the permission for the given role
                    if permissions[i].attributes['access'].value == "r":
                        roles_str = "View " + permissions[i].firstChild.nodeValue
                    elif permissions[i].attributes['access'].value == "rw":
                        roles_str = "Modify " + permissions[i].firstChild.nodeValue
                    elif permissions[i].attributes['access'].value == "rwo":
                        roles_str = "Own " + permissions[i].firstChild.nodeValue
                    user_permissions.append(roles_str)

                    i +=1
    return user_permissions


def getRoles(username : str):
    #Load environment variables (password file)
    load_dotenv()
    DATABASE_RECORDS = os.getenv('DATABASE_RECORDS')

    mydoc = minidom.parse(DATABASE_RECORDS)
    users = mydoc.getElementsByTagName('user')
    # all user
    for elem in users:
        if(username== elem.getElementsByTagName('username')[0].firstChild.nodeValue):
            user_roles = elem.getElementsByTagName('user_role')
            roles_str = user_roles[0].firstChild.nodeValue

    #Append roles retrieved from passwd.txt file to an array of roles
    roles = []
    if "," in roles_str:
        roles = roles_str.split(',')
    else:
        roles.append(roles_str)
    return roles
    
    return roles

getAllRoles()