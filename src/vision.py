from pygame.rect import Rect
from pygame.draw import line, polygon, circle
from pygame.color import Color
from pygame.surface import Surface

from pyguane.gameobjects.gameobject import GameObject
from pyguane.sprites.factory import SpriteFactory


from shapely.geometry import Polygon, Point
from math import sin, cos, radians



def clamp(value, a, b):
    if a > b: b, a = a, b
    if value <= a: return a
    if value >= b: return b
    return value


def shapeToPolygon(position, shape):
    dx, dy = position
    return Polygon([(x + dx, y + dy) for x,y in shape.vertices])

class Vision(GameObject):
    def __init__(self, center, ecart=0, angle=0, radius=250, width=80, layer=1):
        #assert 0 < width <= 180, "The vision width has to be greater than 0 and lower than pi."
        super(Vision, self).__init__()
        self.color = {"front" : (140, 140, 140), "side" : (80, 80, 80)}
        self._polygons = {}
        #build a sprite from a surface
        self.ecart = ecart
        
        img = Surface(((radius + self.ecart)*2, (radius + self.ecart)*2))
        img.fill(Color("green"))
        img.set_colorkey(Color("green"))
        img.set_alpha(60)
        
        self._sprite = SpriteFactory().fromSurface("vision", img, layer=layer)
        self._radius = float(radius)
        self._width = float(width)
        self._coeff = 1./2
        self._last_angle = -1
        self._last_center = (-1, -1)
        #first draw
        self.direction = cos(radians(angle)), sin(radians(angle))
        self.updateSprite(center, angle)
        
    @property
    def radius(self): return self._radius
    @property
    def width(self): return self._width
    @width.setter
    def width(self, value): self._width = value
    @property
    def coeff(self): return self._coeff
    @property
    def polygons(self): return self._polygons
    @property
    def sprite(self): return self._sprite
    
    def collide(self, center, shapes, angle):
        radius = self.radius + self.ecart
        abs_vision_center = Point(self.sprite.center)
        #compute distance from vision origin to each rect
        #consider to start with no detected collision 
        distances = {"left" : 1.0, "front" : 1.0, "right" : 1.0}
        
        _polygons = self.polygons    
        #pour chaque rectangle en collision avec le cercle
        for poly in [shapeToPolygon(position, shape) for position, shape in shapes]: 
            for key, vision_poly in _polygons.iteritems():
                
                intersection_poly = vision_poly.intersection(poly)
                if not intersection_poly.is_empty:
                    dist = abs_vision_center.distance(intersection_poly) / radius
                    #register the distance if it is the lowest
                    if dist < distances[key]:
                        distances[key] = dist
        
        return distances
        
         
    def updateSprite(self, pos, angle):
        angle = -angle
        
        if angle != self._last_angle:
            _d = self.ecart
            _radius = self.radius
            _width = self.width
            
            #helpers
            center = (_radius + _d*(1+cos(radians(angle))), _radius + _d*(1+sin(radians(angle))))
            coord = lambda a : (center[0]  + cos(radians(a))*_radius, center[1]  + sin(radians(a))*_radius)
            
            
            a0 = (center[0]  + cos(radians(angle + _width/2 + 90))*10, center[1]  + sin(radians(angle + _width/2 + 90))*10)
            
            a1 = coord(angle + _width/2.)
            a2 = coord(angle + _width/(2*1./self.coeff))
            
            b0 = (center[0]  + cos(radians(angle - _width/2 - 90))*10, center[1]  + sin(radians(angle - _width/2 - 90))*10)
            
            b1 = coord(angle - _width/2.)
            b2 = coord(angle - _width/(2*1./self.coeff))
            
            absolute_coord = lambda a : (a[0] + pos[0] - _radius,  a[1]+ pos[1] - _radius)
            abs_coords = [absolute_coord(angle_step) for angle_step in (a1, a2, b1, b2, center)]
            
            self._polygons = {
                "left" : Polygon([abs_coords[4], absolute_coord(b0), abs_coords[2], abs_coords[3]]),
                "front" : Polygon([abs_coords[4], abs_coords[1], abs_coords[3]]),
                "right" : Polygon([abs_coords[4], absolute_coord(a0), abs_coords[0], abs_coords[1]]),
            }   
            #should I compute a new vision field ?
            
            _color = self.color
            _surf = self._sprite.image
            #clear the sprite
            _surf.fill(Color("green"))
            #draw three colored triangles
            polygon(_surf, _color["side"], [center, b0, b1, b2, center]) #left
            polygon(_surf, _color["front"], [center, a2, b2, center]) #front
            polygon(_surf, _color["side"], [center, a0, a1, a2, center]) #right
            
            self._last_angle = angle
            self._last_center = pos
            self.sprite.center = pos
            

            self.direction = cos(radians(angle)), sin(radians(angle))
            self.sprite.dirty = 1  
            
        
        
        elif pos != self._last_center:
            #perform only a translation
            dx, dy = pos[0]-self._last_center[0], pos[1]-self._last_center[1]
            
            new_polygons = {}
            for key, poly in self._polygons.iteritems():
                points_list = list(poly.exterior.coords)
                new_polygons[key] = Polygon([(x+dx, y+dy) for (x,y) in points_list])
                
            self._polygons = new_polygons
            self._last_center = pos
            self.sprite.center = pos
            self.sprite.dirty = 1
            
            

