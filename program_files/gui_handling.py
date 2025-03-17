import tkinter as tk
import text_recognition_handling as trh
from tkinter.filedialog import askopenfile
from PIL import ImageTk,Image,ImageOps
import os

class MainWindow:
    def __init__(self):
        self.filename = None
        self.card_image = None
        self.card_image_angle = 0
        self.main = tk.Tk()
        self.window_width = 600
        self.window_height = 600
        self.main.geometry('{0}x{1}'.format(self.window_width,self.window_height))
        self.main.title('easyMTGpl')
        self.app_logo = tk.PhotoImage(file='program_files/resources/app_logo.png')
        self.main.iconphoto(True,self.app_logo)
        self.main.configure(background='#0f0f0f')
        self.description_box = tk.Text(self.main,width=1,wrap='word',fg='#ffffff',bg='#4f05ad',font=("TkDefaultFont",17))
        self.description_box.config(state=tk.DISABLED)
        self.canvas_for_card = tk.Canvas(self.main,width=1,height=1,bg='#4f05ad')
        self.slider = tk.Scale(self.main,width=20,length=1,showvalue=0,sliderlength=18,orient=tk.HORIZONTAL,from_=0,to=360,fg='#ffffff',bg='#4f05ad',troughcolor='#1f1f1f',state=tk.DISABLED,command=self.slider_funcionality)
        resize_button_icon = tk.PhotoImage(file='program_files/resources/mtg_logo.png')
        self.resize_button_icon_fixed = resize_button_icon.subsample(13,13)
        self.button_resize = tk.Button(self.main,height=1,width=1,bg='#0f0f0f',activebackground='#0f0f0f',borderwidth=0,image=self.resize_button_icon_fixed,command=self.resize_button_funcionality)
        self.button_choose_picture = tk.Button(self.main,height=1,text='Wybierz obraz',fg='#ffffff',bg='#4f05ad',activeforeground='#ffffff',activebackground='#4f05ad',font=("TkDefaultFont",23),command=self.choose_file)
        self.button_confirm = tk.Button(self.main,height=1,text='Zatwierdź',fg='#ffffff',bg='#4f05ad',activeforeground='#ffffff',activebackground='#4f05ad',font=("TkDefaultFont",23),state=tk.DISABLED,command=self.display_card_description)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=15)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_rowconfigure(3, weight=6)
        self.main.grid_columnconfigure(0, weight=3)
        self.main.grid_columnconfigure(1, weight=2)
        self.main.grid_columnconfigure(2, weight=4)
        self.description_box.grid(row=1, column=1, columnspan=2, rowspan=3, sticky="nsew",padx=(15,10),pady=(0,10))
        self.canvas_for_card.grid(row=1, column=0, columnspan=1, sticky="nsew",padx=(10,0),pady=(32,15))
        self.slider.grid(row=2, column=0, sticky="nsew",padx=(10,0),pady=(0,0))
        self.button_resize.grid(row=3, column=0, sticky="nsew",padx=(10,0),pady=(15,10))
        self.button_choose_picture.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=(30,45),pady=(25,15))
        self.button_confirm.grid(row=0, column=2, sticky="nsew",padx=(45,30),pady=(25,15))
    def run(self):
        self.main.mainloop()
    def choose_file(self):
        desktop_directory = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')
        file = askopenfile(mode ='r',filetypes=[('Obrazy','*.png .jpg .jpeg')],initialdir=desktop_directory)
        if file is not None:
            self.filename = file.name
            self.button_confirm.config(state=tk.NORMAL)
            self.display_card_image()
            self.slider.config(state=tk.NORMAL)
            self.card_image_angle = 0
            self.slider.set(0)
    def display_card_image(self):
        img = Image.open(self.filename)
        img = ImageOps.exif_transpose(img)
        img_width,img_height = img.size
        new_img_width,new_img_height = None,None
        canvas_width = self.main.winfo_width()/3.044
        canvas_height = self.main.winfo_height()/2.176
        new_img_width = int(canvas_width)
        dif = img_width/new_img_width
        new_img_height = int(img_height/dif)
        self.card_image = ImageTk.PhotoImage(img.rotate(self.card_image_angle).resize((new_img_width,new_img_height)))
        self.canvas_for_card.create_image(int(canvas_width*0.5),int(canvas_height*0.5),image=self.card_image,anchor='center')
    def display_card_description(self):
        description = trh.get_definitions(self.filename,self.card_image_angle)
        self.description_box.config(state=tk.NORMAL)
        self.description_box.delete('1.0',tk.END)
        self.description_box.insert(tk.END,description)
        self.description_box.config(state=tk.DISABLED)
    def slider_funcionality(self,angle):
        self.card_image_angle = int(angle)
        self.display_card_image()
    def resize_button_funcionality(self):
        if self.filename != None:
            self.display_card_image()
        if int(self.main.winfo_width()) < 1200:
            self.description_box.config(font=("TkDefaultFont",17))
        else:
            self.description_box.config(font=("TkDefaultFont",23))