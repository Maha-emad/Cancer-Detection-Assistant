import tkinter as tk
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import subprocess
from tkinter import filedialog
import functools
import json
from PIL import ImageTk, Image, ImageDraw, ImageFont
import torch
from tkinter import messagebox
from fpdf import FPDF
from tkinter import filedialog
import textwrap
import os 
import sys
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\figmas\build\build\assets\examin_rep_imgs")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def login()  :
    script_path = r"login.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()
    
def ex_pbs(): 
    script_path = r"examin_pbs.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()
    
def save_labels_to_pdf():
    # Get the content from labels
    content = []
    content.append("Name: " + nm_val_lbl["text"] + "\n")
    content.append("ID: " + str(id_val_lbl["text"]) + "\n")
    content.append("Gender: " + gen_val_lbl["text"] + "\n")
    content.append("Phone: " + phn_val_lbl["text"] + "\n")
    content.append("\nExamination Results:\n")
    content.append(hd1_lbl["text"] + "\n")
    if 'Early' in prd_set:
        content.append(e_lbl["text"] + "\n")
    if 'Pre' in prd_set:
        content.append(pre_lbl["text"] + "\n")
    if 'Pro' in prd_set:
        content.append(pro_lbl["text"] + "\n")
    if 'Benign' in prd_set:
        content.append(b_lbl["text"] + "\n")
    content.append(rec_lbl["text"] + "\n")

    # Apply line wrapping to the content
    wrapped_content = []
    for line in content:
        wrapped_lines = textwrap.wrap(line, width=90)
        wrapped_content.extend(wrapped_lines)

    # Open file dialog to choose save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save PDF"
    )

    # Save content to a PDF file
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in wrapped_content:
            pdf.cell(0, 10, txt=line, ln=True)
        pdf.output(file_path)

        print("Labels saved to PDF:", file_path)


def save_labels_to_online():
    # Get the Name from labels
    Name = []
    Name.append(nm_val_lbl["text"] + "\n")

    P_id = []
    P_id.append(int(id_val_lbl["text"]))  # Convert P_id to an integer

    Gender = []
    Gender.append(gen_val_lbl["text"] + "\n")

    Phone = []
    Phone.append(int(phn_val_lbl["text"]))

    report = []

    report.append(hd1_lbl["text"] + "\n")
    if 'Early' in prd_set:
        report.append(e_lbl["text"] + "\n")
    if 'Pre' in prd_set:
        report.append(pre_lbl["text"] + "\n")
    if 'Pro' in prd_set:
        report.append(pro_lbl["text"] + "\n")
    if 'Benign' in prd_set:
        report.append(b_lbl["text"] + "\n")
    report.append(rec_lbl["text"] + "\n")

    wrapped_Name = []
    for line in Name:
        wrapped_lines = textwrap.wrap(line, width=90)
        wrapped_Name.extend(wrapped_lines)

    # Convert the content to a single string
    pdf_Name = '\n'.join(Name)
    pdf_P_id = P_id[0]  # Store P_id as an integer
    pdf_Gender = '\n'.join(Gender)
    pdf_Phone = Phone[0]
    pdf_report = '\n'.join(report)

    # Get a Firestore collection reference
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    pdf_collection = db.collection('reports')

    # Check if patient_id exists
    p_docs = pdf_collection.where('P_id', '==', pdf_P_id).limit(1).get()
    if len(p_docs) > 0:
        # Patient exists, retrieve rep_no
        max_rep_no = 0
        for p_doc in p_docs:
            p_data = p_doc.to_dict()
            rep_no = int(p_data.get('rep_no', '0'))  # Convert to integer and default to 0 if not found
            max_rep_no = max(max_rep_no, rep_no)
        new_rep_no = max_rep_no + 1
    else:
        # Patient doesn't exist, set rep_no to 1
        new_rep_no = 1

        # Create a new document and set the PDF content
    new_doc = pdf_collection.document()
    new_doc.set({
        'Name': pdf_Name,
        'P_id': pdf_P_id,
        'Gender': pdf_Gender,
        'Phone': pdf_Phone,
        'report': pdf_report,
        'rep_no': new_rep_no
        # Add more content fields as needed
    })

    print("PDF saved to Firestore:", new_doc.id)
    lbl=Label(text = "Report saved", fg="white", font=("Arial", 12, "bold"),bg='#ADD8E6' , height =2, width =20 ) 
    lbl.place(x=300.0,y=709.0,)



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

logout_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
logout_button = Button(
    image=logout_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: login() ,
    relief="flat"
)
logout_button.place(
    x=1278.0,
    y=48.0,
    width=140.0,
    height=48.0
)

back_button_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
back_button = Button(
    image=back_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_pbs(),
    relief="flat"
)
back_button.place(
    x=1097.0,
    y=48.0,
    width=140.0,
    height=48.0
)

sv_button_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
sv_button = Button(
    image=sv_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=save_labels_to_online,
    relief="flat"
)
sv_button.place(
    x=567.0,
    y=709.0,
    width=182.0,
    height=71.0
)

print_button_image= PhotoImage(
    file=relative_to_assets("button_4.png"))
print_button = Button(
    image=print_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=save_labels_to_pdf,
    relief="flat"
)
print_button.place(
    x=777.0,
    y=709.0,
    width=191.0,
    height=71.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    737.0,
    470.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    732.0,
    204.0,
    image=image_image_3
)


with open('shared_data.json', 'r') as file:
    data = json.load(file)

