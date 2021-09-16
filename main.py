import numpy as np
import os
from tkinter import *
import classifier
from PIL import Image
import network
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.Cheking_btn_apply=False
        self.parent = parent
        self.color = "black"
        self.brush_size = 5
        self.setUI()
        self.button_Reset = Button(
            text="Reset!",
            width=35,
            height=1,
            bg="white",
            fg="black",
            command=lambda: [self.clear(), self.check()],
            font=25)
        self.button_Apply = Button(
            text="Apply!",
            width=35,
            height=1,
            bg="white",
            fg="black",
            command=lambda: [self.calculating(),self.which_button(), self.b_clicked(), self.save()],
            font=25
        )
        self.button_Reset.pack(side=TOP)
        self.button_Apply.pack(side=TOP)
    def draw(self, event):
        self.canv.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5,
                              fill=self.color, outline=self.color)
    def setUI(self):
        self.canv = Canvas(self,height=200,width=300)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canv.grid(padx=5, pady=5, sticky=E + W + S + N)
        self.canv.bind("<B1-Motion>", self.draw)
        self.canv.create_rectangle((0,0,1000,1000),fill='white')
    def clear(self):
        self.canv.destroy()
        self.setUI()
        if self.resultat_output.winfo_ismapped()==1:
            self.resultat_output.forget()
    def save(self):
        self.canv.update()
        self.canv.postscript(file="Images\\test.xps", colormode="color")
        im2 = Image.open("Images\\test.xps")
        im2.save("Images\\test.png", 'png')
    def check(self):
        if self.button_Apply['state'] == DISABLED:
            self.button_Apply['state'] = ACTIVE

    def b_clicked(self):
        self.Cheking_btn_apply = not self.Cheking_btn_apply
        self.button_Apply['state']=DISABLED
        self.resultat_output.pack()

    def which_button(self):  # res
        self.button_Apply['state'] = ACTIVE
    def calculating(self):
        im=classifier.get_image("Images\\test.png")
        res=network.modeling(im)
        vars = StringVar()
        vars.set("The result is " + str(res[0]) + "\n loss is " + str(res[1][0])+"accuracy is" + str(res[1][1]))
        self.resultat_output = Label(
            root, textvariable=vars,relief=RAISED)


WIDTH,HEIGHT=500,600
root = Tk()

fr=Frame(root)
fr.pack()
root.geometry("500x600")
app=Paint(fr)
app.pack(fill='both',expand=1)
root.mainloop()