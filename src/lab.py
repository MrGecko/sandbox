
import json
from random import choice , sample, randint   
from pygame.rect import Rect
from pprint import pprint
import itertools

import cPickle

resources = { 
    "orange" : {
            "filename" : "media/orange.png", "kind": "alive.character.bot",
            "body" : { 
                "filename": "media/bodies/vehicule_circle.obj",
                "mass" : 10.0 
                },
            },
                      
    "characters" : {"filename" : "media/charset.png", "kind" : "main.characters",
        "area" : (0, 0, 16, 25), #pour le body bounding rect car pas de mesh
        "body" : { "mass" : 10.0  },
        "animations" : {
            "frames" : {
                # the topleft red pirate
                "00_bl" : (0, 0, 16, 25), "00_bf" : (16, 0, 16, 25), "00_br" : (32, 0, 16, 25),
                "00_rl" : (0, 25, 16, 25), "00_rf" : (16, 25, 16, 25), "00_rr" : (32, 25, 16, 25),
                "00_fl" : (0, 50, 16, 25), "00_ff" : (16, 50, 16, 25), "00_fr" : (32, 50, 16, 25),
                "00_ll" : (0, 75, 16, 25), "00_lf" : (16, 75, 16, 25), "00_lr" : (32, 75, 16, 25),
                # triple patte
                "01_rf" : (48, 0, 17, 23),
            },
            "clips" : {
                "00_walk_right"  :  ["00_rr", "00_rf", "00_rl", "00_rf"],
                "00_walk_left"  :  ["00_lr", "00_lf", "00_ll", "00_lf"],
                "00_walk_back"  :  ["00_br", "00_bf", "00_bl", "00_bf"],
                "00_walk_front"  :  ["00_fr", "00_ff", "00_fl", "00_ff"],
            } 
        }
    },
                 
    
    "cave" : { 
        "filename" : "media/murs_maison.png", "kind" : "obstacles.map", "ppa" : True,
        "body" : { "mass" : 0.0  },
        "sprites" : {
            "left" : { "area" : (0, 2, 37, 37)},
            "bottom" : { "area" : (2, 78, 37, 37)},
            "right" : { "area" : (37, 2, 37, 37)},
            "top" : { "area" : (2, 41, 37, 37)},
            "floor" : { "area" : (74, 0, 39, 39), "layer" : 0, "kind" : "floor", "body" : None},
            "mid_v" : { "area" : (26, 2, 11, 37)},
            "mid_45" : { "area" : (41, 67, 54, 54),
                         "body" : { "filename" : "media/bodies/cave_mid_45.obj" }},
            "void" : { "area" : (113, 0, 39, 39), "kind" : "void"},
        },
    },
    
    "sporo_blue" : {"filename" : "media/sporo_charset.bmp", "kind": "entity.sporo.blue",
        "animations" : {
            "frames" : {
                "sb1" : (0, 0, 12, 12), "sb2" : (12, 0, 12, 12), "sb3" : (24, 0, 12, 12),
                "sb4" : (36, 0, 12, 12), "sb5" : (48, 0, 12, 12), "sb6" : (60, 0, 12, 12),
                "sb7" : (72, 0, 12, 12), "sb8" : (84, 0, 12, 12), "sb9" : (96, 0, 12, 12),
                "sb10" : (108, 0, 12, 12)
            },
            "clips" : {
                "loop"  :  ["sb%i" % i for i in range(1, 11)],
                "pulse" : ["sb%i" % i for i in range(1, 11)] + ["sb%i" % i for i in range(1, 11)][::-1]
            } 
        }
    },
}

with open("media/resources.json", "w") as f:
    json.dump(resources, f, ensure_ascii=True, separators=(',', ':'))
    


room_sprites = {
    "left":"left", "top":"top",
    "right":"right", "bottom":"bottom",
    "floor": "floor",
    "void": "void",
}

default_location = {"kind" : "absolute", "pos": (0, 0)}


def makeRoom(res, nb_w, nb_h, location=default_location, spr=room_sprites):
    _res_name = res
    #check the resource exists
    if res not in resources.keys():
        print "Error: cannot make a room. %s is not in the declared resources."
        return {}
    if not (spr.has_key("left") and spr.has_key("top") and \
            spr.has_key("right") and spr.has_key("left") and \
            spr.has_key("bottom") and spr.has_key("void") and spr.has_key("floor")):
        print "Error: cannot make a room. %s misses some important sprite keys !"
        return {}        
    
    res = resources[res]["sprites"]
    
    #get the sprite names
    get = lambda p : "%s_%s" % (_res_name, p)
    _l, _t, _r, _b = get("left"), get("top"), get("right"), get("bottom")
    _v, _f = get("void"), get("floor") 
    
    area = lambda name : Rect(res[name]["area"])
    #get the sprites area data
    _l_rect, _t_rect, _r_rect, _b_rect = area("left"), area("top"), area("right"), area("bottom")
    _v_rect, _f_rect = area("void"), area("floor")
    
    layer = 50
    
    #build the room sequence

    sequence = {
      "location" : location,
      "layer" : layer, "max_width" : nb_w, "block_size" : (_l_rect.width, _l_rect.height),
      "symbols" : ["_"] + [_t] * (nb_w - 2) + ["_"] + 
                  ([_l] + [_f] * (nb_w - 2) + [_r]) * (nb_h - 2) + \
                  ["_"] + [_b] * (nb_w - 2) + ["_"]
    }
       
    return [sequence]


#==============================================================    
#                       main map
#==============================================================    
sequences = makeRoom("cave", 45, 18, {"kind": "absolute", "pos": (55, 85)})

map_data = {
    
    'sequences' : sequences + [
       {
         "location" : {"kind": "absolute", "pos": (273, 419)},
         "layer" : 50, "max_width" : 1, "block_size" : (11, 37),
         "symbols" : ["cave_mid_v"] * 4
       },
       {
         "location" : {"kind": "relative", "pos": (111, -298)},
         "layer" : 50, "max_width" : 1, "block_size" : (11, 37),
         "symbols" : ["cave_mid_v"] * 4
       },
       {
         "location" : {"kind": "relative", "pos": (111, 298)},
         "layer" : 50, "max_width" : 1, "block_size" : (11, 37),
         "symbols" : ["cave_mid_v"] * 4
       },
       {
         "location" : {"kind": "relative", "pos": (111, -298)},
         "layer" : 50, "max_width" : 1, "block_size" : (11, 37),
         "symbols" : ["cave_mid_v"] * 4
       },
       {
         "location" : {"kind": "relative", "pos": (111, 298)},
         "layer" : 50, "max_width" : 1, "block_size" : (11, 37),
         "symbols" : ["cave_mid_v"] * 4
       },

    ],

    
    'free' : [
        #{"symbol": "cave_mid_45", "pos" : (451,367), "layer": 50},
        #{"symbol": "cave_mid_45", "pos" : (497,413), "layer": 50},     
    ]           
                   
  
}


#pprint(ship_data)


#with open("media/map_data.json", "w") as f:
#    json.dump(map_data, f, ensure_ascii=True, separators=(',',':'))
    
with open("media/scrolling_map_data.dump", "w") as f:
    cPickle.dump(map_data, f)

    
    


