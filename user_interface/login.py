from tkinter import *
from tkinter import messagebox
import sys
#Import functions from other modules
sys.path.append('./password')
sys.path.append('./access_control_policy')
import user, access_control_policy, password

main_screen = Tk()   # create a GUI window 
global roles_list 

def main_account_screen():

    main_screen.geometry("500x500") # set the configuration of GUI window 
    main_screen.title("Finvest Holdings - Enrol / Login") # Title of Interface
    
    # create a Form label 
    Label(text="SYSC4810 - Assignment 3", bg="grey", width="300", height="1", font=("Calibri bold", 15)).pack() 
    # create a Form label 
    Label(text="Finvest Holdings Prototype\nLogin Or Register a New User Below", width="300", font=("Calibri bold", 15)).pack(pady = 5) 

    # create a register button
    Button(text="Register",font=("Calibri bold", 12), height="4", width="80", command=register).pack(padx = 30,pady = 5)

    # create Login Button 
    Button(text="Login",font=("Calibri bold", 12), height="4", width="80", command=login).pack(padx = 30,pady = 5)
    
    # start the GUI
    main_screen.mainloop() 

def register():

    register_screen = Toplevel(main_screen) 
    register_screen.title("Finvest Holdings - Enrol New User")
    register_screen.geometry("500x500")
 
    # Set text variables
    username = StringVar()
    password = StringVar()
    
    # Set label for user's instruction
    Label(register_screen, text="Register New Finvest Holding User", font=("Calibri bold", 15)).pack()
    
    # Set username label
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack(padx = 30,side= TOP, anchor="w")

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack(padx = 30, pady = 5,fill = "both")

    # Set password label
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack(padx = 30,side= TOP, anchor="w")
        
    # Set password entry
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack(padx = 30, pady = 5,fill = "both")

    # Set roles label
    roles_lable = Label(register_screen, text="Select New User Role(s) * ")
    roles_lable.pack(padx = 30,side= TOP, anchor="w")

    # for scrolling vertically in list of roles
    yscrollbar = Scrollbar(register_screen)
    yscrollbar.pack(side = RIGHT, fill = Y)

    #List of possible user roles
    roles_list = Listbox(register_screen, selectmode = "multiple", yscrollcommand = yscrollbar.set)

    # Expands horizontally and vertically by assigning both to fill option
    roles_list.pack(padx = 30, pady = 5,
            expand = YES, fill = "both")
    
    roles = access_control_policy.getAllRoles()

    #Add all roles retrieved from access control policy to available roles for a user
    for each_item in range(len(roles)):
        roles_list.insert(END, roles[each_item])
        roles_list.itemconfig(each_item)
    
    # Attach listbox to vertical scrollbar
    yscrollbar.config(command = roles_list.yview)

    # Set register button
    Button(register_screen, text="Register", width=20, height=1, command=lambda : register_new_user(username.get(), password.get(), getSelecteduserRoles(roles_list),register_screen)).pack(padx = 30, pady = 5,fill = "both")
    main_screen.eval(f'tk::PlaceWindow {str(register_screen)} center')

def getSelecteduserRoles(roles_list):
    selected_user_roles = []
    for i in roles_list.curselection():
        selected_user_roles.append(roles_list.get(i))
    return selected_user_roles

def login():
    login_screen = Toplevel(main_screen) 
    login_screen.title("Finvest Holdings - User Login")
    login_screen.geometry("500x500")
 
    # Set text variables
    username = StringVar()
    password = StringVar()
    
    # Set label for user's instruction
    Label(login_screen, text="Please login with your credentials below").pack()
    
    # Set username label
    username_lable = Label(login_screen, text="Username * ")
    username_lable.pack(padx = 30,side= TOP, anchor="w")

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    username_entry = Entry(login_screen, textvariable=username)
    username_entry.pack(padx = 30, pady = 5,fill = "both")

    # Set password label
    password_lable = Label(login_screen, text="Password * ")
    password_lable.pack(padx = 30,side= TOP, anchor="w")
        
    # Set password entry
    password_entry = Entry(login_screen, textvariable=password, show='*')
    password_entry.pack(padx = 30, pady = 5,fill = "both")
        
    Label(login_screen, text="").pack()
        
    # Set login button
    Button(login_screen, text="Login", width=10, height=1, command= lambda : login_user(username.get(),password.get(),login_screen)).pack(padx = 30, pady = 5,fill = "both")
    main_screen.eval(f'tk::PlaceWindow {str(login_screen)} center')

def access_control(username):
    user_access_screen = Toplevel(main_screen) 
    user_access_screen.title("Finvest Holdings - User Access")
    user_access_screen.geometry("500x500")
    Label(user_access_screen, text="Welcome, {}".format(username), font=("Calibri bold", 15)).pack()

    #Retrieve user role(s)
    user_roles = access_control_policy.getRoles(username)

    #Retrieve corresponding permissions for those roles

    user_permissions = access_control_policy.getPermissions(user_roles)

    #Retrieve user information, roles, permissions and display to user.
    Label(user_access_screen, text="Account Privileges:", font=("Calibri", 15)).pack()
    text=Text(user_access_screen, width=80, height=15)
    text.pack()

    # Iterate over each item in the list
    for perms in user_permissions:
        text.insert(END, perms + '\n')

    main_screen.eval(f'tk::PlaceWindow {str(user_access_screen)} center')
 

def register_new_user(username, password, userRoles, register_screen):
    if not username:
        messagebox.showwarning('Register', 'Username field is empty.')
    elif not password:
        messagebox.showwarning('Register', 'Password field is empty.')
    elif len(userRoles) == 0:
        messagebox.showwarning('Register', 'No roles selected. Please select at least one user role.')
    else:
        isSuccess, message = user.addUser(username,password,userRoles)
        #User successfully added
        if isSuccess:
            messagebox.showinfo('Register', message)
            register_screen.destroy()
            login()
        #User unsuccessfully added   
        else:
            messagebox.showwarning('Register', message)

def login_user(username, pword, login_screen):
    message = ""
    if not username:
        messagebox.showwarning('Login', 'Username field is empty.')
    elif not pword:
        messagebox.showwarning('Login', 'Password field is empty.')
    else:
        isSuccess, message = password.verifyCredentials(username,pword)
        #User successfully added
        if isSuccess:
            messagebox.showinfo('Login', message)
            login_screen.destroy()
            access_control(username)
        #User unsuccessfully added   
        else:
            messagebox.showwarning('Login', message)\

main_account_screen()
