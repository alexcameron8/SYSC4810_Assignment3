from tkinter import *

main_screen = Tk()   # create a GUI window 

def main_account_screen():

    main_screen.geometry("1000x1000") # set the configuration of GUI window 
    main_screen.title("Account Login") # Title of Interface
    
    # create a Form label 
    Label(text="SYSC4810 - Assignment 3\nLogin Or Register", bg="grey", width="300", height="2", font=("Calibri", 25)).pack() 
    Label(text="").pack() 
    
    # create Login Button 
    Button(text="Login",font=("Calibri", 20), height="10", width="100", command=login).pack() 
    Label(text="").pack() 
    
    # create a register button
    Button(text="Register",font=("Calibri", 20), height="10", width="100", command=register).pack()

    #main_screen.eval('tk::PlaceWindow . center') Center window upon opening
    main_screen.mainloop() # start the GUI

def register():

    register_screen = Toplevel(main_screen) 
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    # Set text variables
    username = StringVar()
    password = StringVar()
    
    # Set label for user's instruction
    Label(register_screen, text="Please register below", bg="grey").pack()
    Label(register_screen, text="").pack()
    
    # Set username label
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    # Set password label
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
        
    # Set password entry
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
        
    Label(register_screen, text="").pack()
        
    # Set register button
    Button(register_screen, text="Register", width=10, height=1, bg="grey").pack()
    main_screen.eval(f'tk::PlaceWindow {str(register_screen)} center')


def login():
    login_screen = Toplevel(main_screen) 
    login_screen.title("Login")
    login_screen.geometry("300x250")
 
    # Set text variables
    username = StringVar()
    password = StringVar()
    
    # Set label for user's instruction
    Label(login_screen, text="Please login with your credentials below", bg="grey").pack()
    Label(login_screen, text="").pack()
    
    # Set username label
    username_lable = Label(login_screen, text="Username * ")
    username_lable.pack()

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    username_entry = Entry(login_screen, textvariable=username)
    username_entry.pack()

    # Set password label
    password_lable = Label(login_screen, text="Password * ")
    password_lable.pack()
        
    # Set password entry
    password_entry = Entry(login_screen, textvariable=password, show='*')
    password_entry.pack()
        
    Label(login_screen, text="").pack()
        
    # Set login button
    Button(login_screen, text="Login", width=10, height=1, bg="grey").pack()
    main_screen.eval(f'tk::PlaceWindow {str(login_screen)} center')

main_account_screen() # call the main_account_screen() function