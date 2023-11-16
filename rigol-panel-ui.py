from tkinter import *
from tkinter.ttk import *

class Button1(Frame):
    def __init__(self, parent,text='',command=None,width=1):
        Frame.__init__(self,parent)
        self.btn=Button(self,text=text,command=command,width=width)
        self.btn.grid(row=0, column=0)

class Arrows(Frame):
    UP=0
    DOWN=1
    RIGHT=2
    LEFT=3
    EXEC=4
    def __init__(self,parent,callback=None):
        Frame.__init__(self,parent)
        self.callback=callback
        self.upbtn=Button1(self,text="^",command=lambda: self.press(Arrows.UP))
        self.dnbtn=Button1(self,text="V",command=lambda: self.press(Arrows.DOWN))
        self.rtbtn=Button1(self,text=">",command=lambda: self.press(Arrows.RIGHT))
        self.lfbtn=Button1(self,text="<",command=lambda: self.press(Arrows.LEFT))
        self.exebtn=Button1(self,text="*",command=lambda: self.press(Arrows.EXEC))
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

class rigol_panel_ui:

    def __init__(self):
        self.top = Tk()
        self.usbnet=IntVar(value=0)
        self.top.geometry("300x600")
        self.top.minsize(250,600)
        self.top.maxsize(400,800)
        self.top.title("Rigol Panel")
        self.unframe=Frame(self.top)
        self.cframe=Frame(self.top)
        self.netbtn=Radiobutton(self.unframe,text='TCP/IP',value=0,var=self.usbnet)
        self.usbbtn=Radiobutton(self.unframe,text='USB',value=1,var=self.usbnet)
        self.conn_btn=Button(self.cframe,text="Connect",command=self.do_connect)
        self.msg = Label(self.top,text="Message")
        self.status = Label(self.top,text="Disconnected")
        self.cstring = Entry(self.cframe)
        self.clabel=LabelFrame(self.top,text='Control')
        self.rsbtn=Button(self.clabel,text="Run/Stop",command=self.do_rs)
        self.singbtn=Button(self.clabel,text="Single",command=self.do_single)
        self.autobtn=Button(self.clabel,text='Auto',command=self.do_auto)
        self.vlabel=LabelFrame(self.top,text='Vertical')
        self.vselect=Combobox(self.vlabel,state='readonly',
            values=['CH1','CH2','CH3','CH4','M1','M2','M3','M4','REF'])
        self.vselect.set('CH1')
        self.vdpad=Arrows(self.vlabel,self.do_vert)
        self.hlabel=LabelFrame(self.top,text="Horizontal")
        self.hdpad=Arrows(self.hlabel,self.do_horiz)
        self.triglabel=LabelFrame(self.top,text="Trigger")
        self.trigup=Button1(self.triglabel,text='^',command=self.do_trigup)
        self.trigdn=Button1(self.triglabel,text="V",command=self.do_trigdn)
        self.tselect=Combobox(self.triglabel,state='readonly',
            values=['Auto','Norm','Single'])
        self.tselect.set('Auto')
        self.tselect.bind("<<ComboboxSelected>>",self.trigchange)

        # arrange
        self.netbtn.pack(side="left")
        self.usbbtn.pack(side="left")
        self.unframe.pack(side="top")
        self.conn_btn.pack(side="left")
        self.cstring.pack(side="left")
        self.cframe.pack(side="top")
        self.rsbtn.pack(side="left")
        self.singbtn.pack(side="left")
        self.autobtn.pack(side="left")
        self.clabel.pack(side='top',fill='both',expand='yes')
        self.vselect.pack(side="top")
        self.vdpad.pack(side="top")
        self.vlabel.pack(side="top",fill="both",expand="yes")
        self.hdpad.pack(side="top")
        self.hlabel.pack(side="top",fill="both",expand="yes")
        self.trigup.pack(side='top')
        self.trigdn.pack(side='bottom')
        self.tselect.pack(side='bottom')
        self.triglabel.pack(side='top',fill='both',expand='yes')
        self.status.pack(side="bottom", fill='x')
        self.msg.pack(side="bottom", fill='x')

    def trigchange(self,event):
        print(self.tselect.get())

    def do_trigup(self):
        pass

    def do_trigdn(self):
        pass

    def do_rs(self):
        pass

    def do_auto(self):
        pass

    def do_single(self):
        pass

    def do_vert(self,key):
        print("***",key,self.vselect.get())
    
    def do_horiz(self,key):
        print("HHH",key)

    def do_connect(self):
        print("Connect",self.cstring.get(),self.usbnet.get(),self.vselect.get())

    def tick(self):
        print("Tick!")
        self.top.after(1000,self.tick)

    def mainloop(self):
        self.top.after(1000,self.tick)
        self.top.mainloop()


if __name__=="__main__":
    w=rigol_panel_ui()
    w.mainloop()

    

