# -*- coding: utf-8


#from pygame.color import Color
#from pygame.draw import circle
#from pygame.rect import Rect
#from pygame.surface import Surface
#from pyguane.physics.world import PhysicWorld
#from pyguane.sprites.factory import SpriteFactory
from math import *

from pygame.time import Clock
from pyguane.gameobjects.gameobject import GameObject
from pyguane.resources.resourcefactory import ResourceFactory
from random import random
from vision import Vision
import pickle

            

def smooth(value):
    return round(floor(10 * value)) / 10. if value >= 0 else round(ceil(10 * value)) / 10.


class Vehicule(GameObject):
    def __init__(self, x, y, color, angle=0.0, vision_radius=100, vision_width=100):
        super(Vehicule, self).__init__()

        self._sprite = ResourceFactory().makeSpriteFromSymbol(color, x, y, 10)
        #self._sprite.playClip("pulse", 30)
         
        self._body = ResourceFactory().makeBodyFromSymbol(color, x, y)
        self._body.user_data = self
        
        self._manual_speed = 20.3
        self._auto_speed = 80 * (1 + random() + random()) 

        self._angle = angle
        self._last_angle = angle
        self._angle_step = 8
        
        self._vision_width = float(vision_width)
        self.vision = Vision(self.sprite.center, 0, self.angle, vision_radius, vision_width, layer=9)

        with open("perceptron.dump") as perceptron_dump:
            self._brain = pickle.load(perceptron_dump)

        self._brain_anwser = [0, 0]
        self._answers = {"left": 1, "front": 1, "right": 1}
        
        self._idle_clock = Clock()
        self._idle_angle = 0
        self._maneuvering = False
        self._maneuver_dir = 0
        self._start_maneuvering = False
     
    @property
    def bounding_rect(self): return  self.vision.sprite.rect       
    
    @property
    def body(self):
        return self._body 
    
    @property
    def angle(self): return self._angle
    @angle.setter
    def angle(self, value): self._angle = value % 360
    
    @property
    def sprite(self): return self._sprite
    
    def isIdling(self): return (self._brain_anwser[0] ** 2 + self._brain_anwser[1] ** 2) #<= limit
    
    def keyboard(self, keysdown, keysup):
        if "left" in keysdown:
            self.angle = self.angle + self._angle_step
        if "right" in keysdown:
            self.angle = self.angle - self._angle_step
        if "up" in keysdown:
            self.move(self._manual_speed)
        if "down" in keysdown:
            self.move(-self._manual_speed)
    
    def move(self, speed):
        #move the body
        dx, dy = self.vision.direction[0] * speed, self.vision.direction[1] * speed
        self._body.setLinearVelocity((dx, dy))
        #print dx, dy
        #move the sprite
        px, py = self._body.position
        #dx, dy = px -self.sprite.rect.left,  py - self.sprite.rect.top
        self.sprite.moveToIP(px, py)
        self.sprite.rect = self.sprite.position
        #self.vision.sprite.rect = self.vision.sprite.position  #========
        #print self.sprite.position, self.sprite.rect
        
    def update(self, tick):
        
        self.vision.updateSprite(self.sprite.center, self.angle)
        if self._last_angle != self.angle:
            #self.sprite.rotateIP(self.angle)
            pass
        self._last_angle = self.angle
        
        idling_score = self.isIdling()
        
        if self._maneuvering:
            self._idle_timer += self._idle_clock.tick()
            if self._idle_timer > 150:
                self._maneuver_dir *= 0.95
        
        elif idling_score <= 0.015:
            d = self._angle % 90
            closest_pi2 = self.angle + d - (self.angle + d) % 90
            self._maneuver_dir = -1 if self.angle < closest_pi2 else 1
            #print closest_pi2, self._maneuver_dir
            self._maneuvering = True
            self._idle_clock = Clock()
            self._idle_timer = 0

        
        if abs(self._maneuver_dir) <= 0.01:
            self._maneuver_dir = 0
            self._maneuvering = False
        elif idling_score <= 0.4:
            self.angle = self.angle + self._maneuver_dir * 5

    
    @property
    def sensor(self): return self._answers
    
    @property
    def output(self): return self._brain_anwser
    
    def feed(self, obstacles_rects):
        #filtre les tiles qui sont en collision avec le bouding rect du sprite de la vision
        self._answers = self.vision.collide(self.sprite.center, obstacles_rects, self.angle)
        left, front , right = self._answers["left"], self._answers["front"], self._answers["right"]

        self._brain_anwser = self._brain.compute([left, front, right])
        delta_angle = smooth(self._brain_anwser[1])
        self.angle = self.angle - delta_angle * 3
        #print self._brain_anwser[0]*self._auto_speed
        self.move(self._brain_anwser[0] * self._auto_speed)
        #print [left, front, right], " -> ", (smooth(self._brain_anwser[0]), smooth(self._brain_anwser[1]))
        
        
