from tkinter import *

"""

Das ist die Datei, die du dann umsetzen sollst.

"""

# OrderTileTest Klassen-Definition; Erbt von "Frame" (eine Klasse von tkinter)
# Ein Frame ist einfach eine leere Fläche in die wir andere Elemente einfügen können, z.B. Buttons
class OrderTileTest(Frame):
    # Konstruktor der Klasse OrderTileTest
    def __init__(
        self, # das Argument muss immer in den Konstruktor, wird aber beim Aufrufen des Konstruktors (siehe 'ordertile_testing_area.py')
              # nicht gesetzt!
        parent, # Gibt an, zu welchem übergeordneten tkinter-Element dieses Frame eingefügt werden soll
        background="white" # Setzt die Hintergrundfarbe des Ordertiles, default Wert ist 'white'
        # Hier könnten noch weitere Parameter hinzugefügt werden
    ):
        # Mit super().__init__(...) rufen wir den Konstruktor von Frame (der Oberklasse) auf;
        # Dadurch wird im Hintergrund das eigentliche Frame Objekt erzeugt
        super().__init__(
            master=parent
            # Hier könnten noch weitere Parameter von 'Frame' gesetzt werden
        )

        self.timestamp = "15:08:12"
        self.meals = ["Meal1", "Meal2", "Meal3"];

        self.status_codes = [ "P", "C", "U" ] # Prepared, Canceled, Unprepared
        self.status_color_codes = [ "green", "red", "gray" ] # Prepared, Canceled, Unprepared

        self.status = 0 # <- Property

        self._change_background(color=self.status_color_codes[self.status])

        self.status_label = Label(text=self.status_codes[self.status]) # <- UI Element zur Property

        self.order_type = ""

        # Hier fügen wir ein Label (=Feld mit Text) zu unserem OrderTile hinzu
        # master=self: Das sagt dem Label, dass es zum OrderTile gehört
        # .grid(row=0,column=0): Das setzt das Label in das 'Grid' des OrderTiles in Zeile 0 und Spalte 0;
        #                        Wenn mehere Elemente gesetzt werden, kann man diese so an verschiedenen Stellen platzieren
        Label(master=self, text=self.timestamp).grid(row=0, column=0)


        def funktion_wenn_button_gedrueckt():
            print("Button gedrueckt!")
        
        # sticky="W" oder sticky=W : Sagt dem Button, dass er sich links (W = West) anordnen soll.
        # Mit "E" (= East) wäre der Button am rechten Rand angeordnet
        Button(master=self, text="Button", command=funktion_wenn_button_gedrueckt).grid(row=1, column=0, sticky="W")

    def _change_background(self, color: str):
        self.config(background=color)

    def _change_status(self, new_status: int) -> int:
        pass
