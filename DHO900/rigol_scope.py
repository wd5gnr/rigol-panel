import pyvisa

class Scope:
    def __init__(self):
        # state
        self.connected=False
        self.visa=None
        self.scope=None

    def connect(self,usb,cxstring):
        if usb==0:
            cxstr="TCPIP::"+cxstring+"::INSTR"
        else:
            cxstr="USB0::0x1AB1::0x044C::"+cxstring+"::INSTR"
        self.visa=pyvisa.ResourceManager()
        self.scope=self.visa.open_resource(cxstr)
        self.connected=True

    def query(self,string):
        s=self.scope.query(string)
        if isinstance(s,str):
            return s[0:len(s)-1]
        else:
            return s

    def write(self,string):
        return self.scope.write(string)

    def id(self):
        return self.query("*IDN?")
    
    def trig_status(self):
        return self.query(":TRIG:STAT?")

    def trig_sweep(self,stype=None):
        if stype==None:
            return self.query(":TRIG:SWE?")
        else:
            self.write(":TRIG:SWE "+stype)
    
    def stop(self):
        self.write(":STOP")
    
    def run(self):
        self.write(":RUN")

    def single(self):
        self.write(":SINGLE")

    def auto(self):
        self.write(":AUTO")

    def vpos(self,chan,dir=1):
        if dir!=0:
            off=float(self.query(":CHAN"+str(chan)+":OFFS?"))
            off+=dir*0.1
        else:
            off=0.0
        self.write(":CHAN"+str(chan)+":OFFS "+str(off))

    def vscale(self,chan,dir=1):
        scale=float(self.query(":CHAN"+str(chan)+":SCAL?"))
        scale+=dir
        self.write(":CHAN"+str(chan)+":SCAL "+str(scale))
    
    def hpos(self,dir=1):
        if dir!=0:
            off=float(self.query(":TIM:OFFS?"))
            off+=dir*0.1
        else:
            off=0.0
        self.write("TIM:OFFS "+str(off))

    def hscale(self,dir=1):
        scale=float(self.query(":TIM:SCAL?"))
        if dir==1:
            scale*=10
        else:
            scale/=10
        self.write(":TIM:SCAL "+str(scale))

    
