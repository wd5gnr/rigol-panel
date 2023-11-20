# Create a tiny button
from tkinter import *
from tkinter.ttk import *

class Button1(Button):
    def __init__(self, parent,text='',command=None,width=1):
        Button.__init__(self,parent,text=text,command=command,width=width)
