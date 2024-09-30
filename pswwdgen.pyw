import tkinter as tk
import random
import pickle
import os
import string
from tkinter import messagebox
import pyperclip
import csv

FILE_PATH = os.getcwd()  # Obtains the current directory of the file


class Myapp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlackFly Toolkit")
        #self.geometry("300x300")

        # Creating screens
        self.homescreen = Home(self)
        self.genscreen = Generate(self)
        self.viewscreen = View(self)
        self.id = Identity(self)


        self.switch_screen(self.homescreen)  # Switch to home screen first

    def switch_screen(self, frame):
        frame.tkraise()  # Bring the frame to the top


class Home(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')  # Initializing the class as a frame
        self.grid(row=0, column=0, sticky="nsew")

        # Adding widgets to the frame
        heading = tk.Label(self, text="Privacy Guard", font=("Helvetica", 25),bg="black", fg="green")
        heading.grid(row=0,column=0,columnspan=2,padx=140,pady=10)

        # Generate button
        pgen_bt = tk.Button(self, text='Generate Password', font=("Helvetica", 18),bg="black", fg="red",borderwidth=0,
                            command=lambda: parent.switch_screen(parent.genscreen))
        pgen_bt.grid(row=1,column=0,columnspan=2,padx=60,pady=40)

        # View button
        pviw_bt = tk.Button(self, text='My Passwords', font=("Helvetica", 18),bg="black", fg="red",borderwidth=0, #highlightthickness=0,
                            command=lambda: parent.switch_screen(parent.viewscreen))
        pviw_bt.grid(row=2,column=0,columnspan=2,padx=10,pady=40)

        # Identity button
        idviw_bt = tk.Button(self, text='My Fake Identity', font=("Helvetica", 18),bg="black", fg="red",borderwidth=0,
                             command=lambda: parent.switch_screen(parent.id))
        idviw_bt.grid(row=3,column=0,columnspan=2,padx=10,pady=40)

        cprt = tk.Label(self,text='     © Blackfly Toolkit', font=('Helvetica', 8),bg="black", fg="green")
        cprt.grid(row=4,pady=40,padx=140,sticky='s')


class Generate(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent,bg='black')
        self.grid(row=0, column=0, sticky="nsew")
        # Adding widgets to the frame
        label = tk.Label(self, text="Generate Password", font=('Helvetica', 22),bg="black", fg="green")
        label.grid(row=1,column=0,columnspan=2,padx=100,pady=40)

        label1 = tk.Label(self, text="Account Name", font=('Helvetica', 18),bg="black", fg="green")
        label1.grid(row=2,column=0,pady=50)

        self.acc_name = tk.Entry(self,bg="#1C1C1C", fg="white", insertbackground="green")
        self.acc_name.grid(row=2,column=1,columnspan=2,pady=10)

        self.gen_btn = tk.Button(self, text='Generate', font=('Helvetica', 16),bg="black", fg="red",borderwidth=0, command=self.genrte)
        self.gen_btn.grid(row=3,column=0,columnspan=2,padx=10,pady=60)

        bck_btn = tk.Button(self,text='< Back',font=('Helvetica', 10),bg="black", fg="red",borderwidth=0,
                            command= lambda: parent.switch_screen(parent.homescreen))
        bck_btn.grid(row=1,column=0,pady=0,padx=0,sticky='nw')


    def genrte(self):
        # Loading data file
        with open(FILE_PATH + '/psswd.p', 'rb') as p_file:
            self.data = pickle.load(p_file)
        acc_deails = self.acc_name.get()  # Read the account name
        characters = string.ascii_letters + string.digits + string.punctuation
        lent = 16
        password = ''.join(random.choice(characters) for _ in range(lent))
        pyperclip.copy(password)  # Copying the password to clipboard
        messagebox.showinfo('Password Generated', 'The Password has been copied to your clipboard!')


        self.data[1][acc_deails] = password
        with open(FILE_PATH + 'psswd.p', 'wb') as fp:
            pickle.dump(self.data, fp, protocol=pickle.HIGHEST_PROTOCOL)

class View(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black')
        self.grid(row=0,column=0,sticky='nsew')

        # Adding widgets to the frame
        label = tk.Label(self, text="Search Account", font=('Helvetica', 22),bg="black", fg="green")
        label.grid(row=1,column=0,columnspan=2,padx=140,pady=40)

        label1 = tk.Label(self, text="Account Name", font=('Helvetica', 18),bg="black", fg="green")
        label1.grid(row=2,column=0,pady=50)

        self.acc_name = tk.Entry(self,bg="#1C1C1C", fg="white", insertbackground="green")
        self.acc_name.grid(row=2,column=1,columnspan=2,pady=10)

        self.gen_btn = tk.Button(self, text='Search', font=('Helvetica', 14),bg="black", fg="red",borderwidth=0, command=self.search)
        self.gen_btn.grid(row=3,column=0,columnspan=2,padx=10,pady=50)

        bck_btn = tk.Button(self,text='< Back',font=('Helvetica', 10),bg="black", fg="red",borderwidth=0,
                            command= lambda: parent.switch_screen(parent.homescreen))
        bck_btn.grid(row=1,column=0,pady=0,padx=0,sticky='nw')


    def search(self):
        # Loading data file
        with open(FILE_PATH + '/psswd.p', 'rb') as p_file:
            self.data = pickle.load(p_file)
        acc_deails = self.acc_name.get()  # Read the account name
        if acc_deails in self.data[1]:
            pyperclip.copy(self.data[1][acc_deails])  # Copying the password to clipboard
            messagebox.showinfo('Account Found', 'The Password has been copied to your clipboard!')
        else:
            messagebox.showinfo('Account Not Found!','Please re-check the details & try again.')
            
class Identity(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black')
        self.grid(row=0,column=0,sticky='nsew')

        with open(FILE_PATH+'/psswd.p','rb') as file:
            self.data = pickle.load(file)

        # Adding widgets to the frame
        bck_btn = tk.Button(self,text='< Back',font=('Helvetica', 10),bg="black", fg="red",borderwidth=0,
                            command= lambda: parent.switch_screen(parent.homescreen))
        bck_btn.grid(row=1,column=0,pady=0,padx=0,sticky='nw')


        label = tk.Label(self, text="Current Fake Identity", font=('Helvetica', 22),bg="black", fg="green")
        label.grid(row=1,column=0,columnspan=2,padx=100,pady=30)

        self.name = tk.Label(self, text=f"Name - {self.data[0]['ï»¿GivenName']} {self.data[0]['MiddleInitial']} {self.data[0]['Surname']}", 
                        font=('Helvetica', 12),bg="black", fg="green")
        self.name.grid(row=2,column=0,columnspan=2,sticky='w',padx=120)

        self.gender = tk.Label(self, text=f"Gender - {self.data[0]['Gender']}", font=('Helvetica', 12),bg="black", fg="green")
        self.gender.grid(row=3,column=0,columnspan=2,sticky='w',padx=120)

        self.address = tk.Label(self, text=f"Address - {self.data[0]['StreetAddress']}\n{self.data[0]['StateFull']}, {self.data[0]['ZipCode']}, {self.data[0]['CountryFull']}", 
                           font=('Helvetica', 12),bg="black", fg="green")
        self.address.grid(row=4,column=0,columnspan=2,sticky='w',padx=120)

        self.dob = tk.Label(self, text=f"D.O.B - {self.data[0]['Birthday']}", font=('Helvetica', 12),bg="black", fg="green")
        self.dob.grid(row=5,column=0,columnspan=2,sticky='w',padx=120)

        self.m_maiden = tk.Label(self, text=f"Mother's Maiden Name - {self.data[0]['MothersMaiden']}", font=('Helvetica', 12),bg="black", fg="green")
        self.m_maiden.grid(row=6,column=0,columnspan=2,sticky='w',padx=120)

        self.age = tk.Label(self, text=f"Age - {self.data[0]['Age']}", font=('Helvetica', 12),bg="black", fg="green")
        self.age.grid(row=7,column=0,columnspan=2,sticky='w',padx=120)

        self.bloodtype = tk.Label(self, text=f"Blood Type - {self.data[0]['BloodType']}", font=('Helvetica', 12),bg="black", fg="green")
        self.bloodtype.grid(row=8,column=0,columnspan=2,sticky='w',padx=120)

        self.weight = tk.Label(self, text=f"Weight - {self.data[0]['Kilograms']} Kg", font=('Helvetica', 12),bg="black", fg="green")
        self.weight.grid(row=9,column=0,columnspan=2,sticky='w',padx=120)

        self.height = tk.Label(self, text=f"Height - {self.data[0]['Centimeters']} cm", font=('Helvetica', 12),bg="black", fg="green")
        self.height.grid(row=10,column=0,columnspan=2,sticky='w',padx=120)
        

        new_id = tk.Button(self,text='Generate New Identity',font=('Helvetica', 12),bg="black", fg="red",borderwidth=0,
                            command= self.newid)
        new_id.grid(row=11,column=0,columnspan=2,pady=50,padx=20)

        cprt = tk.Label(self,text='      http://www.fakenamegenerator.com/license.php', font=('Helvetica', 8),bg="black", fg="green")
        cprt.grid(row=12,pady=10,padx=60,sticky='s')

        cprt = tk.Label(self,text='    © Blackfly Toolkit', font=('Helvetica', 8),bg="black", fg="green")
        cprt.grid(row=13,pady=10,padx=160,sticky='s')

    def newid(self):
        data_list = []
    
        # Reading the CSV file
        with open('Fake-list.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_list.append(row)

        # Select a random row
        self.data[0] = random.choice(data_list)
        #print(self.data[0])

        # Update labels with new identity
        self.name.config(text=f"Name - {self.data[0]['ï»¿GivenName']} {self.data[0]['MiddleInitial']} {self.data[0]['Surname']}")
        self.gender.config(text=f"Gender - {self.data[0]['Gender']}")
        self.address.config(text=f"Address - {self.data[0]['StreetAddress']}\n{self.data[0]['StateFull']}\n{self.data[0]['ZipCode']}\n{self.data[0]['CountryFull']}")
        self.dob.config(text=f"D.O.B - {self.data[0]['Birthday']}")
        self.m_maiden.config(text=f"Mother's Maiden Name - {self.data[0]['MothersMaiden']}")
        self.age.config(text=f"Age - {self.data[0]['Age']}")
        self.bloodtype.config(text=f"Blood Type - {self.data[0]['BloodType']}")
        self.weight.config(text=f"Weight - {self.data[0]['Kilograms']}")
        self.height.config(text=f"Height - {self.data[0]['Centimeters']}")

        #updating data file
        with open(FILE_PATH + '/psswd.p', 'wb') as fp:
            pickle.dump(self.data, fp, protocol=pickle.HIGHEST_PROTOCOL)

        messagebox.showinfo('Identity Updated!','Your new fake identity have been generated.')


if __name__ == '__main__':
    app = Myapp()
    app.mainloop()
