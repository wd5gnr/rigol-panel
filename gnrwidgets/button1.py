# Create a tiny button
from tkinter import *
from tkinter.ttk import *

class Button1(Frame):
    def __init__(self, parent,text='',command=None,width=1):
        Frame.__init__(self,parent)
        self.btn=Button(self,text=text,command=command,width=width)
        self.btn.grid(row=0, column=0)