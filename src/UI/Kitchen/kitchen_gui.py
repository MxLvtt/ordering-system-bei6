from tkinter import *
from ControlPanel import ControlPanel
from OrdersPanel import OrdersPanel
from ordertile import OrderTileGUI


class KitchenGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kitchen")
        root.config(background="black")

        root.update()


        rootHeight = root.winfo_height()
        rootWidth = root.winfo_width()
      

        controlPanelHeight = 80
        controlPanelWidth =  rootWidth

        ordersPanelHeight = rootHeight - controlPanelHeight 
        ordersPanelWidth  =  rootWidth

        self.ordersPanel = OrdersPanel(root, 'white')
        self.ordersPanel.pack(side=TOP,fill='both',expand=1)
        # self.ordersPanel.grid(row=0, column=0, padx=5 , pady= 5)

        self.controlPanel = ControlPanel(root,controlPanelHeight,'black')
        self.controlPanel.pack(side=BOTTOM,fill='x')
        # controlPanel.grid(row=1, column=0)
        # self.controlPanel.grid_propagate(0)
        
        self.controlPanel.set_command_add_button(self.ordersPanel.add_order_tile)
        self.controlPanel.set_command_next_button(self.ordersPanel.go_to_next_page)
        self.controlPanel.set_command_previous_button(self.ordersPanel.go_to_prev_page)



        mainloop()




  