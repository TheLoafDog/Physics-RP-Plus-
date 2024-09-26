from tkinter import *

darkGrey = '#ababab'

requiredPracticalList = ["RP1 Stationary Waves on a String", "RP2 Interference Effects", "RP3 Determination of g", "RP4 Determination of Young's Modulus", "RP5 Determination of Resistivity of a Wire", "RP6 Internal resistance and emf", "RP7 Simple Harmonic Motion", "RP8 Boyle's Law", "RP9 Charging and Discharging Capacitors", "RP10 Magnetic Force on a Wire", "RP11 Magnetic Flux Linkage", "RP12 Inverse Square Law"]

def main():
    root = Tk()
    
    root.title("Physics RP Plus")
    root.minsize(1080, 720)
    root.geometry("1080x720")
    
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 2)
    root.columnconfigure(1, weight = 8)
    
    sideBar = Frame(master = root, width = 200, height = 720, bd = 2, relief = "groove", bg = darkGrey)
    sideBar.grid(row = 0, column = 0, sticky = "nsew")
    
    sideBarTitle = Label(master = sideBar, width = 20, height = 3, text = "Physics RP Plus", bg = darkGrey, font = ('Arial', 12))
    sideBarTitle.place(relx = 0.5, rely = 0.05, anchor = CENTER)
    
    sideBarButtonFrame = Frame(master = sideBar, width = 150, height = 625, bd = 2, relief = "groove", bg = darkGrey)
    sideBarButtonFrame.place(relx = 0.5, rely = 0.525, anchor = CENTER)
    
    for i in range(0,12):
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125)
        newSideBarButton.grid(row = i, column = 0, padx = 5, pady = 5)
    
    mainFrame = Frame(master = root, width = 880, height = 720, bd = 2, relief = "groove")
    mainFrame.grid(row = 0, column = 1, sticky = "nsew")
    
    root.mainloop()

    
    
main()

