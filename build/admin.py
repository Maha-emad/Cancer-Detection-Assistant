import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
import os 
import sys
import subprocess


from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk




cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client() 
    



OUTPUT_PATH = Path('<output_path>')
ASSETS_PATH = Path(r"C:\Users\user\Desktop\figmas\build\build\assets\admin_imgs")

def logout() : 
    script_path = r"login.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def populate_treeview():
    # Clear existing items in the Treeview
    tree.delete(*tree.get_children())

    # Fetch updated data from Firestore
    doctors_ref = db.collection('doctors').order_by('id', direction=firestore.Query.ASCENDING)
    doctors_data = doctors_ref.get()

    # Populate the Treeview with the updated data
    for doctor in doctors_data:
        doc_data = doctor.to_dict()
        tree.insert("", "end", values=(doc_data["id"], doc_data["username"]))


def delete_selected_row():
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, "values")
        id_value = int(values[0])

        # Delete the selected doctor from Firestore
        doctor_ref = db.collection('doctors').where('id', '==', id_value)
        for doc in doctor_ref.stream():
            doc.reference.delete()

        # Update the IDs of doctors higher than the deleted one
        doctors_ref = db.collection('doctors').where('id', '>', id_value)
        for doc in doctors_ref.stream():
            doc.reference.update({'id': doc.get('id') - 1})

        # Delete the selected item from the Treeview
        tree.delete(selected_item)

        canvas.itemconfig(message_label_1, text="")
        canvas.itemconfig(message_label_1, text="Doctor deleted")

        # Repopulate the Treeview with updated data
        populate_treeview()





            
def save_data():
    entry1_value = entry_1.get()
    entry2_value = entry_2.get()

  

    cred = credentials.Certificate(r'E:\College resources\GraduationProject\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-00ab4ef02d.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    doctors_ref = db.collection('doctors')
    query = doctors_ref.where('username', '==', entry1_value).limit(1)
    doctors = query.get()

    canvas.itemconfig(message_label_1, text="")
    canvas.itemconfig(message_label_2, text="")
    if not entry1_value or not entry2_value:
        canvas.itemconfig(message_label_1, text="Please complete the data")
        return
    if len(doctors) > 0:
        canvas.itemconfig(message_label_1, text="User already exists")

    elif len(entry2_value) < 6 or not re.search(r"\d", entry2_value) or not re.search(r"[a-zA-Z]", entry2_value):
            canvas.itemconfig(message_label_2, text="Password should be at least 6 characters long and contain a mix of letters and numbers")
            return
    else:
        entry3_value = entry_3.get()
        canvas.itemconfig(message_label_1, text="Doctor added successfully")
        if entry2_value == entry3_value:
            max_dr = db.collection('doctors').order_by('id', direction=firestore.Query.DESCENDING).limit(1).get()

            new_dr = 1

            if max_dr:
                for doc in max_dr:
                    new_dr = doc.get('id') + 1

            data = {
                'username': entry1_value,
                'password': entry2_value,
                'id': new_dr,
                'dr': 1
            }
            db.collection('doctors').add(data)

            tree.insert("", "end", values=(new_dr, entry1_value))
        else:
            canvas.itemconfig(message_label_1, text="Password is not identical")


window = Tk()

window.geometry("1530x790")
window.configure(bg="#051747")

canvas = Canvas(
    window,
    bg="#051747",
    height=790,
    width=1530,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    765.0,
    395.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    470.0,
    245.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=316.0,
    y=221.0,
    width=308.0,
    height=46.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    470.0,
    328.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=317.0,
    y=303.0,
    width=306.0,
    height=48.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    470.0,
    407.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_3.place(
    x=317.0,
    y=382.0,
    width=306.0,
    height=48.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: logout(),
    relief="flat"
)
button_3.place(
    x=1329.0,
    y=41.0,
    width=140.0,
    height=48.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=save_data,
    relief="flat"
)
button_1.place(
    x=200.0,
    y=455.0,
    width=246.0,
    height=63.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=delete_selected_row,  
    relief="flat"
)
button_2.place(
    x=1250.0,
    y=130.0,
    width=246.0,
    height=63.0
)
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1098.0,
   481.0,
    image=image_image_2
)

message_label_1 = canvas.create_text(
    250.0,  
    600.0,
    anchor="w",
    text="",
    fill="#FFFFFF",
    font=("Arial", 14)
)

message_label_2 = canvas.create_text(
    100.0,  
    600.0,
    anchor="w",
    text="",
    fill="#FFFFFF",
    font=("Arial", 10)
)


tree = ttk.Treeview(window, columns=("id", "Username"), show="headings")
tree.place(x=690, y=198, width=810, height=567)

tree.heading("id", text="id")
tree.heading("Username", text="Username")


doctors_ref = db.collection('doctors').order_by('id', direction=firestore.Query.ASCENDING)
doctors_data = doctors_ref.get()


for doctor in doctors_data:
    doc_data = doctor.to_dict()
    tree.insert("", "end", values=(doc_data["id"], doc_data["username"]))

window.resizable(True, True)
window.mainloop()
