from tkinter import *
from ControlPanel import ControlPanel
from OrdersPanel import OrdersPanel


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

        ordersPanel = OrdersPanel(root, ordersPanelWidth, ordersPanelHeight, 'white')
        ordersPanel.grid(row=0, column=0, padx=5 , pady= 5)

        controlPanel = ControlPanel(root, controlPanelWidth, controlPanelHeight ,'black')
        controlPanel.grid(row=1, column=0)
        controlPanel.grid_propagate(0)


        root.mainloop()
