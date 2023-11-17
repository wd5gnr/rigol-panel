from tkinter import *
from tkinter.ttk import *

from gnrwidgets.button1 import Button1


class Dpad(Frame):
    UP=0
    DOWN=1
    RIGHT=2
    LEFT=3
    EXEC=4
    def __init__(self,parent,callback=None):
        Frame.__init__(self,parent)
        self.callback=callback
        self.upbtn=Button1(self,text="^",command=lambda: self.press(Dpad.UP))
        self.dnbtn=Button1(self,text="V",command=lambda: self.press(Dpad.DOWN))
        self.rtbtn=Button1(self,text=">",command=lambda: self.press(Dpad.RIGHT))
        self.lfbtn=Button1(self,text="<",command=lambda: self.press(Dpad.LEFT))
        self.exebtn=Button1(self,text="*",command=lambda: self.press(Dpad.EXEC))
        self.upbtn.grid(row=0, column=1)
        self.lfbtn.grid(row=1, column=0)
        self.rtbtn.grid(row=1, column=2)
        self.dnbtn.grid(row=2,column=1)
        self.exebtn.grid(row=1,column=1)

# you have choices. Override press, override up/down/right/left/execute
# or set a callback. To set a callback you do not need to derive        
    def press(self,btn):
        if self.callback==None:
            [self.up, self.down, self.right, self.left, self.execute][btn]()
        else:
            self.callback(btn)

    # presumably you will override these or replace press or use callback   
    def up(self):
        print("Up")

    def down(self):
        print("Down")
    
    def right(self):
        print("Right")

    def left(self):
        print("Left")
    
    def execute(self):
        print("Execute")
