# encoding: utf-8

from pyguane.resources.resourcefactory import ResourceFactory
from pyguane.gameobjects.gameobject import GameObject

from pyguane.physics.constants import BOX2D_UNITS_SYSTEM

from math import sqrt, floor



class NPC(GameObject):
    
    def __init__(self, symbol, (x, y), layer):
        super(NPC, self).__init__()
        self._sprite = ResourceFactory().makeSpriteFromSymbol(symbol, x, y, layer)

        self._solid = ResourceFactory().makeSolidFromSymbol(symbol, x, y)
        if self._solid.body is not None:
            self._solid.body.user_data = self

        self._speed = 19.5
        self._anim_speed = 130
        self._sprite.mobile = True #sinon il sort du quadgroup. a revoir ?
        
        self._moved = True

    def update(self, tick, delta):
        if self._solid.body is not None:
            px, py = self._solid.body.position
            px, py = px / BOX2D_UNITS_SYSTEM, py / BOX2D_UNITS_SYSTEM
            px = floor(px - self._solid.relative_position[0])
            py = floor(py - self._solid.relative_position[1])

            self.sprite.moveToIP(px , py)
            if self._moved:            
                dx, dy = delta #delta camera
                self.sprite.rect.move_ip(dx + self.sprite.position.left - self.sprite.rect.left,
                                         dy + self.sprite.position.top - self.sprite.rect.top)
    
    @property
    def sprite(self): return self._sprite
    
    @property
    def body(self): return self._solid.body
    
    def move(self, dx, dy):   
        self._solid.body.linearVelocity = (dx, dy) 
        return (dx != 0) or (dy != 0)  


class Mousse(NPC):
    def __init__(self, symbol, sub_symbol, (x, y), layer):
        super(Mousse, self).__init__(symbol, (x, y), layer)
        self._sub_symbol = sub_symbol
        self._sprite.current_frame = "%s_rf" % self._sub_symbol

        
    def _walkRight(self):
        self._sprite.playClip("%s_walk_right" % self._sub_symbol, speed=self._anim_speed)
        pass
    def _walkLeft(self):
        self._sprite.playClip("%s_walk_left" % self._sub_symbol, speed=self._anim_speed)
        pass
    def _walkFront(self):
        self._sprite.playClip("%s_walk_front" % self._sub_symbol, speed=self._anim_speed)
        pass
    def _walkBack(self):
        self._sprite.playClip("%s_walk_back" % self._sub_symbol, speed=self._anim_speed)
        pass
    
        
    def keyboard(self, keysdown, keysup):         
        dx, dy = 0, 0
        
        if keysdown != []:
            step = self._speed
            
            if "left" in keysdown:
                if "up" not in keysdown and "down" not in keysdown:
                    self._walkLeft()
                    dx = -step
                else:
                    dx = -step / sqrt(2.0)
    
            if "right" in keysdown:
                if "up" not in keysdown and "down" not in keysdown:
                    self._walkRight()
                    dx = step
                else:
                    dx = step / sqrt(2.0)
               
    
            if "up" in keysdown:
                self._walkBack()
                if "left" not in keysdown and "right" not in keysdown:
                    dy = -step
                else:
                    dy = -step / sqrt(2.0)
            
            
            if "down" in keysdown:
                self._walkFront()
                if "left" not in keysdown and "right" not in keysdown:
                    dy = step
                else:
                    dy = step / sqrt(2.0)
                


        self._moved = self.move(dx, dy)       
        if not self._moved:
            self._sprite.stopClip()
            #self._body.setLinearVelocity((0, 0))
            
    
    
        
class VegSpawner(NPC):
    def __init__(self, symbol, (x, y), layer):
        super(VegSpawner, self).__init__(symbol, (x, y), layer)
        
    
    
