
import json
#from random import choice , sample, randint   
#from pygame.rect import Rect
#from pprint import pprint
#import itertools

import cPickle

resources = { 
                                   
    "renard" : {"filename" : "media/renard.png", "kind" : "main.characters",
         #pour le body bounding rect car pas de mesh
        "body" : { "mass" : 10.0, "type" : "dynamic", "area" : (5, 2, 38, 50) },
        "animations" : {
            "frames" : {
                "00_bl" : (0, 103, 44, 53), "00_bf" : (44, 103, 42, 53), "00_br" : (86, 103, 49, 53),
                "00_rl" : (0, 53, 47, 50), "00_rf" : (47, 53, 49, 50), "00_rr" : (96, 53, 47, 50),
                "00_fl" : (0, 0, 41, 53), "00_ff" : (41, 0, 40, 53), "00_fr" : (81, 0, 45, 53),
                "00_ll" : (0, 156, 47, 50), "00_lf" : (47, 156, 49, 50), "00_lr" : (96, 156, 47, 50),
            },
            "clips" : {
                "00_walk_right"  :  ["00_rr", "00_rf", "00_rl", "00_rf"],
                "00_walk_left"  :  ["00_lr", "00_lf", "00_ll", "00_lf"],
                "00_walk_back"  :  ["00_br", "00_bf", "00_bl", "00_bf"],
                "00_walk_front"  :  ["00_fr", "00_ff", "00_fl", "00_ff"],
            } 
        }
    },
             
    "poulailler" : {
        "filename" : "media/poulailler.png", "kind" : "obstacles.map",
        "body" : None,
        "sprites" : {
            #"barraque_A" :  {"area" : (0, 0, 174, 80), "body" : { "area" : (20, 290, 40, 50)}},
            #"barraque_B" :  {"area" : (24, 80, 174, 43), "body" : { "area" : (0, 0, 500, 1)}},
            
            "terrain" : { "area" : (70, 215, 50, 20), "body" : None},
            "terrain_vide" : { "area" : (70, 236, 24, 20), "body" : None},
            "trou" : {"area": (210, 215, 50, 20), "body": None},
            "navet" : {"area" : (142, 184, 23, 29), "body" : {"type" : "dynamic", "mass" : 500.0} },
            "carotte" : {"area" : (122, 179, 12, 35), "body" : {"type" : "dynamic", "mass" : 500.0} },
        }    
    },
                 
    
    "pan" : { 
        "filename" : "media/panneaux.png", "kind" : "obstacles.map",
        "body" : { "mass" : 0.0 , "area" : (0, 0, 69, 1) },
        "sprites" : {
                     
            #========  UP  ==========         
            #"pt_corde_A" : { "area" : (2, 0, 5, 52)},
            "N1_A" : { "area" : (7, 0, 64, 20), "body" : None},
            "pt_A" : { "area" : (71, 0, 5, 20), "body" : None},
            "N2_A" : { "area" : (76, 0, 64, 20), "body" : None},
            #"floor_A" : { "area" : (16, 64, 32, 26), "layer" : 0, "kind" : "floor", "body" : None},
            #"S1_A" : { "area" : (7, 108, 64, 52)},
            #"S2_A" : { "area" : (76, 108, 64, 52)},
                     
            #========  DOWN  ==========    
            "N1_B" : { "area" : (7, 20, 64, 32), },
            "pt_B" : { "area" : (71, 20, 5, 32)},
            "N2_B" : { "area" : (76, 20, 64, 32)},

        },
    },
    

}

with open("media/resources.json", "w") as f:
    json.dump(resources, f, ensure_ascii=True, separators=(',', ':'))
    


#==============================================================    
#                       main map
#==============================================================    

map_data = {
    
    'sequences' : [
                   
       {
         "location" : {"kind": "absolute", "pos": (0, 0)},
         "layer" : 90,
         "symbols" :(["poulailler_terrain_vide"] * 3 + ["poulailler_terrain"] * 9 + ["poulailler_terrain_vide"] * 2 + ["poulailler_terrain"] * 10 + ["+"]) * 32 
       },
                   
                   
       {
         "location" : {"kind": "absolute", "pos": (-90, 14)},
         "layer" : 150,
         "symbols" : ["pan_pt_A", "pan_N2_A", "pan_N1_A", "pan_N2_A", "pan_pt_A", "pan_N1_A"] * 5 
       },
       {
         "location" : {"kind": "cardinal", "pos": "south"},
         "layer" : 95,
         "symbols" : ["pan_pt_B", "pan_N2_B", "pan_N1_B", "pan_N2_B", "pan_pt_B", "pan_N1_B"] * 5 
       },
                   
        {
         "location" : {"kind": "absolute", "pos": (-90, 580)},
         "layer" : 150,
         "symbols" : ["pan_pt_A", "pan_N1_A", "pan_N2_A", "pan_pt_A", "pan_N2_A", "pan_N1_A", "pan_N2_A", ] * 5 
       },
       {
         "location" : {"kind": "cardinal", "pos": "south"},
         "layer" : 95,
         "symbols" : ["pan_pt_B", "pan_N1_B", "pan_N2_B", "pan_pt_B", "pan_N2_B", "pan_N1_B", "pan_N2_B" ] * 5 
       },

    ],

    
    'free' : [
        #{"symbol": "poulailler_barraque_A", "pos" : (431, 200), "layer": 150},
        #{"symbol": "poulailler_barraque_B", "pos" : (455, 280), "layer": 49},

        #{"symbol": "cave_mid_45", "pos" : (497, 413), "layer": 50},
    ]           
                   
  
}


#pprint(ship_data)


#with open("media/map_data.json", "w") as f:
#    json.dump(map_data, f, ensure_ascii=True, separators=(',',':'))
    
with open("media/map_data.dump", "w") as f:
    cPickle.dump(map_data, f)


    
    


