# -*- coding: utf-8 -*-

import FrostpyteEngine as fpe
from Constantes import *

fpe.init(frame_size * nbr_frame_x, frame_size * nbr_frame_y, fpe.Player("Gauthier", "./Sprites/Characters/Pirate", 0, 2), window_name, window_icon, frame_rate)

main_thread = fpe.MainRun()
main_thread.start()

Herbe = fpe.Tileset("./Sprites/Tilesets/Herbe", 0, 0, 20, 15)
fpe.drawTileset(Herbe)

Pirate2 = fpe.Sprite("./Sprites/Characters/Pirate", 5, 5)
fpe.drawSprite(Pirate2)
Pirate2.move_buffer = ["up", "up", "down", "down", "left"]

Pirate3 = fpe.Sprite("./Sprites/Characters/Pirate", 8, 8)
fpe.drawSprite(Pirate3)
Pirate3.move_buffer = ["down", "down", "down", "right", "right"]

Tonneau = fpe.GrObject("./Sprites/Tilesets/Tonneau/image.png", 9, 9, 1, False)
fpe.drawObject(Tonneau)

Tonneau2 = fpe.GrObject("./Sprites/Tilesets/Tonneau/image.png", 11, 12, 1, False)
fpe.drawObject(Tonneau2)
