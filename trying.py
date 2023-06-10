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
       

        self.frames = {}

        self.frames["home"] = self.hm_frame
        
        
        
        

    def show_frame(self,name):
        frame = self.frames[name]
        frame.pack()
        frame.tkraise()
        

        # Hide other frames
        for key in self.frames:
            if key != name:
                self.frames[key].pack_forget()


        
#         button_image_1 = PhotoImage(
#             file=relative_to_assets("home_button_1.png")
#         )

#         button_1 = Button(
#             home_canvas,
#             image=button_image_1,
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: pt(),
#             relief="flat"
#         )
#         button_1.place(
#             x=84.0,
#             y=94.0,
#             width=413.0,
#             height=376.0
#         )

#         button_image_2 = PhotoImage(
#             file=relative_to_assets("home_button_2.png")
#         )

#         button_2 = Button(
#             home_canvas,
#             image=button_image_2,
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: login_frame(window),
#             relief="flat"
#         )
#         button_2.place(
#             x=1329.0,
#             y=41.0,
#             width=140.0,
#             height=48.0
#         )

#         button_image_3 = PhotoImage(
#             file=relative_to_assets("home_button_3.png")
#         )

#         button_3 = Button(
#             home_canvas,
#             image=button_image_3,
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: ex_opts(),
#             relief="flat"
#         )
#         button_3.place(
#             x=567.0,
#             y=375.0,
#             width=402.0,
#             height=365.0
#         )

#         button_image_4 = PhotoImage(
#             file=relative_to_assets("home_button_4.png")
#         )

#         button_4 = Button(
#             home_canvas,
#             image=button_image_4,
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: settings(),
#              relief="flat"
#             )
#         button_4.place(
#                 x=1209.0,
#                 y=42.0,
#                 width=65.0,
#                 height=51.0
#             )


                
        
window = Tk()

window.geometry("1530x790")
window.configure(bg="#051747")
window.title("Cancer Detection Assistant")


# hm_frame = Frame(window, width=1530, height=790)

# home_canvas = Canvas(
#     hm_frame,
#     bg="#051747",
#     height=790,
#     width=1530,
#     bd=0,
#     highlightthickness=0,
#     relief="ridge"
# )

# home_canvas.place(x=0, y=0)

# image_image_1 = PhotoImage(
#     file=relative_to_assets("home_image_1.png")
# )

# image_1 =home_canvas.create_image(
#     765.0,
#     395.0,
#     image=image_image_1
# )
# hm_frame.tkraise()
window=Tk()
frame = Frame(window)
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



# Run the main event loop
window.mainloop()

