
from tkinter.ttk import Combobox
from pathlib import Path
from datetime import datetime
from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter.ttk import Treeview
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import subprocess
import json
import os 
import sys
import subprocess



OUTPUT_PATH = Path('<output_path')
ASSETS_PATH = Path(r"C:\Users\user\Desktop\figmas\build\build\assets\patients_imgs")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def home() : 
    script_path = r"home.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()

def login() : 
    script_path = r"login.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()


def add_patient():
    name = name_entry.get()
    gender = gender_var.get()
    phone_number = phone_entry.get()
    dob = dob_entry.get()

    # Check if phone number is valid
    if not (phone_number.isdigit() and len(phone_number) == 11 and phone_number.startswith(("010", "011", "012", "015"))):
        canvas.itemconfigure(error_label, text="Invalid phone number")
        return

    try:
        dob_date = datetime.strptime(dob, "%d/%m/%Y")
    except ValueError:
        canvas.itemconfigure(error_label, text="Enter date in dd/mm/yyyy format")
        return

    try:
        dob_date = datetime.strptime(dob, "%d/%m/%Y")
    except ValueError:
        canvas.itemconfigure(error_label, text="Enter date in dd/mm/yyyy format")
        return

    patients_ref = db.collection('patients')
    maxRef = patients_ref.order_by("id").limit_to_last(1).get()
    dataRef = maxRef[0] if len(maxRef) != 0 else 1
    id = dataRef.get('id')
    id = int(id) + 1 

    new_patient_data = {
        'name': name,
        'gender': gender,
        'phone': phone_number,
        'id': id,
        'DOB': dob,
    }
    patients_ref.add(new_patient_data)

    # Update the table with the new patient
    table.insert('', 'end', values=(id, name, gender, dob, phone_number, 0))
    canvas.itemconfigure(error_label, text="")





def delete_patient():
    selection = table.selection()
    if selection:
        patient_id = search_entry.get()
        if patient_id:
            patient_id = int(patient_id)
            
            cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            patients_ref = db.collection('patients')

            query = patients_ref.where('id', '==', patient_id).limit(1).get()

            if len(query):
                # Delete the patient document
                for doc in query:
                    doc.reference.delete()

                # Decrement the IDs of higher patients
                decrement_ref = patients_ref.where('id', '>', patient_id).get()
                for doc in decrement_ref:
                    doc.reference.update({'id': doc.get('id') - 1})

                # Delete associated reports
                reports_ref = db.collection('reports')
                query = reports_ref.where('patient_id', '==', patient_id).get()

                for doc in query:
                    doc_id = doc.id
                    reports_ref.document(doc_id).delete()

                show_all_data()
        else:
            canvas.itemconfigure(error_label, text="Enter patient ID to delete")



def update_patient():
    patient_id = int(search_entry.get())
    
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    patients_ref = db.collection('patients')

    query = patients_ref.where('id', '==', patient_id).limit(1).get()

    if len(query) != 0:
        for doc in query:
            # Retrieve the existing patient data
            data = doc.to_dict()

            # Get the updated values from the entry fields
            name = name_entry.get() if name_entry.get() else data['name']
            gender = gender_var.get() if gender_var.get() else data['gender']
            phone_number = phone_entry.get() if phone_entry.get() else data['phone']
            dob = dob_entry.get() if dob_entry.get() else data['DOB']

            # Create the updated patient data dictionary
            updated_patient_data = {
                'name': name,
                'gender': gender,
                'phone': phone_number,
                'DOB': dob,
            }

            # Update the patient document in Firestore
            key = doc.id
            patients_ref.document(key).update(updated_patient_data)
            
        show_all_data()  # Show all the patients in the table after updating
    else:
        table.delete(*table.get_children())
        table.insert('', 'end', values=("Patient Not Found.", "", ""))


  


    

def search_patient():
    global patient_id
    patient_id = int(search_entry.get())
    
    
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
            
    patients_ref = db.collection('patients')
    query = patients_ref.where('id', '==', patient_id).get()

    if len(query) != 0:
        table.delete(*table.get_children())  # Clear existing table rows

        for doc in query:
            reports_ref = db.collection('reports')
            report_query = reports_ref.where('patient_id', '==', patient_id).get()
            
            data = doc.to_dict()
            table.insert('', 'end', values=(data['id'], data['name'], data['gender'], data['DOB'],                                                                                              data['phone'], len(report_query)))
            
    else:
        table.delete(*table.get_children())
        table.insert('', 'end', values=("Patient Not Found.", "", ""))