pt_id = data['p_id']
pt_nm = data['p_nm']
prd_set = data['pred_set']

cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    
if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
db = firestore.client()
    

p_ref = db.collection('patients')

p_docs = p_ref.where('id', '==', pt_id).limit(1).get()

found = 0

if len(p_docs) > 0:
    print("hey")
    p_doc = p_docs[0]
    print('found')
    found = 1
    p_data = p_doc.to_dict()
    print(p_data)
    p_name = p_data['name']
    p_id = p_data['id']
    p_phone = p_data['phone']
    p_gender = p_data['gender']



else:
    print("patient not found")
xx = 97
if found == 1:
    
    nm_lbl = Label(text="Name:", font=("times new roman", 12, "bold"), bg='#BABDC5')
    nm_lbl.place(x=xx, y=191)
    xx += 65
    nm_val_lbl = Label(text=p_name, font=("times new roman", 12, "bold"), bg='#BABDC5')
    nm_val_lbl.place(x=xx, y=191)
    xx += 90

    id_lbl = Label(text="ID:", font=("times new roman", 12, "bold"), bg='#BABDC5')
    id_lbl.place(x=xx, y=191)
    xx += 65
    id_val_lbl = Label(text=p_id, font=("times new roman", 12, "bold"), bg='#BABDC5')
    id_val_lbl.place(x=xx, y=191)
    xx += 90

    gen_lbl = Label(text="Gender:", font=("times new roman", 12, "bold"), bg='#BABDC5')
    gen_lbl.place(x=xx, y=191)
    xx += 65

    gen_val_lbl = Label(text=p_gender, font=("times new roman", 12, "bold"), bg='#BABDC5')
    gen_val_lbl.place(x=xx, y=191)
    xx += 90

    phn_lbl = Label(text="Phone:", font=("times new roman", 12, "bold"), bg='#BABDC5')
    phn_lbl.place(x=xx, y=191)
    xx += 65

    phn_val_lbl = Label(text=p_phone, font=("times new roman", 12, "bold"), bg='#BABDC5')
    phn_val_lbl.place(x=xx, y=191)
    xx += 90

else:
    nm_lbl = Label(text="Patient not found", font=("times new roman", 12, "bold"), bg='#BABDC5')
    nm_lbl.place(x=xx, y=184)

Heading_txt = " Microscopic Examination and Diagnosis"

Early_txt = "Early-ALL cells  :  Found\nThe examination shows irregular cell shapes and an abnormal nuclear-to-cytoplasmic ratio. In addition, there is an increased number of immature and abnormal cells and decreased numbers\nof normal blood cells. Also,cells tend to form clusters or aggregates in the peripheral blood, indicating their tendency to associate with each other and potentially leading to the obstruction of\nblood vessels.\n"

pre_txt = "Pre-ALL cells  :  Found\nSome nuclei appear to be round and others are slightly irregular.The chromatin pattern is coarse. In addition, there is an abnormal proliferation of immature B-cell progenitors,as well as a significant\nnumber of blast cells (lymphoblasts), leading to a reduction in the number of normal blood cells.This reduction can cause anemia, thrombocytopenia, and decreased mature white blood cells.\n"

pro_txt = "Pro-ALL cells  :  Found\nHere, immature cellular features are observed, including large nuclei, fine chromatin pattern, prominent nucleoli, and scant cytoplasm.The nuclear shape is rounded and irregular, with a fine\ngranular chromatin pattern and dispersed chromatin clumps.There is a lack of cytoplasmic granules, as well as an increased number of blasts and a high nucleocytoplasmic ratio, indicating\nthe presence of immature cells and the presence of ribosomes and other protein synthesis machinery in the cytoplasm.\n"

benign_txt = "Benign-Cancer cells:  Found\nThe cellular composition appears normal with small, round lymphocytes, including more fragile cells known as 'smudge cells.'There is also an increased number of platelets; however, the platelets\nthemselves may appear normal in morphology. Additionally, there is an increased number of red blood cells.\n"

rec_txt = "Recommendations:\nIt is recommended to start following up with a hematologist in order to manage the treatment plan and coordinate care. In addition, it is important to start chemotherapy as soon as possible\nto avoid any progression in the proposed case. Also, supportive care measures must be implemented to manage and minimize treatment-related side effects.Emotional support and counseling\n should be provided to facilitate the treatment process.\n\nRemember,\n\"You never know how strong you are until being strong is your only choice.\""

nw_x = 95
nw_y = 265

hd1_lbl = Label(text=Heading_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
hd1_lbl.place(x=nw_x, y=nw_y)
nw_y += 40

if 'Early' in prd_set:
    e_lbl = Label(text=Early_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
    e_lbl.place(x=nw_x, y=nw_y)
    nw_y += 100
if 'Pre' in prd_set:
    pre_lbl = Label(text=pre_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
    pre_lbl.place(x=nw_x, y=nw_y)
    nw_y += 100

if 'Pro' in prd_set:
    pro_lbl = Label(text=pro_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
    pro_lbl.place(x=nw_x, y=nw_y)
    nw_y += 100

if 'Benign' in prd_set:
    b_lbl = Label(text=benign_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
    b_lbl.place(x=nw_x, y=nw_y)
    nw_y += 100

rec_lbl = Label(text=rec_txt, font=("times new roman", 12, "bold"), bg='#BABDC5', justify='left', anchor='w')
rec_lbl.place(x=nw_x, y=nw_y)

window.resizable(True, True)
window.mainloop()