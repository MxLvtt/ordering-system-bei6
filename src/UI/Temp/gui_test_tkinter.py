from tkinter import *

root = Tk()  # Fenster erstellen
root.attributes('-fullscreen', True)
root.wm_title("Raspberry Pi GUI")
root.config(background="#FFFFFF")

root.update()

rootHeight = root.winfo_height()
rootWidth = root.winfo_width()

lF_width = rootWidth * 1 / 4
leftFrame = Frame(root, width=lF_width-10, height=rootHeight-10, background="darkgray")
leftFrame.grid(row=0, column=0, padx=5, pady=5)
leftFrame.grid_propagate(0) # Ensures that the frame doesn't resize when widgets are added

leftLabel1 = Label(leftFrame, text="Platzhalter Text")
leftLabel1.grid(row=0, column=0, padx=10, pady=3)
leftLabel2 = Label(leftFrame, text="Dies ist ein Text\nmit mehreren Zeilen.")
leftLabel2.grid(row=1, column=0, padx=10, pady=3)

rF_width = rootWidth * 3 / 4
rightFrame = Frame(root, width=rF_width-10, height=rootHeight-10, background="darkgray")
rightFrame.grid(row=0, column=1, padx=5, pady=5)

mainloop()  # Updating GUI. Don't add further elements beneath.
