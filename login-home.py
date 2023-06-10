from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import subprocess
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\figmas\build\build\assets\login_home_imgs")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MyApp:
    def __init__(self, root):
        self.root = root
        

        self.hm_frame = Frame(self.root, width=1530, height=790)
        self.lg_frame = Frame(self.root, width=1530, height=790)

        

        def show_frame(name):
            frame = self.frames[name]
            frame.pack()

            # Hide other frames
            for key in self.frames:
                if key != name:
                    self.frames[key].pack_forget()

        def hm_canvas(frame):
            home_canvas = Canvas(
                frame,
                bg="#051747",
                height=790,
                width=1530,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )

            home_canvas.place(x=0, y=0)

            image_image_1 = PhotoImage(
                file=relative_to_assets("home_image_1.png")
            )

            image_1 = home_canvas.create_image(
                765.0,
                395.0,
                image=image_image_1
            )

            button_image_1 = PhotoImage(
                file=relative_to_assets("home_button_1.png")
            )

            button_1 = Button(
                home_canvas,
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: pt(),
                relief="flat"
            )
            button_1.place(
                x=84.0,
                y=94.0,
                width=413.0,
                height=376.0
            )

            button_image_2 = PhotoImage(
                file=relative_to_assets("home_button_2.png")
            )

            button_2 = Button(
                home_canvas,
                image=button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: login_frame(window),
                relief="flat"
            )
            button_2.place(
                x=1329.0,
                y=41.0,
                width=140.0,
                height=48.0
            )

            button_image_3 = PhotoImage(
                file=relative_to_assets("home_button_3.png")
            )

            button_3 = Button(
                home_canvas,
                image=button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: ex_opts(),
                relief="flat"
            )
            button_3.place(
                x=567.0,
                y=375.0,
                width=402.0,
                height=365.0
            )

            button_image_4 = PhotoImage(
                file=relative_to_assets("home_button_4.png")
            )

            button_4 = Button(
                home_canvas,
                image=button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: settings(),
                 relief="flat"
                )
            button_4.place(
                    x=1209.0,
                    y=42.0,
                    width=65.0,
                    height=51.0
                )

        def  lg_canvas(frame):
                login_canvas = Canvas(
                    frame,
                    bg = "#051747",
                    height = 790,
                    width = 1530,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge"
                )

                login_canvas.place(x = 0, y = 0)
                image_image_1 = PhotoImage(
                    file=relative_to_assets("login_image_1.png"))

                image_1 = login_canvas.create_image(
                    768.0,
                    395.0,
                    image=image_image_1
                )


                dr_id_var = IntVar()
                dr_id_var.set("")
                #entry_image_1
                id_entry_image = PhotoImage(
                    file=relative_to_assets("login_entry_1.png"))
                #entry_bg_1
                id_entry_bg = login_canvas.create_image(
                    757.0,
                    349.0,
                    image=id_entry_image
                )


                # entry_1
                id_entry = Entry(login_canvas,
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
                    file=relative_to_assets("login_entry_2.png"))
                #entry_bg_2
                pass_entry_bg = login_canvas.create_image(
                    757.0,
                    466.0,
                    image=pass_entry_image
                )
                # entry_2
                pass_entry= Entry(login_canvas,
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
                    file=relative_to_assets("login_button_1.png"))
                # button_1
                login_button = Button(login_canvas,
                    image=login_button_image,
                    borderwidth=0,
                    highlightthickness=0,
                    command=lambda: home_frame(window),
                    relief="flat"
                )
                login_button.place(
                    x=651.0,
                    y=512.0,
                    width=184.0,
                    height=74.0
                )
                
        hm_canvas(self.hm_frame)
        lg_canvas(self.lg_frame)

        self.frames = {}

        self.frames["login"] = self.lg_frame
        self.frames["home"] = self.hm_frame

        show_frame("login")

window = Tk()

window.geometry("1530x790")
window.configure(bg="#051747")
window.title("Cancer Detection Assistant")

app = MyApp(window)

# Run the main event loop
window.mainloop()


##################################### limit #############################################################################3 
# window = Tk()

# window.geometry("1530x790")
# window.configure(bg="#051747")
# window.title("Cancer Detection Assistant")
# def home_frame(window) : 
    

#     home_frame = Frame(window , width=1530, height=790)
#     # home_frame.pack()

#     home_canvas = Canvas(
#         home_frame,
#         bg = "#051747",
#         height = 790,
#         width = 1530,
#         bd = 0,
#         highlightthickness = 0,
#         relief = "ridge"
#     )

#     home_canvas.place(x = 0, y = 0)

#     image_image_1 = PhotoImage(
#         file=relative_to_assets("home_image_1.png"))

#     image_1 = home_canvas.create_image(
#         765.0,
#         395.0,
#         image=image_image_1
#     )

#     button_image_1 = PhotoImage(
#         file=relative_to_assets("home_button_1.png"))

#     button_1 = Button(home_canvas , 
#         image=button_image_1,
#         borderwidth=0,
#         highlightthickness=0,
#         command=lambda: pt() ,
#         relief="flat"
#     )
#     button_1.place(
#         x=84.0,
#         y=94.0,
#         width=413.0,
#         height=376.0
#     )


#     button_image_2 = PhotoImage(
#         file=relative_to_assets("home_button_2.png"))

#     button_2 = Button(home_canvas,
#         image=button_image_2,
#         borderwidth=0,
#         highlightthickness=0,
#         command=lambda: login_frame(window),
#         relief="flat"
#     )
#     button_2.place(
#         x=1329.0,
#         y=41.0,
#         width=140.0,
#         height=48.0
#     )


