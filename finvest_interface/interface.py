import sys
sys.path.append('./password')
sys.path.append('./access_control_policy')
import user, access_control_policy, password

def finvestPrototype():
    '''
    Command line user interfacem for Finvest Holdings Prototype solution.
    No python GUI module exists on the VM, therefore, the terminal is the only option for the interface...
    '''
    while True:
        print("------------------------------------------------------")
        print("Finvest Holdings")
        print("Client Holdings and Information System")
        print("------------------------------------------------------")
        
        action = ""
        while action !='r' and action !='l' and action !='e':
            action = input("Would you like to enrol a new user, login an existing user or exit?\n1. Type 'r' to enrol a user.\n2. Type 'l' to login an exsting user.\n3. Type 'e' to exit.\n>>")
            if action!='r' and action!='l' and action!='e':
                print("Invalid selection.")
        
        if action == 'r':
            register()
        elif action == 'l':
            login()
        else:
            print("\nGoodbye. Have a nice day.")
            exit(0) 

def register():
    isSuccess = False
    while not isSuccess:
        username =''; pword='';user_roles=[]
        print("--------------------------------------------")
        print("Finvest Holdings - Enrol New User")
        print("--------------------------------------------")
        print("Register New Finvest Holding User")

        #Request user credentials to register a new user
        while username =='':
            username = input("Username:")
            #Username cannot be empty
            if(username == ''):
                print('Username cannot be empty.')

        while pword =='':
            pword = input("Password:")
            #Password cannot be empty
            if(pword == ''):
                print('Password cannot be empty.')

        while len(user_roles) == 0:
            #Retrieve a list of possible user roles
            roles = access_control_policy.getAllRoles()
            print("Select New User Role(s)")
            print("(Role selection example: Client role: >>1   or multiple roles (Client, Financial Planner, Teller): >>1,4,7)\n")

            for i in range(len(roles)):
                print("{}.".format(i+1), roles[i])
            user_role_selection = input("Roles:")
            
            #Validate user response TO-DOOOOOOOOOOOOOOO
            #Validate user response TO-DOOOOOOOOOOOOOOO
            #Validate user response TO-DOOOOOOOOOOOOOOO
            # Validate the numbers are within the correct range
            # Validate the value provided is a digit
            #isValid = re.search('[a-zA-Z]', user_role_selection)

            if user_role_selection != '':
                if "," in user_role_selection:
                    user_roles = user_role_selection.split(',')
                    print(user_roles)
                else:
                    user_roles.append(user_role_selection)
                #Retrieve the roles in string format 
                str_user_roles = []
                for i in range(len(user_roles)):
                    str_user_roles.append(roles[int(user_roles[i])-1])
       
                print(str_user_roles)
            #Password cannot be empty
            if(len(user_roles) == 0):
                print('Must select at least one role for new user.')        
        
        print("Time to add user!")
        isSuccess, message = register_user(username, pword, str_user_roles)
        if isSuccess:
            print(message)
        else:
            print(message)


def login():
    isSuccess = False
    while not isSuccess:
        username =''; pword=''
        print("--------------------------------------------")
        print("Finvest Holdings - User Login")
        print("--------------------------------------------")
        print("Please login with your user credentials below")
        #Request user credentials to login
        while username =='':
            username = input("Username:")
            #Username cannot be empty
            if(username == ''):
                print('Username cannot be empty.')
        while pword =='':
            pword = input("Password:")
            #Password cannot be empty
            if(pword == ''):
                print('Password cannot be empty.')
        
        #Attempt to log user in       
        isSuccess, message = login_user(username,pword)
        #print the resulting message
        print(message,"\n")

def login_user(username, pword):
    isSuccess = False
    message = ""
    if not username:
        message = 'Username field is empty.'
        return isSuccess, message
    elif not pword:
        message='Password field is empty.'
        return isSuccess, message
    else:
        isSuccess, message = password.verifyCredentials(username,pword)
        #User successfully added
        if isSuccess:
            #Display a list of the logged in users privileges based on their role.
            access_control(username)
            return isSuccess, message
        #User unsuccessfully added   
        else:
            return isSuccess, message

def register_user(username,password,userRoles):
    isSuccess = False
    if not username:
        message ='Register', 'Username field is empty.'
        return isSuccess, message
    elif not password:
        message ='Password field is empty.'
        return isSuccess, message
    elif len(userRoles) == 0:
        message ='Register', 'No roles selected. Please select at least one user role.'
        return isSuccess, message
    else:
        isSuccess, message = user.addUser(username,password,userRoles)
        #User successfully added
        if isSuccess:
            print("User registered, please login.")
            login()
            return isSuccess, message
        #User unsuccessfully added   
        else:
            return isSuccess, message
    return 

def access_control(username):
    print("\nWelcome, {}".format(username))

    #Retrieve user role(s)
    user_roles = access_control_policy.getRoles(username)

    #Retrieve corresponding permissions for those roles
    user_permissions = access_control_policy.getPermissions(user_roles)

    #Retrieve user information, roles, permissions and display to user.
    print("Account Privileges:")

    for perms in user_permissions:
        print("-", perms)
    t=''
    while t =='':
        t = input("\nPress any key and hit enter to continue to Finvest Holdings main screen.\n>>") 

finvestPrototype()