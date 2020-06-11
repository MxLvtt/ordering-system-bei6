from tkinter import *
# Importiere die andere Klasse, damit wir ein OrderTile benutzen können
from ordertile_test import OrderTileTest

"""

Alles was hier drin passiert, ist nicht Teil deiner Aufgabe.
Diese Datei dient nur zum testen deiner Fortschritte mit dem OrderTile,
der Code hier wird dann in der KitchenUI umgesetzt.

"""

# Platzhalter Variablen für die Größe des 'Order Tiles'
TILE_WIDTH = 400
TILE_HEIGHT = 600

# Erstellt ein objekt (root) des fensters
root = Tk()
# Setzt den Titel des Fensters
root.wm_title("Test Window For Order-Tile Development")
# Setzt die Hintergrundfarbe des Fensters (#696969 = Dunkelgrau)
root.config(background="#696969")
# Setzt die Größe des Fensters mit Format: <width>x<height>
root.geometry(f"{TILE_WIDTH}x{TILE_HEIGHT}+0+0")
# Gibt an, ob die Größe des Fenster geändert werden darf
# Argumente: x-resizable, y-resizable
root.resizable(True, True)

# Fügt ein 'OrderTile' zum Fenster hinzu und füllt das ganze Fenster damit (fill='both');
# 'both' heißt er füllt es in x- und y-Richtung. Ansonsten nur fill='x' oder 'y' angeben;
# Der 'OrderTile' soll auch die Größe verändern, wenn sich die Größe des Fensters ändert (expand=1);
ordertile_objekt = OrderTileTest(parent=root, background='green')
ordertile_objekt2= OrderTileTest(parent=root, background='green')
ordertile_objekt.pack(expand=1, fill='both')
# Alle Funktionen und Argumente kommen von der Klasse "Frame", von der die 'OrderTileTest' Klasse erbt;
# Deswegen können wir die auch bei 'OrderTileTest' benutzen. Man kann auch einfach sagen:
# Frame(root, bg='green').pack(expand=1, fill='both')

# Startet die main loop, so dass das Fenster angezeigt bleibt, bis man es schließt
mainloop()
