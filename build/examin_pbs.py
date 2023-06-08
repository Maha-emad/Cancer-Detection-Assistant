
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
import os 
import sys
import subprocess


# imp : we should enter patient data then browse for the image 
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\figmas\build\build\assets\examin_pbs_imgs")


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
    command=lambda: login(),
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
    command=lambda: ex_opts(),
    relief="flat"
)
back_button.place(
    x=1097.0,
    y=48.0,
    width=140.0,
    height=48.0
)

gen_rep_button_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
gen_rep_button = Button(
    image=gen_rep_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: gen_rep(),
    relief="flat"
)
gen_rep_button.place(
    x=120.0,
    y=482.0,
    width=235.0,
    height=56.0
)

browse_button_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
browse_button = Button(
    image=browse_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: browse_file(),
    relief="flat"
)
browse_button.place(
    x=905.0,
    y=715.0,
    width=174.0,
    height=55.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    972.0,
    431.0,
    image=image_image_2
)

pnm_var = StringVar()
pnm_entry_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    238.0,
    321.5,
    image=pnm_entry_image 
    
)
pnm_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable = pnm_var
)
pnm_entry.place(
    x=121.5,
    y=297.0,
    width=233.0,
    height=47.0
)


pid_var = IntVar()
pid_var.set("")
id_entry_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    238.0,
    419.5,
    image=id_entry_image
)
id_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0 , 
    textvariable = pid_var
)
id_entry.place(
    x=121.5,
    y=395.0,
    width=233.0,
    height=47.0
)



def browse_file():
        
        pt_nm = pnm_var.get() 
        
        if  pt_nm=="" : 
            lbl=Label(text="Enter patient data!" , fg="white", font=("Arial", 12, "bold"),bg='red' , height =2, width =20 ) 
            lbl.place(x=600,y=723.0)
    
        else :    
            image_path =filedialog.askopenfilename()
            img =Image.open( image_path)
            predict_image(image_path ) 
  
        
        

           
def predict_image(image_path):
    model_path = "D:/best.pt"
#     model_path = "D:/best_skin.pt"
    if not os.path.exists(model_path):
        print(f"Model file '{model_path}' not found.")
        return
    model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
    
    image = Image.open(image_path)
    image = image.resize((452, 452))
    predictions = model(image)
   
    pred = predictions.pandas().xyxy[0]
    if len(pred) > 0:
        class_counts = pred["name"].value_counts()
        most_repeated_class = class_counts.idxmax()

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size=12)
        
        pred_set=set() 
        for index, row in pred.iterrows():
            x1, y1, x2, y2, conf, class_id = row[:6]
            predicted_class = model.names[int(class_id)]
            pred_set.add(predicted_class)
            
            confidence = "{:.2f}".format(float(conf))

            original_image_size = image.size
            x1 = int(x1 * original_image_size[0] / 452)
            y1 = int(y1 * original_image_size[1] / 452)
            x2 = int(x2 * original_image_size[0] / 452)
            y2 = int(y2 * original_image_size[1] / 452)

            draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=1)
            draw.text((x1, y1 - 10), f"{predicted_class} ({confidence})", fill="red", font=font)
            
            
        pred_list = list(pred_set)    
        data = {
          'p_id':pid_var.get() ,
          'p_nm': pnm_var.get(),
          'pred_set': pred_list
               }

            # Write the dictionary to the file in JSON format
        with open('shared_data.json', 'w') as file:
            json.dump(data, file)
            
        rendered_image = ImageTk.PhotoImage(image)
        output_lbl = Label(width=452, height=452, bg='#F1F2F4')
        output_lbl.place(x=700, y=190)
        label = Label(output_lbl, width=452, height=452)
        label.image = rendered_image
        label.configure(image=rendered_image)
        label.pack()
    
    
def login() :   
    script_path = r"login.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()
    
    
def ex_opts(): 
    script_path = r"examin_opt.py"
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    window.destroy()
    
def gen_rep():
    cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    # Access Firestore database
    db = firestore.client()
    
    # Retrieve document from 'patients' collection
    doc_ref = db.collection('patients').where('id', '==',  pid_var.get()).where('name', '==',  pnm_var.get()).limit(1).stream()
    documents = [doc for doc in doc_ref]
    
    if documents:
        script_path = r"Examin_rep_blood.py"
        subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        window.destroy()
        
        
    else:
        no_p_lbl = Label(text="No such patient", fg="white", font=("Arial", 12, "bold"), bg='#3E4B66', height=2, width=20)
        no_p_lbl.place(x=120, y=561)
        print("no patient")
    
    firebase_admin.delete_app(firebase_admin.get_app())

    
window.resizable(True, True)
window.mainloop()
