from ctypes import Structure, wintypes, POINTER, windll, pointer, WinError
from playsound import playsound
import threading, time
import tkinter as tk

class Energy(): 
    def BatteryState(*args):
       class EnergyStateSystem(Structure):
           _fields_ = [("ACLineStatus", wintypes.BYTE),
                       ("BatteryFlag", wintypes.BYTE),
                       ("BatteryLifePercent", wintypes.BYTE),]

       EnergyState = POINTER(EnergyStateSystem)

       GetSystemPowerStatus = windll.kernel32.GetSystemPowerStatus
       GetSystemPowerStatus.argtypes = [EnergyState]
       GetSystemPowerStatus.restype = wintypes.BOOL

       state = EnergyStateSystem()
       if not GetSystemPowerStatus(pointer(state)): raise WinError()

       charger, charge = state.ACLineStatus, state.BatteryLifePercent
       return (charger, charge)

def BattSt(*args):
    def run():
        global minBTT,maxBTT
        try:
            settings = [float(minBTT.get()),
                        float(maxBTT.get())]
            chargercharge = Energy.BatteryState()
            charger = chargercharge[0]
            charge = chargercharge[1]
            if charger == 0:
                if charge <= settings[0]: playsound('data/BttL.mp3')
            elif charger == 1:
                if charge >= settings[1]: playsound('data/BttH.mp3')
        except: pass
    th = threading.Thread(target=run); th.start()
    root.after(10000, BattSt)  
      
def Apply(*args):
    global SV
    minBTT.set(minBTT.get())
    maxBTT.set(maxBTT.get())
    f = open('data/BSDB','w')
    f.write(minBTT.get()+','+maxBTT.get())
    f.close(); BattSt()

root = tk.Tk()
root.title('Battery Scan')
root.minsize(235,180)
root.maxsize(235,180)
root.iconbitmap('data/bi.ico')

minBTT = tk.StringVar()
maxBTT = tk.StringVar()
f = open('data/BSDB','r')
settings = f.read()
if(len(settings)<3): settings = [15,99]
else: settings = settings.split(',')
minBTT.set(settings[0])
maxBTT.set(settings[1])
f.close()

LMinBTT = tk.Label(root, text = 'Min %')
EMinBTT = tk.Entry(root, textvariable = minBTT)
LMaxBTT = tk.Label(root, text = 'Max %')
EMaxBTT = tk.Entry(root, textvariable = maxBTT)

BSET = tk.Button(root, text = 'Start', command = Apply)

LMinBTT.place(relx = 0.02, rely = 0.15, relwidth = 0.46)
EMinBTT.place(relx = 0.02, rely = 0.30, relwidth = 0.46, relheight = 0.25)
LMaxBTT.place(relx = 0.52, rely = 0.15, relwidth = 0.46)
EMaxBTT.place(relx = 0.52, rely = 0.30, relwidth = 0.46, relheight = 0.25)

BSET.place(relx = 0.25, rely = 0.65, relwidth = 0.5, relheight = 0.25)

root.mainloop()
