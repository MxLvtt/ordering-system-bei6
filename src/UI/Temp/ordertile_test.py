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
        ,status=status 
    ):
        # Mit super().__init__(...) rufen wir den Konstruktor von Frame (der Oberklasse) auf;
        # Dadurch wird im Hintergrund das eigentliche Frame Objekt erzeugt
        super().__init__(
            master=parent,
            background=background
            # Hier könnten noch weitere Parameter von 'Frame' gesetzt werden
        )
        self.status = status
        # Hier fügen wir ein Label (=Feld mit Text) zu unserem OrderTile hinzu
        # master=self: Das sagt dem Label, dass es zum OrderTile gehört
        # .grid(row=0,column=0): Das setzt das Label in das 'Grid' des OrderTiles in Zeile 0 und Spalte 0;
        #                        Wenn mehere Elemente gesetzt werden, kann man diese so an verschiedenen Stellen platzieren
        Label(self, text="Das ist ein Beispiel Text").grid(row=0, column=0)

        def funktion_wenn_button_gedrueckt():
            print("Button gedrueckt!")
        
        # sticky="W" oder sticky=W : Sagt dem Button, dass er sich links (W = West) anordnen soll.
        # Mit "E" (= East) wäre der Button am rechten Rand angeordnet
        Button(master=self, text="Button", command=funktion_wenn_button_gedrueckt).grid(row=1, column=0, sticky="W")
