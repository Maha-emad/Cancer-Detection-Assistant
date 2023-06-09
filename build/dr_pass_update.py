from pathlib import Path
from tkinter import *
# Explicit imports to satisfy Flake8
from PIL import Image,ImageTk
import os 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import subprocess
from tkinter import filedialog 
import functools 
import json
from roboflow import Roboflow 
from PIL import ImageTk, Image, ImageDraw, ImageFont
import torch 
import time
import re

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\figmas\build\build\assets\dr_setting_imgs")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1530x790")
window.configure(bg = "#051747")


canvas = Canvas(
    window,
    bg = "#051747",
    height = 790,
    width = 1530,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
# id(x= 555 , y= 173)   old(x = 556 , 269)  nw(x = 556 , y = 367)    cnf(x = 556 , y = 465) 
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    773.0,
    395.0,
    image=image_image_1
)



with open('login_data.json', 'r') as file:
        data = json.load(file)
    
    
dr_id =  data['dr_id']

message_label_1 = canvas.create_text(600.0,200.0 , anchor="w",
    text="",
    fill="#FFFFFF",
    font=("Arial", 20,"bold"),
)



canvas.itemconfig(message_label_1, text=dr_id )


old_pass_var = StringVar()
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    709.0,
    294.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable = old_pass_var
)
entry_2.place(
    x=556.0,
    y=269.0,
    width=306.0,
    height=48.0
)






nw_pass_var = StringVar()

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    709.0,
    490.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable = nw_pass_var
)
entry_3.place(
    x=556.0,
    y=465.0,
    width=306.0,
    height=48.0
)






cnf_pass_var = StringVar()
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    709.0,
    392.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable = cnf_pass_var
)
entry_4.place(
    x=556.0,
    y=367.0,
    width=306.0,
    height=48.0
)


back_button_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
back_button = Button(
    image=back_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:home(),
    relief="flat"
)
back_button.place(
    x=1260.0,
    y=48.0,
    width=140.0,
    height=48.0
)




button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_pass(),
    relief="flat"
)
button_1.place(
    x=621.0,
    y=534.0,
    width=136.0,
    height=80.0
)


message_label_1 = canvas.create_text(
    615.0,  
    625.0,
    anchor="w",
    text="",
    fill="#FFFFFF",
    font=("Arial", 12,"bold"),
)

message_label_2 = canvas.create_text(
    900.0,  
    367.0,
    anchor="w",
    text="",
    fill="#FFFFFF",
    font=("Arial", 12,"bold"),
)




        

def home(): 
    script_path = r"home.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()
def update_pass()  : 
    
    
    
    old_pass = old_pass_var.get()
    nw_pass = nw_pass_var.get()
    conf_pass= cnf_pass_var.get()
    
    canvas.itemconfig(message_label_1, text="")
    canvas.itemconfig(message_label_2, text="")
    
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    # Access Firestore database
    db = firestore.client()
    
    old_pass= old_pass_var.get()
    
    dr_ref = db.collection('doctors')
    
   
    query = dr_ref.where('id', '==', dr_id ).where('password', '==' ,old_pass ).limit(1).get()
    
    documents = [doc for doc in query]
    
    if not dr_id or not old_pass or not nw_pass or not conf_pass:
        #lbl=Label(text = "Please complete the data", fg="white", font=("Arial", 12, "bold"),bg='red' ) 
        canvas.itemconfig(message_label_1, text="Please complete the data")
        #lbl.place(x = 615 , y = 620) 
        return
    
    if len(query) != 0:
            
        if len(nw_pass) < 6 or not re.search(r"\d", nw_pass) or not re.search(r"[a-zA-Z]", nw_pass):
            #lbl=Label(text = "Password should be at least 6 characters long\n and contain a mix of letters and numbers", fg="white", font=                          ("Arial", 12, "bold"),bg='red' ) 
            #lbl.place(x = 900 , y = 367)
            canvas.itemconfig(message_label_2, text="Password should be at least 6 characters long\n and contain a mix of letters and numbers")
            return
        
        else :
            # Check if new_pass matches conf_pass
            if nw_pass == conf_pass:
                # Update the password field of the matching document
                document_ref = documents[0].reference
                document_ref.update({'password': nw_pass})
                #lbl=Label(text = "Password updated", fg="white", font=("Arial", 12, "bold"),bg='red' , height =2, width =20 ) 
                canvas.itemconfig(message_label_1, text="Password updated")
                #lbl.place(x = 615 , y = 620)
            else:
                #lbl=Label(text = "New password and confirmed password not matched", fg="white", font=("Arial", 12, "bold"),bg='red' ) 
                #lbl.place(x = 900 , y = 367) 
                canvas.itemconfig(message_label_2, text="New password and confirmed password not matched")
    else:
        #lbl=Label(text = "No such doctor", fg="white", font=("Arial", 12, "bold"),bg='red' , height =2, width =20 ) 
        #lbl.place(x = 615 , y = 620)
        canvas.itemconfig(message_label_1, text="No such doctor")
    
    
    
    
window.resizable(True, True)
window.mainloop()
