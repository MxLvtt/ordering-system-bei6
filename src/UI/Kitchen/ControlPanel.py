import ControlPanelBackground as bg
from tkinter import font as tkFont
from tkinter import *
import os



class ControlPanel(Frame):
     def __init__(self, parent, panelheight, panelbackground):
                super().__init__(
                master=parent,
               #  width=panelwidth,
                cnf={},
                height=panelheight,
                background=panelbackground
                )
                self.update()
                panelwidth = self.winfo_screenwidth()

                helv36 = tkFont.Font(family='Helvetica', size=20, weight='bold')

                base_folder = os.path.dirname(__file__)
                image_path1 = os.path.join(base_folder, 'arrowleft.gif')
                self.image_previous = PhotoImage(file=image_path1)
                PreviousPage = Button(self,text="Previous", image=self.image_previous, width=int(panelwidth / 5) ,font=helv36, height=panelheight,background="LightBlue4", compound="left", state = DISABLED, command= bg.previous_page)
                PreviousPage.grid(row=0,column=0)
               
                image_path2 = os.path.join(base_folder, 'arrowright.gif')         
                self.image_next = PhotoImage(file=image_path2)
                NextPage = Button(self,text="Next", image=self.image_next, width=int(panelwidth / 5) ,font=helv36, height=panelheight,background="LightBlue4" ,compound="right", command=bg.next_page)
                NextPage.grid(row=0, column=4, sticky=E)
                
                image_path3 = os.path.join(base_folder, 'Transparent.gif')
                self.image_tresparent = PhotoImage(file=image_path3)
                DoneButton = Button(self, width=int(panelwidth / 5) ,height=panelheight,image=self.image_tresparent, text="Done",background="green",font=helv36,compound="left", command=bg.set_done)
                DoneButton.grid(row=0, column=1)
        
                CancelButton = Button(self, text="Cancel",width=int(panelwidth / 5) , image=self.image_tresparent, height= panelheight,background="red",compound="left", font=helv36,command=bg.cancel_order)
                CancelButton.grid(row=0, column=2)
         
                SummaryButton = Button(self, text="Summary",width=int(panelwidth / 5) ,image=self.image_tresparent, height= panelheight,background="yellow",compound="left", font=helv36,command= bg.open_summary)
                SummaryButton.grid(row=0, column=3)
                self.update()

          
         
       