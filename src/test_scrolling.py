# encoding: utf-8
"""
LizardWizard.py

Created by Julien Pilla on 2010-05-20.
"""

import sys
from multiprocessing import Pool

from pyguane.game import Game
from pyguane.core.window import Window
from pyguane.map.tilemap import TileMap
from pyguane.map.tile import Tile
from pyguane.resources.resourcefactory import ResourceFactory
from pyguane.camera import Camera

from pygame.color import Color
from pygame.mouse import set_visible as setMouseVisible
from pygame.display import flip as displayFlip
from random import randint, choice
from math import *

from pyguane.core.librarian import Librarian

from pyguane.widgets.label import Label
from pyguane.sprites.factory import SpriteFactory




BLUE = (8, 69, 133)
GREY = (242, 242, 242)


class Simulation(Game):
    def __init__(self, w, h):
        super(Simulation, self).__init__(w, h)
        Window().bgd = Color(*GREY)
        Window().caption = "Yet Another Multilayer Perceptron: a driving simulation"
        ResourceFactory("media/resources.json")
                
        setMouseVisible(False)
        
        sprite_factory = SpriteFactory()
        loading_label = Label(0, 0, 28, u"Loading...", kind="widget.label.loading", color=BLUE)
        sprite_factory.showSpritesFromKind("widget.label.loading", True)
        
        surface = Window().surface
        surface.fill(GREY)
        loading_label_pos = (surface.get_rect().centerx - loading_label.width/2, 
                             surface.get_rect().centery - loading_label.height/2)
        surface.blit(loading_label.sprite.image, loading_label_pos)
        displayFlip()
               
        
        self.camera = Camera(Window().rect)       
        self.addObjects("camera.main", self.camera)        
       
        TileMap("media/scrolling_map_data.dump").tiles       
                
        self.observeKeyboard(self.myMainKeyboard)
        
        self.sprite_factory.initQuadTree(depth=3)

        #destroy the loading screen
        sprite_factory.delSpritesFromKind("widget.label.loading")
        displayFlip()
        
        self.updateWorld(self.updateGame) 
        self.updateGame()  

        
    def updateGame(self):
        tick = self.clock.tick()      

        self.updateObjects(tick)        
        self.physic_world.step(1.0 / 60.0, 10, 8)
        
        
    def myMainKeyboard(self, keysdown, keysup):
        if "escape" in keysdown:
            #print self," exits !"
            sys.exit()
            
        if "d" in keysdown:
            self.physic_world.debug = not self.physic_world.debug
            
        if "f" in keysdown:
            Window().toggleFullscreen()
            
        if "r" in keysdown:
            self.camera.moveIP(6, 0)
        if "l" in keysdown:
            self.camera.moveIP(-6, 0)


            
            
if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    # Let's go !
    Simulation(1024, 640).hatch()

    


