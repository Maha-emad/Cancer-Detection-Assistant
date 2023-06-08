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




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\figmas\build\build\assets\login_imgs")


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

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    768.0,
    395.0,
    image=image_image_1
)


dr_id_var = IntVar()
dr_id_var.set("")
#entry_image_1
id_entry_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
#entry_bg_1
id_entry_bg = canvas.create_image(
    757.0,
    349.0,
    image=id_entry_image
)


# entry_1
id_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable=dr_id_var
)

# entry_1
id_entry.place(
    x=603.0,
    y=325.0,
    width=308.0,
    height=46.0
)


dr_pass_var = StringVar()
# entry_image_2
pass_entry_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
#entry_bg_2
pass_entry_bg = canvas.create_image(
    757.0,
    466.0,
    image=pass_entry_image
)
# entry_2
pass_entry= Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show='*',
    textvariable=dr_pass_var
)
pass_entry.place(
    x=604.0,
    y=441.0,
    width=306.0,
    height=48.0
)

# button_image_1
login_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
# button_1
login_button = Button(
    image=login_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: login_and_open_file(),
    relief="flat"
)
login_button.place(
    x=651.0,
    y=512.0,
    width=184.0,
    height=74.0
)


def login_and_open_file():
    
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Retrieve document from 'doctores' collection
    doc_ref = db.collection('doctors').where('id', '==', dr_id_var.get()).where('password', '==', dr_pass_var.get()).limit(1).stream()
    documents = [doc for doc in doc_ref]
    
    if documents:
        doc = documents[0] 
        role = doc.get('dr') 
        if role == 0 :  
            script_path = r"admin.py"
            subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            window.destroy()
            
        else :
            script_path = r"home.py"
            subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            window.destroy()
  
    else:
        print("Wrong doctor password or ID")
        no_p_lbl = Label(text="Wrong doctor password or ID!", fg="white", font=("Arial", 12, "bold"), bg='red')
        no_p_lbl.place(x=651, y=630)




window.resizable(True, True)
window.mainloop()
