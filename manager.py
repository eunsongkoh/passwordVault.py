from tkinter import * 
from tkinter import simpledialog
from functools import partial 
import os 
import sqlite3, hashlib

# -------- checking what files are present ------------- 
cwd = os.getcwd()
print(cwd)

files = os.listdir(cwd)
print(files)


# --------------- databases and passwords----------
# initilizing database
with sqlite3.connect("passwordManage.db") as db:
    cursor = db.cursor()

# creating a table in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
''')


# creating a table to save the database for the vault 
cursor.execute('''
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL, 
password TEXT NOT NULL);
''')



# hashing the password 
def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash


# --------------- UI ------------------------
# welcome page 
class login(Tk):
    def __init__(self):
        super().__init__()   
        
        self.geometry("800x600")
        self.title("login")
        self.configure(background='#CC99FF')

        Label(self, text="enter master password").place(x=250, y=300)

        self.loginPass = Entry(width = 20, show="*")
        self.loginPass.place(x=400, y=300)
        
        Button(self, text="submit", command=self.confirm).place(x=350, y=400)
    
    def getMasterPassword(self): 
            # takes the password the user enters 
            checkHashedPassword = hashPassword(self.loginPass.get().encode('utf-8'))
            # checks for a match 
            cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
            print(checkHashedPassword)
            return cursor.fetchall()
    
    def confirm(self):
        match = login.getMasterPassword(self) 
        print(match)
        if match:
            window = MainMenu(self)
            window.grab_set()
        else: 
            Label(self, text="wrong password, please try again!").place(x=375, y=500)


# Main Menu 
class MainMenu(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # display config
        self.geometry("800x600")
        self.title("main menu")
        self.configure(background='#CC99FF')

        addpass = Button(self, text="add a password", command=self.open_Add).place(x=475, y=400)
        viewpass = Button(self, text="view passwords", command=self.open_View).place(x=200, y=400)

    # opens the "add password" window
    def open_Add(self):
        window = Password(self)
        window.grab_set()
    
    # opens the "view password" window 
    def open_View(self):
        window = viewPass(self)
        window.grab_set()

"""
For later implementations 
# change master password
class masterPass(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # display config 
        self.geometry("800x600")
        self.title("main menu")

        back = Button(self, text="main menu", command=self.destroy).grid(padx=20, pady=30)

        Label(self, text="what is your current master password?").place(x=250, y=400)
        self.newPass = Entry(width = 20)
        self.newPass.place(x=400, y=300)

        Button(self, text="submit", command=self.confirm).place(x=350, y=400)
    
    # confims for right password 
    def confirm(self):
        password = self.newPass.get()
        if str(password) == self.newPass.get():
            window = changeMaster(self)
            window.grab_set()
        else: 
            Label(self, text="this is incorrect").place(x=375, y=500)
"""
# change master password with correct input 
class changeMaster(Tk):
    def __init__(self):
        super().__init__()

        # display config 
        self.geometry("800x600")
        self.title("change master password")
        self.configure(background='#CC99FF')
       
        # main menu button 
        back = Button(self, text="exit", command=self.destroy).grid(padx=20, pady=30)

        # enter new password 
        Label(self, text="enter new password").place(x=250, y=300)
        self.newPass = Entry(width = 20)
        self.newPass.place(x=400, y=300)

        # re-enter password 
        Label(self, text="re-enter password").place(x=250, y=400)
        self.enter = Entry(width = 20)
        self.enter.place(x=400, y=400)
        
        # submit password 
        Button(self, text="submit", command=self.confirm).place(x=350, y=500)
    
    def confirm(self):
        # if the passwords match 
        if self.newPass.get() == self.enter.get():
            # new password is set to hashedPassword and hashes
            hashedPassword = hashPassword(self.newPass.get().encode('utf-8'))

            # inserts the new password into the database 
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""

            # 
            cursor.execute(insert_password, [(hashedPassword)])
           
            # saves into database
            db.commit()

            # switch to the viewpassword window 
            window = viewPass(self)
            window.grab_set()
        else:
            Label(self, text="passwords do not match").place(x=375, y=500)
    def changeWindow(self):
        window = login(self)
        window.grab_set()

# view password window  
class viewPass(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # display config
        self.geometry("800x600")
        self.title("view password")
        self.configure(background='#CC99FF')

        # main menu button 
        back = Button(self, text="main menu", command=self.destroy).grid(padx=20, pady=30)

        # columns 
        web = Label(self, text="website")
        web.grid(row=2, column=0, padx=88)
        user = Label(self, text="username")
        user.grid(row=2, column=1, padx=88)
        passw = Label(self, text="password")
        passw.grid(row=2, column=2, padx=88)
        
        cursor.execute("SELECT * FROM vault ")
        print(cursor.fetchall()) 

        # accesses the db 
        cursor.execute("SELECT * FROM vault ")
        array = cursor.fetchall()

        if (cursor.fetchall() != None):
            i = 0
            while True: 
                # if the length of the array is equal to zero 
                if (len(array) == 0):
                    break
                
                lbl = Label(self, text=(array[i][1]), font=("Helvetica", 12))
                lbl.grid(column=0, row=i+3)
                lbl = Label(self, text=(array[i][2]), font=("Helvetica", 12))
                lbl.grid(column=1, row=i+3)
                lbl = Label(self, text=(array[i][3]), font=("Helvetica", 12))
                lbl.grid(column=2, row=i+3)

                # delete button 
                delete = Button(self, text="delete", command=partial(viewPass.remove, array[i][0]))
                delete.grid(column=3, row=i+3, pady=10)

                i = i+1

                cursor.execute("SELECT * FROM vault ")
                
                # stops running after all entries 
                if (len(cursor.fetchall()) <= i):
                    break
                

        # refreshses the toplevel? 
        #self.Toplevel.update()
    
    def remove(self, input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        #Toplevel.update(self)
    

# ADD a password
class Password(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # displays config
        self.geometry("900x600")
        self.title("add password")
        self.configure(background='#CC99FF')
        
        # main menu button 
        back = Button(self, text="main menu", command=self.destroy).grid(padx=20, pady=30,)
        
        # grabs the website from the user
        website= Label(self, text="website: ").place(x=100, y=200)
        self.websiteEntry = Entry(self, width=25)
        self.websiteEntry.place(x=150, y=200)
        #Button(self, text="confirm website", command=self.insert).place(x=175, y=250)

       
        # grabs the username from the user
        username = Label(self, text="username: ").place(x=315, y=200)
        self.usernameEntry = Entry(self, width=25)
        self.usernameEntry.place(x=375, y=200)
        #Button(self, text="confirm user", command=self.insert).grid(row = 3, column=2, sticky=NW, pady=4, padx=80)
        
        # grabs the password from the user 
        password = Label(self, text="password: ").place(x=540, y=200)
        self.passwordEntry = Entry(self, width=25)
        self.passwordEntry.place(x=600, y=200)
        #Button(self, text="confirm pass", command=self.insert).grid(row=3, column=3)
        
        # submit 
        submit = Button(self, text="submit", command=self.insert).place(x=800, y=200)

        viewPass = Button(self, text="view passwords", width=20, command=self.switch).place(x=350, y=400)
    

    def insert(self):
        global websiteGrab, usernameEntry, passwordGrab
        websiteGrab = self.websiteEntry.get()
        usernameEntry = self.websiteEntry.get()
        passwordGrab = self.passwordEntry.get()

        # inserting the value into the data base 
        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?, ?, ?)"""
        cursor.execute(insert_fields, (websiteGrab, usernameEntry, passwordGrab))
        
        # adds the information to the database 
        db.commit()
    
    def switch(self):
        window = viewPass(self)
        window.grab_set()



if __name__ == "__main__":
    check = cursor.execute("SELECT * FROM masterpassword")
    # if there is already a present password 
    if check.fetchall(): 
        app = login()
    else: 
        app = changeMaster()

app.mainloop()
    
