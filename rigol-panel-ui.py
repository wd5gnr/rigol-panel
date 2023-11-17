from tkinter import *
from tkinter.ttk import *

from gnrwidgets.dpad import Dpad
from gnrwidgets.button1 import Button1
from DHO900.rigol_scope import Scope

from pypref import SinglePreferences as Preferences


class Rigol_panel_ui:

    REFRESH_DELAY=250   # milliseconds

    def __init__(self):
        # state
        self.connected=False
        self.scope=None
        self.current_rs=1   # 1= run, 0=stop
        self.pref=Preferences(filename='rigol-panel-prefs.py')
        # ui
        self.top = Tk()
        self.top.protocol('WM_DELETE_WINDOW',self.top.destroy)
# style is only needed right now
        style=Style()
        style.configure("GoBtn.TButton",foreground="green")
        style.configure("StopBtn.TButton",foreground="red")

        self.usbnet=IntVar(value=0)
        self.top.geometry("300x600")
        self.top.minsize(250,600)
        self.top.maxsize(400,800)
        self.top.title("Rigol Panel")
        self.unframe=Frame(self.top)
        self.cframe=Frame(self.top)
        self.netbtn=Radiobutton(self.unframe,text='TCP/IP',value=0,var=self.usbnet)
        self.usbbtn=Radiobutton(self.unframe,text='USB',value=1,var=self.usbnet)
        self.usbnet.set(self.pref.get('usbnet',0))
        self.msg = Label(self.top,text="Disconnected")
        self.status = Label(self.top,text="Disconnected")
        self.cstring = Entry(self.cframe)
        self.cstring.insert(0,self.pref.get('visa_string',default='192.168.1.1'))
        self.conn_btn=Button(self.cframe,text="Connect",command=self.do_connect)
        self.clabel=LabelFrame(self.top,text='Control')
        self.rsbtn=Button(self.clabel,text="Run/Stop",command=self.do_rs,style="GoBtn.TButton")
        self.singbtn=Button(self.clabel,text="Single",command=self.do_single)
        self.autobtn=Button(self.clabel,text='Auto',command=self.do_auto)
        self.vlabel=LabelFrame(self.top,text='Vertical')
        self.vselect=Combobox(self.vlabel,state='readonly',
            values=['CH1','CH2','CH3','CH4'])
        self.vselect.set('CH1')
        self.vdpad=Dpad(self.vlabel,self.do_vert)
        self.hlabel=LabelFrame(self.top,text="Horizontal")
        self.hdpad=Dpad(self.hlabel,self.do_horiz)
        self.triglabel=LabelFrame(self.top,text="Trigger")
        self.tselect=Combobox(self.triglabel,state='readonly',
            values=['Auto','Normal','Single'])
        self.tselect.set('Auto')
        self.tselect.bind("<<ComboboxSelected>>",self.trigchange)

        # arrange
        self.netbtn.pack(side="left")
        self.usbbtn.pack(side="left")
        self.unframe.pack(side="top")
        self.conn_btn.pack(side="right")
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
        self.tselect.pack(side='top',fill='both',expand='yes')
        self.triglabel.pack(side='top',fill='both',expand='yes')
        self.status.pack(side="bottom", fill='y')
        self.msg.pack(side="bottom", fill='both',expand='yes')

        # grab enter key in connect string
        self.cstring.bind("<Return>",self.enter_connect)
        self.cstring.focus()

    def enter_connect(self,event):
        if self.connected==True:
            return
        self.do_connect()

    def trigchange(self,event):
        if self.connected==False:
            return
        self.scope.trig_sweep(self.tselect.get())

    def do_rs(self):
        if self.connected==False:
            return
        if self.current_rs==1:
            self.current_rs=0
            self.scope.stop()
        else:
            self.current_rs=1
            self.scope.run()

    def do_auto(self):
        if self.connected==False:
            return
        self.scope.auto()

    def do_single(self):
        if self.connected==False:
            return
        self.scope.single()

    def do_vert(self,key):
        if self.connected==False:
            return
        chan=int(self.vselect.get())
        if key==Dpad.UP:
            self.scope.vpos(chan,1)
        if key==Dpad.DOWN:
            self.scope.vpos(chan,-1)
        if key==Dpad.RIGHT:
            self.scope.vscale(chan,1)
        if key==Dpad.LEFT:
            self.scope.vscale(chan,-1)
        if key==Dpad.EXEC:
            self.scope.vpos(chan,0)
    
    def do_horiz(self,key):
        if self.connected==False:
            return
        if key==Dpad.RIGHT:
            self.scope.hpos(1)
        if key==Dpad.LEFT:
            self.scope.hpos(-1)
        if key==Dpad.EXEC:
            self.scope.hpos(0)
        if key==Dpad.UP:
            self.scope.hscale(1)
        if key==Dpad.DOWN:
            self.scope.hscale(-1)

    def do_connect(self):
        if self.connected==False:
            self.scope=Scope()
            self.scope.connect(self.usbnet.get(),self.cstring.get())
            self.connected=True
            self.status['text']=self.scope.id()
            self.pref.update_preferences({'visa_string': self.cstring.get()})
            self.pref.update_preferences({'usbnet': self.usbnet.get()})

# update our controls and model periodically
    def update_scope(self):
        if self.connected==False:
            return
        state=self.scope.trig_status()
        if state[0:4]=="STOP":
            self.rsbtn.configure(style="StopBtn.TButton")
            self.current_rs=0
        else:
            self.rsbtn.configure(style="GoBtn.TButton")
            self.current_rs=1
        # check for trigger mode
        state1=self.scope.trig_sweep()
        if state1[0:4]=="AUTO":
            self.tselect.set('Auto')
        if state1[0:4]=="NORM":
            self.tselect.set('Normal')
        if state1[0:4]=="SING":
            self.tselect.set('Single')
        if self.connected==True:
            msgstring="Connected "+state+" "+state1
        else:
            msgstring="Disconnected"
        self.msg['text']=msgstring

    def tick(self):
        self.update_scope()
        self.top.after(self.REFRESH_DELAY,self.tick)

    def mainloop(self):
        self.top.after(self.REFRESH_DELAY,self.tick)
        self.top.mainloop()


if __name__=="__main__":
    w=Rigol_panel_ui()
    w.mainloop()

    

