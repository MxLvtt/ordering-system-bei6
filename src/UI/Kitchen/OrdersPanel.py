from tkinter import *
from odertile import OrderTileGUI
from random import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import messagebox




class OrdersPanel(Frame):
     def  __init__(self, parent, panelbackground):
          super().__init__(
                master=parent,
                cnf={},
               #  width= panelwidth,
               #  height= panelheight,
                background=panelbackground,
          )


          self._idx =1
          self._idxr = 0
        


          addbutton = Button(self, text="+" , height = 5 , width=5,  background="blue", command=self.add_order_tile)
          addbutton.grid(sticky=N+W,row=0,column=0)


        #   canvas = Canvas(self)
        #   scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        #   self.scrollable_frame = ttk.Frame(canvas)

        #   self.scrollable_frame.bind(
        #       "<Configure>",
        #       lambda e: canvas.configure(
        #           scrollregion=canvas.bbox("all")
        #       )
        #   )

        #   canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        #   canvas.configure(yscrollcommand=scrollbar.set)

        #   canvas.pack(side="left", fill="both", expand=True)
        #   scrollbar.pack(side="right", fill="y")




     def add_order_tile(self):

         rh = random() * 500 + 200
         if self._idxr > 1:
              messagebox.showerror("Error", 'The window is full, you cannot add another order')
              return
         OrderTileGUI(parent=self, row=self._idxr, column=self._idx, height=rh)
         self._idx = self._idx + 1
         if self._idx == 4:
             self._idx = 0
             self._idxr = self._idxr + 1
             

 
 





# root = Tk()

# OrdersPanel(parent=root,panelbackground="grey")

# mainloop()
