#!/usr/bin/env python3

"""
This code contains the animation data for a animation of the metabolic proces in humans.

If you wish to create an animation for yourself you can read the animation doc string and
examenate the default animation data.

To use this animation data to create a animation you will need the project.py script, this scipt
will read the animation data and will render the animation.

Also you will need to install the program povray and the python3 packages vapory and pypovray
"""

__author__ = "Micha Beens"

__version__ = "1.0.0"

# Imports

import math
from vapory import Sphere, Camera, LightSource
from pypovray import models

# Functions
def get_animation_data(num=0, start_frame=0, sme_pos_ethanol=[[70, 0, 0], [0, 0, 0], [-70, 0, 0]],
                       ethanol_start_wacht = 0, ethanol_mid_wacht = -1, aldh_speed = 0, show_name = False):
    """
    Gets the data for the animation

    Needed data per object:
    - (String) Name object
    - (Bool) Molecule
        - True (bool) part of molecule {if true keyframes end position xyz becomes offset}
            - True (string) object to split
            - True (list) atoms to split {!!Current program only supports 1 atom split at a time!!}
                - (int) atom
            - False (file_path) pdb document
        - False (vapory components) components {!!These components are static and cant move!!}
    - (list) The frames of the end position
        - (int) frame
    - (list) The xyz end positions
        - (list) xyz end postions of the complement frame.
            - (int/float) x position
            - (int/float) y position
            - (int/float) z position

    Optional data per object:
    - (list) The frames of the rotation
        - (int) frame
    - (list) The rotation end positions
        - (list) rotation axes and radians to rotate of the complement frame
            - (list) rotation axes
                - (int/float) x axel (0-1)
                - (int/float) y axel (0-1)
                - (int/float) z axel (0-1)
            - (list) radians
                - (int/float) x axel
                - (int/float) y axel
                - (int/float) z axel
    - (list) The frames when object should be shown of not
        - (int) frame
    - (list) shown or not for the the complement frame
        - (bool) Should the object be shown
    """
    ethanol_shown = False
    if num == 0:
        ethanol_shown = True
        # Camera
        camera = {"name": "camera",
                  "molecule": [False, [0, 0, 100], [0, 0, 0]],
                  "keyframe_endpos_frames": [0, 30, 90, 140, 190, 250, 280],
                  "keyframe_endpos": [[[0, 0, 100], [0, 0, 0]],
                                      [[30, 0, 50], [30, 0, -10]],
                                      [[30, 0, 50], [30, 0, -10]],
                                      [[0, 0, 75], [0, 0, 0]],
                                      [[-30, 0, 50], [-30, 0, -10]],
                                      [[-30, 0, 50], [-30, 0, -10]],
                                      [[0, 0, 100], [0, 0, 0]],
                                      ],
                  }

        # Static vapory objects
        enzyme1 = {"name": "enzyme1",
                   "molecule": [False, Sphere([30, 0, -10], 4, models.default_sphere_model)],
                   "keyframe_endpos_frames": [0],
                   "keyframe_endpos": [[30, 0, -10],
                                       ],
                   }

        enzyme2 = {"name": "enzyme2",
                   "molecule": [False, Sphere([-30, 0, -10], 4, models.default_sphere_model)],
                   "keyframe_endpos_frames": [0],
                   "keyframe_endpos": [[-30, 0, -10],
                                       ],
                   }
    # Molecules step 1 (alcohol dehydrogenase)
    ethanol1_1 = {"name": "ethanol{}_1".format(num),
                  "molecule": [True, False, "pdb/ethanol2.pdb"],
                  "keyframe_endpos_frames": [20, 29, 30, 75, 90, 140, 141, 190, 205, 250],
                  "keyframe_endpos": [[sme_pos_ethanol[0][0]+10, sme_pos_ethanol[0][1], sme_pos_ethanol[0][2]],
                                      sme_pos_ethanol[0],
                                      sme_pos_ethanol[0],
                                      [30, 0, 0],
                                      [30, 0, 0, "join", False, "h_movement{}_1".format(num)],
                                      sme_pos_ethanol[1],
                                      sme_pos_ethanol[1],
                                      [-30, 0, 0],
                                      [-30, 0, 0, "join", False, "water{}_3".format(num)],
                                      sme_pos_ethanol[2],
                                      ],
                  "keyframe_rotation_frames":[29, 30, 75, 90, 140, 141, 190, 205, 250, 500],
                  "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[0, 0, 0], [0, 0, 0]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[0, 0, 0], [0, 0, 0]],
                                       [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                       [[1, 1, 1], [math.pi*8, math.pi*8, math.pi*8]],
                                       ],
                  "keyframe_shown_frames": [0-start_frame, 0, 250],
                  "keyframe_shown": [ethanol_shown, True, True],
                  }

    water1_1 = {"name": "water{}_1".format(num),
                "molecule": [True, False, "pdb/water.pdb"],
                "keyframe_endpos_frames": [30, 75, 90, 140],
                "keyframe_endpos": [[-30, -70, 0],
                                    [30, -7.5, 0],
                                    [30, -7.5, 0, "join", False, "waterstof{}_1".format(num)],
                                    [70, -70, 0],
                                    ],
                "keyframe_rotation_frames":[30, 75, 90, 140],
                "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                     [[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]]
                                     ],
                "keyframe_shown_frames": [0, 140],
                "keyframe_shown": [True, False],
                }

    nad1_1 = {"name": "NAD{}_1".format(num),
              "molecule": [True, False, "pdb/NAD.pdb"],
              "keyframe_endpos_frames": [30, 75, 90, 140],
              "keyframe_endpos": [[-30, 70, 0],
                                  [20, 7.5, 0],
                                  [20, 7.5, 0, "join", False, "h_movement_nad{}_1".format(num), "hNAD{}_1".format(num)],
                                  [70, 70, 0],
                                  ],
              "keyframe_rotation_frames": [30, 75, 90, 140],
              "keyframe_rotation": [[[0, 0, 0], [0, 0, 0]],
                                    [[1, 1, 1], [math.pi, 1.5, 0]],
                                    [[0, 0, 0], [0, 0, 0]],
                                    [[1, 1, 1], [math.pi, math.pi*2, math.pi]],
                                    ],
              "keyframe_shown_frames": [0, 140],
              "keyframe_shown": [True, False],
              }

    waterstof1_1 = {"name": "waterstof{}_1".format(num),
                    "molecule": [True, True, "ethanol{}_1".format(num), [3]],
                    "keyframe_endpos_frames": [75, 90],
                    "keyframe_endpos": [[0, 0, 0],
                                        [-0.3, -5.5, -0.2],
                                        ],
                    "keyframe_shown_frames": [0, 90],
                    "keyframe_shown": [True, False],
                    }

    hnad1_1 = {"name": "hNAD{}_1".format(num),
               "molecule": [True, True, "ethanol{}_1".format(num), [8]],
               "keyframe_endpos_frames": [75, 90],
               "keyframe_endpos": [[0, 0, 0],
                                   [-6, 2.7, -1.5],
                                   ],
               "keyframe_shown_frames": [0, 90],
               "keyframe_shown": [True, False],
               }

    h_movement1_1 = {"name": "h_movement{}_1".format(num),
                     "molecule": [True, True, "ethanol{}_1".format(num), [4]],
                     "keyframe_endpos_frames": [75, 90],
                     "keyframe_endpos": [[0, 0, 0],
                                         [0.1, -0.3, 0.8],
                                         ],
                     "keyframe_shown_frames": [0, 90],
                     "keyframe_shown": [True, False],
                     }

    h_movement_nad1_1 = {"name": "h_movement_nad{}_1".format(num),
                         "molecule": [True, True, "NAD{}_1".format(num), [64]],
                         "keyframe_endpos_frames": [75, 90],
                         "keyframe_endpos": [[0, 0, 0],
                                           [-0.3, 0.2, -0.9],
                                           ],
                         "keyframe_shown_frames": [0, 90],
                         "keyframe_shown": [True, False],
                         }

    # Molecules step 2 (ethanal dehydrogenase)
    nad1_2 = {"name": "NAD{}_2".format(num),
               "molecule": [True, False, "pdb/NAD.pdb"],
               "keyframe_endpos_frames": [145, 190, 205, 260],
               "keyframe_endpos": [[-90, 70, 0],
                                   [-40, 7.5, 0],
                                   [-40, 7.5, 0, "join", False, "h_movement_nad{}_2".format(num), "hNAD{}_2".format(num)],
                                   [10, 70, 0],
                                   ],
               "keyframe_rotation_frames": [145, 190, 205, 260],
               "keyframe_rotation": [[[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi, 1.5, 0]],
                                     [[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi, math.pi*2, math.pi]],
                                     ],
               "keyframe_shown_frames": [0, 145, 250],
               "keyframe_shown": [False, True, False],
               }

    water1_2 = {"name": "water{}_2".format(num),
                "molecule": [True, False, "pdb/water.pdb"],
                "keyframe_endpos_frames": [145, 190, 205, 260],
                "keyframe_endpos": [[-90, -70, 0],
                                    [-30, -7.5, 0],
                                    [-30, -7.5, 0, "join", False, "waterstof{}_2".format(num)],
                                    [30, -70, 0],
                                    ],
                "keyframe_rotation_frames":[145, 190, 205, 260],
                "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                     [[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]]
                                     ],
                "keyframe_shown_frames": [0, 145, 250],
                "keyframe_shown": [False, True, False],
                }

    water1_3 = {"name": "water{}_3".format(num),
                "molecule": [True, False, "pdb/water.pdb"],
                "keyframe_endpos_frames": [145, 190, 205, 260],
                "keyframe_endpos": [[-90, -70, 0],
                                    [-35, -2, 0],
                                    [-31, -2.2, 0.2],
                                    [30, -70, 0],
                                    ],
                "keyframe_rotation_frames":[145, 190, 205],
                "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                     [[1, 1, 1], [math.pi*2, math.pi*2, math.pi]],
                                     [[1, 0, 0], [1, 0, 0]],
                                     ],
                "keyframe_shown_frames": [0, 145, 205],
                "keyframe_shown": [False, True, False],
                }

    waterstof1_2 = {"name": "waterstof{}_2".format(num),
                    "molecule": [True, True, "ethanol{}_1".format(num), [6]],
                    "keyframe_endpos_frames": [190, 205],
                    "keyframe_endpos": [[0, 0, 0],
                                        [-0.3, -5.5, -0.2],
                                        ],
                    "keyframe_shown_frames": [190, 205],
                    "keyframe_shown": [True, False],
                    }

    hnad1_2 = {"name": "hNAD{}_2".format(num),
               "molecule": [True, True, "water{}_3".format(num), [2]],
               "keyframe_endpos_frames": [190, 205],
               "keyframe_endpos": [[0, 0, 0],
                                   [-1.8, 5.8, 0],
                                   ],
               "keyframe_shown_frames": [190, 205],
               "keyframe_shown": [True, False],
               }

    h_movement_nad1_2 = {"name": "h_movement_nad{}_2".format(num),
                         "molecule": [True, True, "NAD{}_2".format(num), [64]],
                         "keyframe_endpos_frames": [190, 205],
                         "keyframe_endpos": [[0, 0, 0],
                                             [-0.3, 0.2, -0.9],
                                             ],
                         "keyframe_shown_frames": [190, 205],
                         "keyframe_shown": [True, False],
                         }

    if num == 0:
        animation_objects = {"camera": camera,
                             # Static vapory objects
                             "enzyme1": enzyme1,
                             "enzyme2": enzyme2,
                             # molecules step 1
                             "ethanol{}_1".format(num): ethanol1_1,
                             "water{}_1".format(num): water1_1,
                             "NAD{}_1".format(num): nad1_1,
                             "waterstof{}_1".format(num): waterstof1_1,
                             "hNAD{}_1".format(num): hnad1_1,
                             "h_movement{}_1".format(num): h_movement1_1,
                             "h_movement_nad{}_1".format(num): h_movement_nad1_1,
                             # molecules step 2
                             "NAD{}_2".format(num): nad1_2,
                             "water{}_2".format(num): water1_2,
                             "water{}_3".format(num): water1_3,
                             "waterstof{}_2".format(num): waterstof1_2,
                             "hNAD{}_2".format(num): hnad1_2,
                             "h_movement_nad{}_2".format(num): h_movement_nad1_2,
                             }
    else:
        animation_objects = {# molecules step 1
                             "ethanol{}_1".format(num): ethanol1_1,
                             "water{}_1".format(num): water1_1,
                             "NAD{}_1".format(num): nad1_1,
                             "waterstof{}_1".format(num): waterstof1_1,
                             "hNAD{}_1".format(num): hnad1_1,
                             "h_movement{}_1".format(num): h_movement1_1,
                             "h_movement_nad{}_1".format(num): h_movement_nad1_1,
                             # molecules step 2
                             "NAD{}_2".format(num): nad1_2,
                             "water{}_2".format(num): water1_2,
                             "water{}_3".format(num): water1_3,
                             "waterstof{}_2".format(num): waterstof1_2,
                             "hNAD{}_2".format(num): hnad1_2,
                             "h_movement_nad{}_2".format(num): h_movement_nad1_2,
                             }

    for obj in animation_objects:

        if show_name and not obj == "camera":
            animation_objects[obj]["show_name"] = True
        else:
            animation_objects[obj]["show_name"] = False

        if try_dict_keys(animation_objects[obj], "keyframe_endpos_frames"):
            for frame in range(len(animation_objects[obj]["keyframe_endpos_frames"])):
                animation_objects = add_multipliers(obj, frame, animation_objects, "keyframe_endpos_frames", start_frame, ethanol_start_wacht, ethanol_mid_wacht, aldh_speed)

        if try_dict_keys(animation_objects[obj], "keyframe_rotation_frames"):
            for frame in range(len(animation_objects[obj]["keyframe_rotation_frames"])):
                animation_objects = add_multipliers(obj, frame, animation_objects, "keyframe_rotation_frames", start_frame, ethanol_start_wacht, ethanol_mid_wacht, aldh_speed)

        if try_dict_keys(animation_objects[obj], "keyframe_shown_frames"):
            for frame in range(len(animation_objects[obj]["keyframe_shown_frames"])):
                animation_objects = add_multipliers(obj, frame, animation_objects, "keyframe_shown_frames", start_frame, ethanol_start_wacht, ethanol_mid_wacht, aldh_speed)
                
    return animation_objects

def try_dict_keys(dictionary, key):
    try:
        dictionary[key]
        return True
    except:
        return False

def add_multipliers( obj, frame, animation_objects, key, start_frame, ethanol_start_wacht, ethanol_mid_wacht, aldh_speed):
    # Add start_frame, ethanol_start_wacht, ethanol_mid_wacht and ALDH speed
    if animation_objects[obj][key][frame] >= 190:
        animation_objects[obj][key][frame] += start_frame + ethanol_start_wacht + ethanol_mid_wacht + aldh_speed

    # Add start_frame, ethanol_start_wacht and ethanol_mid_wacht
    elif animation_objects[obj][key][frame] >= 141:
        animation_objects[obj][key][frame] += start_frame + ethanol_start_wacht + ethanol_mid_wacht

    # Add start_frame and ethanol_start_wacht
    elif animation_objects[obj][key][frame] >= 30:
        animation_objects[obj][key][frame] += start_frame + ethanol_start_wacht

    # Add start_frame
    else:
        animation_objects[obj][key][frame] += start_frame

    return animation_objects
