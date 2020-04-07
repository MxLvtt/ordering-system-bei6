import ControlPanelBackground as bg
from tkinter import *
import os



class ControlPanel(Frame):
     def __init__(self, parent , panelwidth , panelheight, panelbackground):
                super().__init__(
                master=parent,
                width=panelwidth,
                height=panelheight,
                background=panelbackground
                )

                base_folder = os.path.dirname(__file__)
                image_path1 = os.path.join(base_folder, 'arrowleft.gif')
                self.image_previous = PhotoImage(file=image_path1)
                PreviousPage = Button(self,text="Previous", image=self.image_previous, width=int(panelwidth / 5) , height=panelheight, compound="left", state = DISABLED, command= bg.previous_page)
                PreviousPage.grid(row=0,column=0)

                image_path2 = os.path.join(base_folder, 'arrowright.gif')         
                self.image_next = PhotoImage(file=image_path2)
                NextPage = Button(self,text="Next", image=self.image_next, width=int(panelwidth / 5) , height=panelheight, compound="right", command=bg.next_page)
                NextPage.grid(row=0, column=4, sticky=E)
                
                DoneButton = Button(self, width=53 , height= 5, text="Done", command=bg.set_done)
                DoneButton.grid(row=0, column=1)
        
                CancelButton = Button(self, text="Cancel",width=53 , height= 5, command=bg.cancel_order)
                CancelButton.grid(row=0, column=2)
         
                SummaryButton = Button(self, text="Summary",width=53 , height= 5, command= bg.open_summary)
                SummaryButton.grid(row=0, column=3)


          
         
       