def show_report():
    p_id = search_entry.get()
    data = {'patient_id': p_id}

    with open('patient_id.json', 'w') as file:
        json.dump(data, file)
    window.destroy()
    script_path = r"pt_rep.py"
    if os.path.exists(script_path):
        subprocess.Popen(['python', script_path])
    else:
        print("rep file not found!")
        




cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

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
    765.0,
    395.0,
    image=image_image_1
)

name_entry_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
name_entry_bg = canvas.create_image(
    371.0,
    244.5,
    image=name_entry_image
)
name_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
name_entry.place(
    x=254.5,
    y=220.0,
    width=233.0,
    height=47.0
)

search_entry_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
search_entry_bg = canvas.create_image(
    796.0,
    234.5,
    image=search_entry_image
)
search_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
search_entry.place(
    x=679.5,
    y=210.0,
    width=233.0,
    height=47.0
)

phone_entry_image = PhotoImage(
    file=relative_to_assets("entry_3.png"))
phone_entry_bg = canvas.create_image(
    371.0,
    428.5,
    image=phone_entry_image
)
phone_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
phone_entry.place(
    x=254.5,
    y=404.0,
    width=233.0,
    height=47.0
)

dob_entry_image = PhotoImage(
    file=relative_to_assets("entry_4.png"))
dob_entry_bg = canvas.create_image(
    371.0,
    532.5,
    image=dob_entry_image
)
dob_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
dob_entry.place(
    x=254.5,
    y=508.0,
    width=233.0,
    height=47.0
)

gender_entry_image = PhotoImage(
    file=relative_to_assets("entry_5.png"))
gender_entry_bg = canvas.create_image(
    371.0,
    336.5,
    image=gender_entry_image
)
gender_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
gender_entry.place(
    x=254.5,
    y=312.0,
    width=233.0,
    height=47.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: login() ,
    relief="flat"
)
button_1.place(
    x=1278.0,
    y=48.0,
    width=140.0,
    height=48.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: home(),
    relief="flat"
)
button_2.place(
    x=1278.0,
    y=131.0,
    width=140.0,
    height=48.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_patient(),
    relief="flat"
)
button_3.place(
    x=286.0,
    y=657.0,
    width=169.0,
    height=53.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: delete_patient(),
    relief="flat"
)
button_4.place(
    x=796.0,
    y=663.0,
    width=191.0,
    height=53.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_patient(),
    relief="flat"
)
button_5.place(
    x=1025.0,
    y=664.0,
    width=229.0,
    height=49.84619140625
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_report(),
    relief="flat"
)
button_6.place(
    x=1278.0,
    y=657.0,
    width=169.0,
    height=53.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: search_patient(),
    relief="flat"
)
button_7.place(
    x=987.0,
    y=203.31982421875,
    width=169.0,
    height=49.2900390625
)

canvas.create_rectangle(
    599.0,
    269.0,
    1475.0,
    630.0,
    fill="#F1F1F3",
    outline="")

gender_var = StringVar()
gender_entry = Combobox(
    values=["Female", "Male"],
    textvariable=gender_var,
    state="readonly",
    width=22,
)
gender_entry.place(
    x=254.5,
    y=312.0,
    width=233.0,
    height=47.0
)


table = Text(
    bd=0,
    bg="#F1F1F3",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 12),
)

table = Treeview(window, columns=('ID', 'Name', 'Gender', 'Date Of Birth', 'Phone Number', 'Number Of Reports'), show = 'headings')
table.place(x=604, y=274, width=870, height=356)

table.column("ID", stretch=NO, width=110)
table.heading('ID', text='ID')
table.column("Name", stretch=NO, width=160)
table.heading('Name', text='Name')
table.column("Gender", stretch=NO, width=150)
table.heading('Gender', text='Gender')
table.column("Date Of Birth",stretch=NO, width=150)
table.heading('Date Of Birth', text='Date Of Birth')
table.column("Phone Number", stretch=NO, width=150)
table.heading('Phone Number', text='Phone Number')
table.column("Number Of Reports", stretch=NO, width=150)
table.heading('Number Of Reports', text='Number of Reports')
#table.grid(row=0, column=0, sticky='nsew')
error_label = canvas.create_text(
    200,
    600,
    text="",
    fill="red",
    font=("Arial", 12)
)

def show_all_data():
    patients_ref = db.collection('patients')
    query = patients_ref.order_by('id').get()  # Order the data by ID

    table.delete(*table.get_children())  # Clear existing table rows

    for doc in query:
        reports_ref = db.collection('reports')
        report_query = reports_ref.where('patient_id', '==', doc.id).get()

        data = doc.to_dict()
        table.insert('', 'end', values=(data['id'], data['name'], data['gender'], data['DOB'], data['phone'], len(report_query)))

show_all_data()

window.resizable(True, True)
window.mainloop()
