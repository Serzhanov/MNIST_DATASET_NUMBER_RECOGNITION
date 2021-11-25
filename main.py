import os
from tkinter import *
import classifier
from PIL import Image
import network
global vars
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.Checking_btn_apply=False
        self.parent = parent
        self.color = "black"
        self.brush_size = 6
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
            command=lambda: [self.save_image(),self.calculating(), self.b_clicked()],
            font=25
        )
        self.button_Reset.pack(side=TOP)
        self.button_Apply.pack(side=TOP)
        self.model_loss_metrics_values = Label(
            root, textvariable="", relief=RAISED)
        self.resultat_output = Label(
            root, textvariable="", relief=RAISED)
    def draw(self, event):
        self.canv.create_rectangle(event.x - 6, event.y -6 , event.x + 6, event.y + 6,
                              fill=self.color, outline=self.color)
    def setUI(self):
        self.canv = Canvas(self,height=375,width=475)
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
    def save_image(self):
        self.canv.update()
        self.canv.postscript(file="Images\\test.xps", colormode="color")
        im2 = Image.open("Images\\test.xps")
        im2.save("Images\\test.png", 'png')
    def check(self):
        if self.button_Apply['state'] == DISABLED:
            self.button_Apply['state'] = ACTIVE
    def b_clicked(self):
        if self.Checking_btn_apply == True:
            self.button_Apply['state']=ACTIVE
            self.Checking_btn_apply=False
        else:
            self.Checking_btn_apply = not self.Checking_btn_apply
            self.button_Apply['state']=DISABLED
    def calculating(self):
        im=classifier.get_image("Images\\test.png")
        res=network.modeling(im)
        print((network.val_loss*100,network.val_acc*100))
        self.model_loss_metrics_values.config(text=f'Loss value of model with test data is %d percentages and Metrics value for the model with test data is %d percentages\n\n' %(network.val_loss*100,network.val_acc*100))
        self.model_loss_metrics_values.pack()
        self.resultat_output.config(text=f'The result of image evaluation is %d\n'% res)
        self.resultat_output.pack()

WIDTH,HEIGHT=500,600
root = Tk()
fr=Frame(root)
fr.pack()
root.geometry("500x600")
app=Paint(fr)
app.pack(fill='both',expand=1)
root.mainloop()