#     button_image_3 = PhotoImage(
#         file=relative_to_assets("home_button_3.png"))


#     button_3 = Button( home_canvas,
#         image=button_image_3,
#         borderwidth=0,
#         highlightthickness=0,
#         command=lambda: ex_opts() ,
#         relief="flat"
#     )
#     button_3.place(
#         x=567.0,
#         y=375.0,
#         width=402.0,
#         height=365.0
#     )

#     button_image_4 = PhotoImage(
#         file=relative_to_assets("home_button_4.png"))

#     button_4 = Button(home_canvas ,
#         image=button_image_4,
#         borderwidth=0,
#         highlightthickness=0,
#         command=lambda: settings() ,
#         relief="flat"
#     )
#     button_4.place(
#         x=1209.0,
#         y=42.0,
#         width=65.0,
#         height=51.0
#     )

#     def login() : 
#         script_path = r"login.py"
#         subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#         window.destroy()

#     def ex_opts() : 
#         script_path = r"examin_opt.py"
#         subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#         window.destroy()

#     def pt() : 
#         script_path = r"patients.py"
#         subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#         window.destroy()
#     def settings() : 
#         script_path = r"dr_pass_update.py"
#         subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#         window.destroy()
#     home_frame.pack()        
#     home_frame.tkraise()   
#     window.resizable(True, True)
#     window.mainloop()
    
    

# def login_frame(window): 
#     home_frame.pack_forget()
#     login_frame = Frame(window , width=1530, height=790)

#     login_frame.pack()

#     login_canvas = Canvas(
#         login_frame,
#         bg = "#051747",
#         height = 790,
#         width = 1530,
#         bd = 0,
#         highlightthickness = 0,
#         relief = "ridge"
#     )

#     login_canvas.place(x = 0, y = 0)
#     image_image_1 = PhotoImage(
#         file=relative_to_assets("login_image_1.png"))
    
#     image_1 = login_canvas.create_image(
#         768.0,
#         395.0,
#         image=image_image_1
#     )


#     dr_id_var = IntVar()
#     dr_id_var.set("")
#     #entry_image_1
#     id_entry_image = PhotoImage(
#         file=relative_to_assets("login_entry_1.png"))
#     #entry_bg_1
#     id_entry_bg = login_canvas.create_image(
#         757.0,
#         349.0,
#         image=id_entry_image
#     )


#     # entry_1
#     id_entry = Entry(login_canvas,
#         bd=0,
#         bg="#D9D9D9",
#         fg="#000716",
#         highlightthickness=0,
#         textvariable=dr_id_var
#     )

#     # entry_1
#     id_entry.place(
#         x=603.0,
#         y=325.0,
#         width=308.0,
#         height=46.0
#     )


#     dr_pass_var = StringVar()
#     # entry_image_2
#     pass_entry_image = PhotoImage(
#         file=relative_to_assets("login_entry_2.png"))
#     #entry_bg_2
#     pass_entry_bg = login_canvas.create_image(
#         757.0,
#         466.0,
#         image=pass_entry_image
#     )
#     # entry_2
#     pass_entry= Entry(login_canvas,
#         bd=0,
#         bg="#D9D9D9",
#         fg="#000716",
#         highlightthickness=0,
#         show='*',
#         textvariable=dr_pass_var
#     )
#     pass_entry.place(
#         x=604.0,
#         y=441.0,
#         width=306.0,
#         height=48.0
#     )

#     # button_image_1
#     login_button_image = PhotoImage(
#         file=relative_to_assets("login_button_1.png"))
#     # button_1
#     login_button = Button(login_canvas,
#         image=login_button_image,
#         borderwidth=0,
#         highlightthickness=0,
#         command=lambda: home_frame(window),
#         relief="flat"
#     )
#     login_button.place(
#         x=651.0,
#         y=512.0,
#         width=184.0,
#         height=74.0
#     )


#     def login_and_open_file():

#         cred = credentials.Certificate('firebase\cancerdetection-8f9e0-firebase-adminsdk-iqsdf-23750ab0b9.json')

#         if not firebase_admin._apps:
#             firebase_admin.initialize_app(cred)

#         db = firestore.client()

#         data = {'dr_id':dr_id_var.get()}

#                 # Write the dictionary to the file in JSON format
#         with open('login_data.json', 'w') as file:
#                 json.dump(data, file)

#         # Retrieve document from 'doctores' collection
#         doc_ref = db.collection('doctors').where('id', '==', dr_id_var.get()).where('password', '==', dr_pass_var.get()).limit(1).stream()
#         documents = [doc for doc in doc_ref]

#         if documents:
#             doc = documents[0] 
#             role = doc.get('dr') 
#             if role == 0 :  
#                 script_path = r"admin.py"
#                 subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#                 window.destroy()

#             else :
#                 script_path = r"home.py"
#                 subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
#                 window.destroy()

#         else:
#             print("Wrong doctor password or ID")
#             no_p_lbl = Label(text="Wrong doctor password or ID!", fg="white", font=("Arial", 12, "bold"), bg='red')
#             no_p_lbl.place(x=651, y=630)
     
#     login_frame.pack()        
#     login_frame.tkraise()   
#     window.resizable(True, True)
#     window.mainloop()
# ######################################  home2 canvas ##################################################################################  

# home_frame(window) 




