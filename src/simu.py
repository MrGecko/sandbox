# encoding: utf-8
"""
LizardWizard.py

Created by Julien Pilla on 2010-05-20.
"""


from mousse import Mousse, VegSpawner
from pygame.color import Color #@UnresolvedImport
from pygame.display import flip as displayFlip
from pygame.mouse import set_visible as setMouseVisible
from pyguane.core.gamestate import TimeLockedState
from pyguane.core.window import Window
from pyguane.game import Game
from pyguane.map.tilemap import TileMap
from pyguane.resources.resourcefactory import ResourceFactory
from pyguane.widgets.label import Label
from pyguane.camera import Camera

from random import randint


#"TODO: regarder les collision filtering b2Shape.SetFilterData"

BLUE = (8, 69, 133)
GREY = (242, 242, 242)
GREEN_LEAF = (110, 153, 67)
BROWN_EARTH = (94, 56, 34)


class PlayingState(TimeLockedState):
    def __init__(self, game,):
        super(PlayingState, self).__init__(lock=1000)
        self._timer = 0
        self._game = game
        setMouseVisible(False)
        
        #build the loading screen
        loading_label = Label(0, 0, 28, u"Loading...", kind="widget.label.loading", color=BLUE)
        self._game.sprite_factory.showSpritesFromKind("widget.label.loading", True)
        
        surface = Window().surface
        surface.fill(GREY)
        loading_label_pos = (surface.get_rect().centerx - loading_label.width / 2,
                             surface.get_rect().centery - loading_label.height / 2)
        surface.blit(loading_label.sprite.image, loading_label_pos)
        displayFlip()
        
        #load game data
        tiles = TileMap("media/map_data.dump").tiles
        mousse = Mousse("renard", "00", (20, 210), 100)
        
        vegetables = ["carotte", "navet"]
        veg_spawners = []
        for i in range(1, 24):
            veg_spawners.append(VegSpawner("poulailler_%s" % (vegetables[randint(0, len(vegetables) - 1)]),
                                            (90 + randint(30, 720), 170 + randint(-80, 320)), 98))
        

        self._game.addObjects("map", tiles)
        self._game.addObjects("characters", mousse)
        self._game.addObjects("items", veg_spawners)

        
        self._camera = Camera()
        self._game.addObjects("camera", self._camera)

        self._game.observeKeyboard(mousse.keyboard, self.keyboard)
        #destroy the loading screen
        self._game.sprite_factory.delSpritesFromKind("widget.label.loading")
        Window().bgd = BROWN_EARTH
        displayFlip()
        
        
    @property
    def time(self): 
        return self._timer
        
    def update(self, *args, **kwargs):
        super(PlayingState, self).update()
        tick = kwargs["tick"]
        self._timer += tick

        self._game.updateObjects(tick=tick, delta=self._camera.delta)        
        self._game.physic_world.step(1.0 / 60.0, 6, 6)
        self._game.sprite_factory.update("*", tick)
        
    def keyboard(self, keysdown, keysup):
        if "k" in keysdown:
            self._camera.moveIP(17, 0)
        elif "l" in keysdown:
            self._camera.moveIP(-17, 0)

    def release(self):
        self._game.delObjects("items")
        self._game.delObjects("map")
        self._game.delObjects("characters") 
        self._game.delObjects("camera")
        


class Simulation(Game):
    def __init__(self, w, h):
        super(Simulation, self).__init__(w, h)
        Window().bgd = Color(*GREY)
        Window().caption = "Pyguane: Sandbox level"
        ResourceFactory("media/resources.json")
                
        self.observeKeyboard(self.myMainKeyboard)
        self.updateWorld(self.updateGame) 

        self.state_manager.set(PlayingState, game=self)  
        #self._labels = {"Time" : Label(16, 12, 22, color=BLUE), }
        #self.addObjects("widgets.label", self._labels.values())
                
        self.rebootQuadTree()
        self.updateGame()  
        

    def rebootQuadTree(self):
        self.sprite_factory.initQuadTree(depth=4)
        self.sprite_factory.updateQuadGroupFromRect(Window().rect)
        self.sprite_factory.quadgroup.seek_dirties = True
        
    def updateGame(self):
        tick = self.clock.tick()            
        self.state_manager.update(tick=tick)  
        
    def myMainKeyboard(self, keysdown, keysup):
        if "escape" in keysdown:
            self.stop()
            
        if "d" in keysdown:
            self.physic_world.debug = not self.physic_world.debug
            
        if "f" in keysdown:
            Window().toggleFullscreen()
            
        if "p" in keysdown:
            self.state_manager.pop()

        if "o" in keysdown:
            self.state_manager.set(PlayingState, game=self)
            self.rebootQuadTree()

            
if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    # Let's go !
    Simulation(1024, 640).hatch()

    

