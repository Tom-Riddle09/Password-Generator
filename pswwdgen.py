import tkinter as tk
import random
import pickle
import os

FILE_PATH = os.getcwd()#Obtains the current directory of the file

#===PASSWORD GENERATOR FOR BLACKFLY TOOLKIT===
def ex():
    window.destroy()#destroy the window upon exit

    
def pswdgen():
    def savpswd(): #function for generating and saving new passwords
        accname = entry.get()#read the acc name
        instrct.destroy()
        btn.destroy()
        entry.destroy()
        lwr = 'abcdefghijklmnopqrstuvwxyz'
        uppr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        num = '1234567890'
        symbl  = '[]{}()+;/,_-.!@#$%^&'
        all = lwr + uppr + num + symbl
        lent = 16
        passwrd = "".join(random.sample(all,lent))
        lbl_show = tk.Label(master=frame,text="Generated Password [copy the text]",fg="white",bg="#808080")
        lbl_show.place(x=20,y=20)
        ent_pswd= tk.Entry(master=frame,fg="black",bg="white",width=20)
        ent_pswd.insert(0,passwrd) #displays the generated password
        ent_pswd.place(x=10,y=40)
        op=open(FILE_PATH+'\\psswd.p', 'rb')
        dct=pickle.load(op)
        op.close()
        dct={}
        dct[accname] = passwrd
        with open(FILE_PATH+'\\psswd.p', 'wb') as fp: 
            pickle.dump(dct, fp, protocol=pickle.HIGHEST_PROTOCOL)
        lbl_instruct= tk.Label(master=frame,text="Password Saved Successfully",fg="white",bg="#808080")
        lbl_instruct.place(x=30,y=70)
        btn_exit = tk.Button(master=frame,relief=tk.RAISED,command=ex,
        text="Done",
        bg="black",
        fg="white")
        btn_exit.place(x=150,y=40)

    btn1.destroy()
    btn2.destroy()
    instrct = tk.Label(master=frame,text="Enter the account name:",fg="white",bg="#808080")
    instrct.place(x=20,y=20)
    entry= tk.Entry(master=frame,textvariable="Account Name",fg="black",bg="white",width=20)#prompt for account name
    entry.place(x=10,y=40)
    btn = tk.Button(master=frame,relief=tk.RAISED,command=savpswd,
    text="Done",
    bg="black",
    fg="white")
    btn.place(x=150,y=40)
    
def paswdview():
    def retrive():
        accname = entry.get()#read the acc name
        instrct.destroy()
        btn.destroy()
        entry.destroy()
        dct1={}
        with open(FILE_PATH+'\\psswd.p', 'rb') as fp:
            dct1=pickle.load(fp)
            try:
                lbl_show = tk.Label(master=frame,text=("Password for Acc:",accname),fg="white",bg="#808080")
                lbl_show.place(x=20,y=20)
                ent_pswd= tk.Entry(master=frame,fg="black",bg="white",width=20)
                ent_pswd.insert(0,dct1[accname]) #displays the generated password
                ent_pswd.place(x=10,y=40)
                btn_exit = tk.Button(master=frame,relief=tk.RAISED,command=ex,
                text="Exit",
                bg="black",
                fg="white")
                btn_exit.place(x=150,y=40)
            except KeyError as kd:
                lbl_show = tk.Label(master=frame,text=("Password not found for :",accname),fg="white",bg="#808080")
                lbl_show.place(x=20,y=20)
                btn_exit = tk.Button(master=frame,relief=tk.RAISED,command=ex,
                text="Exit",
                bg="black",
                fg="white")
                btn_exit.place(x=100,y=40)
        
        
    btn1.destroy()
    btn2.destroy()
    instrct = tk.Label(master=frame,text="Enter the account name:",fg="white",bg="#808080")
    instrct.place(x=20,y=20)
    entry= tk.Entry(master=frame,textvariable="Account Name",fg="black",bg="white",width=20)#prompt for account name
    entry.place(x=10,y=40)
    btn = tk.Button(master=frame,relief=tk.RAISED,command=retrive,
    text="Done",
    bg="black",
    fg="white")
    btn.place(x=150,y=40)



#--Main code---
window = tk.Tk()
window.title("Blackfly Toolkit")
frame = tk.Frame(master=window,relief=tk.RAISED,borderwidth=5,width=270,height=150,bg="#808080")
frame.pack()
gretng = tk.Label(master=frame,relief=tk.SUNKEN,text="Password Generator & Retriever",fg="black",bg="white")
gretng.place(x=40,y=0)
btn1 = tk.Button(master=frame,relief=tk.RAISED,command=pswdgen,
    text="Password Generator",
    bg="black",
    fg="white")
btn2 = tk.Button(master=frame,relief=tk.RAISED,command=paswdview,
    text="Password Retriever",
    bg="black",
    fg="white")
btn1.place(x=9,y=75)
btn2.place(x=130,y=75)
window.mainloop()


