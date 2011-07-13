# encoding: utf-8

from pyguane.resources.resourcefactory import ResourceFactory
from pyguane.gameobjects.gameobject import GameObject

from pyguane.physics.constants import BOX2D_UNITS_SYSTEM

from math import sqrt, floor



class NPC(GameObject):
    
    def __init__(self, symbol, sub_symbol, (x, y), layer):
        super(NPC, self).__init__()
        
        self._sprite = ResourceFactory().makeSpriteFromSymbol(symbol, x, y, layer)
        self._sub_symbol = sub_symbol
        self._body = ResourceFactory().makeBodyFromSymbol(symbol, x, y)
        self._body.user_data = self
        
        self._sprite.current_frame = "%s_rf" % self._sub_symbol
        
        self._speed = 13.5
        self._anim_speed = 180
        self._sprite.mobile = True
        
        self._last_body_position = self.body.position
        
        #print self.body.body

    def update(self, tick):
        #if not self._body.is_sleeping:
            lpx, lpy = self._last_body_position
            px, py = self._body.position
            
            dx, dy = px - lpx, py - lpy
            #print px, py
            px, py = px / BOX2D_UNITS_SYSTEM, py / BOX2D_UNITS_SYSTEM
            
            px = floor(px)#/ BOX2D_UNITS_SYSTEM)
            py = floor(py)#/ BOX2D_UNITS_SYSTEM)
            self.sprite.moveToIP(px , py)
            self.sprite.rect = self.sprite.position
            self.sprite.dirty = 1
            self._last_body_position = self.body.position
        
        
    @property
    def sprite(self): return self._sprite
    
    @property
    def body(self): return self._body
    
    def move(self, dx, dy):   
        self._body.setLinearVelocity((dx, dy))   


        
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
    



class Mousse(NPC):
    def __init__(self, symbol, sub_symbol, (x, y), layer):
        super(Mousse, self).__init__(symbol, sub_symbol, (x, y), layer)
    
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
                


        self.move(dx, dy)       
        if dx == 0 and dy == 0:
            self._sprite.stopClip()
            #self._body.setLinearVelocity((0, 0))
            
    
    
        
        
        
