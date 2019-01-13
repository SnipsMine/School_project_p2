#!/usr/bin/env python3

"""
This program creates a series of frames that can be combined to form a animation
of the metabolic poroces of ethanol in humans.

Current functions:
- Create a molecule from a pbb file.
- Move molecules from start position to end position
- Split atoms form larger molecules
- Move the atoms to offset
- Create basic vapory objects
- Joining multiple molecules together into one molecule
- Rotation of molecules (only with single core renders)

Upcomming functions:
- Rotation of molecules with multi core render support
- Stop showing objects
- Start showing objects (currently all objects are always shown)
- Reading the animation data from a .micdes animation file
- Add support for splits with multiple atoms at a time
- Add support for moving vapory objects.

Known bugs:
- After splitting a molecule the molecule auto centers itself. This couses the molecule to moves a
  bit.
"""

__author__ = "Micha Beens"

__version__ = "1.0.0"

# Imports
import sys
import math
from vapory import Sphere, Camera, LightSource, Scene
from pypovray import pypovray, models, pdb


# Globals
MOLECULES = None
ANIMATION_OBJECTS = None


# Functions
def get_animation_data():
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

    global ANIMATION_OBJECTS

    # Camera
    camera = {"name": "camera",
              "molecule": [False, Camera("lokation", [0, 0, 100], "look_at", [0, 0, 0])],
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
    ethanol1 = {"name": "ethanol1",
               "molecule": [True, False, "pdb/ethanol2.pdb"],
               "keyframe_endpos_frames": [30, 75, 90, 140, 190, 205, 250],
               "keyframe_endpos": [[70, 0, 0],
                                   [30, 0, 0],
                                   [30, 0, 0, "join", False, "h_movement1"],
                                   [0, 0, 0],
                                   [-30, 0, 0],
                                   [-30, 0, 0, "join", False, "water3"],
                                   [-70, 0, 0]
                                   ],
               "keyframe_rotation_frames":[30, 75, 90, 140, 190, 205, 260],
               "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                    [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                    [[0, 0, 0], [0, 0, 0]],
                                    [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                    [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                    [[0, 0, 0], [0, 0, 0]],
                                    [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                    ],
               }

    water1 = {"name": "water1",
             "molecule": [True, False, "pdb/water.pdb"],
             "keyframe_endpos_frames": [30, 75, 90, 150],
             "keyframe_endpos": [[-30, -70, 0],
                                 [30, -7.5, 0],
                                 [30, -7.5, 0, "join", False, "waterstof1"],
                                 [70, -70, 0],
                                 ],
             "keyframe_rotation_frames":[30, 75, 90, 150],
             "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                  [[0, 0, 0], [0, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]]
                                  ],
             }

    nad1 = {"name": "NAD1",
           "molecule": [True, False, "pdb/NAD.pdb"],
           "keyframe_endpos_frames": [30, 75, 90, 150],
           "keyframe_endpos": [[-30, 70, 0],
                               [20, 7.5, 0],
                               [20, 7.5, 0, "join", False, "h_movement_nad1", "hNAD1"],
                               [70, 70, 0],
                               ],
           "keyframe_rotation_frames": [30, 75, 90, 150],
           "keyframe_rotation": [[[0, 0, 0], [0, 0, 0]],
                                 [[1, 1, 1], [math.pi, 1.5, 0]],
                                 [[0, 0, 0], [0, 0, 0]],
                                 [[1, 1, 1], [math.pi, math.pi*2, math.pi]],
                                 ],
           }

    waterstof1 = {"name": "waterstof1",
                 "molecule": [True, True, "ethanol1", [3]],
                 "keyframe_endpos_frames": [75, 90],
                 "keyframe_endpos": [[0, 0, 0],
                                     [-0.3, -5.5, -0.2],
                                     ],
                  "keyframe_shown_frames": [0, 90],
                  "keyframe_shown": [True, False]
                 }

    hnad1 = {"name": "hNAD1",
            "molecule": [True, True, "ethanol1", [8]],
            "keyframe_endpos_frames": [75, 90],
            "keyframe_endpos": [[0, 0, 0],
                                [-6, 2.7, -1.5],
                                ],
            "keyframe_shown_frames": [0, 90],
            "keyframe_shown": [True, False]
            }

    h_movement1 = {"name": "h_movement1",
                  "molecule": [True, True, "ethanol1", [4]],
                  "keyframe_endpos_frames": [75, 90],
                  "keyframe_endpos": [[0, 0, 0],
                                      [0.1, -0.3, 0.8],
                                      ],
                  "keyframe_shown_frames": [0, 90],
                  "keyframe_shown": [True, False]
                  }

    h_movement_nad1 = {"name": "h_movement_nad1",
                      "molecule": [True, True, "NAD1", [64]],
                      "keyframe_endpos_frames": [75, 90],
                      "keyframe_endpos": [[0, 0, 0],
                                        [-0.3, 0.2, -0.9],
                                        ],
                      "keyframe_shown_frames": [0, 90],
                      "keyframe_shown": [True, False]
                      }

    # moleculen stap 2 (ethanal dehydrogenase)
    nad2 = {"name": "NAD2",
           "molecule": [True, False, "pdb/NAD.pdb"],
           "keyframe_endpos_frames": [145, 190, 205, 260],
           "keyframe_endpos": [[-90, 70, 0],
                               [-40, 7.5, 0],
                               [-40, 7.5, 0, "join", False, "h_movement_nad2", "hNAD2"],
                               [10, 70, 0],
                               ],
           "keyframe_rotation_frames": [145, 190, 205, 260],
           "keyframe_rotation": [[[0, 0, 0], [0, 0, 0]],
                                 [[1, 1, 1], [math.pi, 1.5, 0]],
                                 [[0, 0, 0], [0, 0, 0]],
                                 [[1, 1, 1], [math.pi, math.pi*2, math.pi]],
                                 ],
           }

    water2 = {"name": "water2",
             "molecule": [True, False, "pdb/water.pdb"],
             "keyframe_endpos_frames": [145, 190, 205, 260],
             "keyframe_endpos": [[-90, -70, 0],
                                 [-30, -7.5, 0],
                                 [-30, -7.5, 0, "join", False, "waterstof2"],
                                 [30, -70, 0],
                                 ],
             "keyframe_rotation_frames":[145, 190, 205, 260],
             "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]],
                                  [[0, 0, 0], [0, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]]
                                  ],
             }
    water3 = {"name": "water3",
             "molecule": [True, False, "pdb/water.pdb"],
             "keyframe_endpos_frames": [145, 190, 205, 260],
             "keyframe_endpos": [[-90, -70, 0],
                                 [-35, -2, 0],
                                 [-31, -2.2, 0.2],
                                 [30, -70, 0],
                                 ],
             "keyframe_rotation_frames":[145, 190, 205, 260],
             "keyframe_rotation":[[[0, 0, 0], [0, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi]],
                                  [[1, 0, 0], [1, 0, 0]],
                                  [[1, 1, 1], [math.pi*2, math.pi*2, math.pi*2]]
                                  ],
             }

    waterstof2 = {"name": "waterstof2",
                 "molecule": [True, True, "ethanol1", [6]],
                 "keyframe_endpos_frames": [190, 205],
                 "keyframe_endpos": [[0, 0, 0],
                                     [-0.3, -5.5, -0.2],
                                     ],
                  }

    hnad2 = {"name": "hNAD1",
            "molecule": [True, True, "water3", [2]],
            "keyframe_endpos_frames": [190, 205],
            "keyframe_endpos": [[0, 0, 0],
                                [-1.8, 5.8, 0],
                                ],
            }

    h_movement_nad2 = {"name": "h_movement_nad2",
                      "molecule": [True, True, "NAD2", [64]],
                      "keyframe_endpos_frames": [190, 205],
                      "keyframe_endpos": [[0, 0, 0],
                                        [-0.3, 0.2, -0.9],
                                        ],
                      }

    ANIMATION_OBJECTS = {"camera": camera,
                         # Static vapory objects
                         "enzyme1": enzyme1,
                         "enzyme2": enzyme2,
                         # moleculen stap 1
                         "ethanol1": ethanol1,
                         "water1": water1,
                         "NAD1": nad1,
                         "waterstof1": waterstof1,
                         "hNAD1": hnad1,
                         "h_movement1": h_movement1,
                         "h_movement_nad1": h_movement_nad1,
                         #moleculen stap 2
                         "NAD2": nad2,
                         "water2": water2,
                         "water3": water3,
                         "waterstof2": waterstof2,
                         "hNAD2": hnad2,
                         "h_movement_nad2": h_movement_nad2,
                         }


def make_molecules(molecules):
    """
    make_molecules([frame, molecules])
    """
    sorted_animation_objects = sort_molecules()

    for obj in sorted_animation_objects:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]

        if molecule_data[0] and not molecule_data[1]:
            # Making normal molecules from pdb file
            molecule = pdb.PDBMolecule(molecule_data[2], center=True)

        elif not molecule_data[0]:
            # Making basic vapory objects
            molecule = molecule_data[1:]

        elif molecule_data[0] and molecule_data[1]:
            # Make the molecule a None object until it is time to split the moleucle
            molecule = None

        molecules[obj] = molecule
    return molecules


def sort_molecules():
    """
    Sorts the animaion objects so that there are no split errors happen
    """
    sorted_animation_objects = []

    special_object_list = []

    for obj in ANIMATION_OBJECTS:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        if molecule_data[0] and molecule_data[1]:
            # Molecuels that have to be created bij spliting bigger molecules
            molecule_name = obj
            mother_molecule = ANIMATION_OBJECTS[obj]["molecule"][2]
            split_atom = ANIMATION_OBJECTS[obj]["molecule"][3]
            special_object_list.append([molecule_name, mother_molecule, split_atom])
        else:
            # Objects that do not need to be split
            sorted_animation_objects.append(obj)

    # Get a list of mother molecules from the special object list
    mother_list = list(set([special_object_list[index][1]
                            for index in range(len(special_object_list))]))

    for mother in mother_list:
        high_2_low = get_highest(mother, special_object_list, [])
        print("SORTED:", high_2_low)
        for obj in high_2_low:
            if not obj in sorted_animation_objects:
                sorted_animation_objects.append(obj)

    # Print objects in sorter for debugging
    for obj in sorted_animation_objects:
        #print("DEBUG:", obj)
        pass

    return sorted_animation_objects


def get_highest(mother, object_list, high_2_low):
    """outputs a list from high to low"""
    highest = -1
    highest_molecule = ""
    for obj in object_list:
        if obj[1] == mother and obj[2][0] > highest:
            highest = obj[2][0]
            highest_molecule = obj[0]

    high_2_low.append(highest_molecule)
    object_list.pop(object_list.index([highest_molecule, mother, [highest]]))

    if is_mother_in_list(mother, object_list):
        get_highest(mother, object_list, high_2_low)

    return  high_2_low


def is_mother_in_list(mother, object_list):
    """Outputs a bool to see if there are objects with te same mother"""
    output = False
    for obj in object_list:
        if mother in obj:
            output = True
            break
    return output


def calculate_distance(frames, ends, step, molecule_start, offset=False):
    """Calculates the step size for the movement"""

    distance_list = []

    time = frames[1] - frames[0]
    
    for index, start in enumerate(molecule_start):
        if offset:
            end = ends[index]
        else:
            end = ends[index] - start
        distance = start + end / time * (step - frames[0])
        distance_list.append(distance)

    return distance_list


def calculate_radians(frames, ends):
    """Calculates how many radians must be moved per step"""
    time = frames[1] - frames[0]
    radians_list = []
    for end in ends:
        radians = end / time
        radians_list.append(radians)
    return radians_list


def molecule_maker(mol1, mol2, name):
    """Combines two molecules into one"""
    combo = mol1.atoms
    while len(mol2.atoms) > 0:
        combo += [mol2.atoms.pop(0)]
    final_combo = pdb.PDBMolecule(name, atoms=combo, center=False)
    final_combo.render_molecule()
    return final_combo


def move_objects(obj, step, mother=False):
    global MOLECULES
    
    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_endpos_frames"]
    keyframe_endpos_data = ANIMATION_OBJECTS[obj]["keyframe_endpos"]

    for frame in range(len(keyframe_frames_data)):
        if frame != 0 and step in [val for val in range(keyframe_frames_data[frame-1]+1,
                                                        keyframe_frames_data[frame]+1)]:
            # move the object to the place equevelent to the step
            print("(move) if:", obj)
            if molecule_data[0] and molecule_data[1]:
                
                start_pos = MOLECULES[obj]["start"].copy()
                for index in range(frame):
                    start_pos[0] += keyframe_endpos_data[index][0]
                    start_pos[1] += keyframe_endpos_data[index][1]
                    start_pos[2] += keyframe_endpos_data[index][2]
                
                distance = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                              keyframe_endpos_data[frame],
                                              step,
                                              start_pos,
                                              True)

                MOLECULES[obj]["molecule"].move_to(list(distance))
                
            elif mother and step != keyframe_frames_data[frame]:
                MOLECULES[obj].move_to(keyframe_endpos_data[frame-1])

            elif molecule_data[0]:
                distance = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                              keyframe_endpos_data[frame][:3],
                                              step,
                                              keyframe_endpos_data[frame-1][:3])

                MOLECULES[obj].move_to(list(distance))

            elif not molecule_data[0]:
                if obj == "camera":
                    location = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                                  keyframe_endpos_data[frame][0][:3],
                                                  step,
                                                  keyframe_endpos_data[frame-1][0][:3])

                    look_at = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                                  keyframe_endpos_data[frame][1][:3],
                                                  step,
                                                  keyframe_endpos_data[frame-1][1][:3])

                    MOLECULES[obj] = [location, look_at]

            # if molecules need to be joined
            if step == keyframe_frames_data[frame] and try_dict_keys(keyframe_endpos_data[frame], 3) and not mother and not keyframe_endpos_data[frame][4]:
                for mol in range(5, 5+len(keyframe_endpos_data[frame][5:])):
                    print("join {} and {} at frame {}".format(obj, keyframe_endpos_data[frame][mol], step))
                    # Set the molecules that is
                    move_objects(keyframe_endpos_data[frame][mol], step)
                    if ANIMATION_OBJECTS[keyframe_endpos_data[frame][mol]]["molecule"][1]:
                        MOLECULES[obj] = molecule_maker(MOLECULES[obj], MOLECULES[keyframe_endpos_data[frame][mol]]["molecule"], obj)
                    else:
                        MOLECULES[obj] = molecule_maker(MOLECULES[obj], MOLECULES[keyframe_endpos_data[frame][mol]], obj)
                    keyframe_endpos_data[frame][4] = True
            break

        elif frame == 0 and step <= keyframe_frames_data[frame]:
            # if true move objects to start position and go to the next molecule
            print("(move) elif1:", obj)
            #print(MOLECULES[obj])
            if molecule_data[0] and not molecule_data[1]:
                MOLECULES[obj].move_to(keyframe_endpos_data[frame])
            elif obj == "camera":
                MOLECULES[obj] = [keyframe_endpos_data[frame][0], keyframe_endpos_data[frame][1]]
            break

        elif molecule_data[0] and molecule_data[1]:
            # If the other statment are false do this
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("(move) elif2:", obj)
            distance = MOLECULES[obj]["start"].copy()
            for index in range(frame+1):
                distance += keyframe_endpos_data[index]
            MOLECULES[obj]["molecule"].move_to(distance)

        elif molecule_data[0]:
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("(move) elif3:", obj)
            MOLECULES[obj].move_to(keyframe_endpos_data[frame][:3])
            
            # if molecules need to be joined
            if step >= keyframe_frames_data[frame] and try_dict_keys(keyframe_endpos_data[frame], 3) and not mother and not keyframe_endpos_data[frame][4]:
                for mol in range(5, 5+len(keyframe_endpos_data[frame][5:])):
                    print("join {} and {} at frame {}".format(obj, keyframe_endpos_data[frame][mol], keyframe_frames_data[frame]))
                    # Set the molecules that is
                    move_objects(keyframe_endpos_data[frame][mol], keyframe_frames_data[frame])
                    MOLECULES[obj] = molecule_maker(MOLECULES[obj], MOLECULES[keyframe_endpos_data[frame][mol]]["molecule"], obj)
                    keyframe_endpos_data[frame][4] = True

        else:
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("(move) else: {}".format(obj))
            if obj == "camera":
                MOLECULES[obj] = [keyframe_endpos_data[frame][0], keyframe_endpos_data[frame][1]]

def rotate_objects(obj, step, mother=False):
    rotate_frames_data = ANIMATION_OBJECTS[obj]["keyframe_rotation_frames"]
    rotate_endpos_data = ANIMATION_OBJECTS[obj]["keyframe_rotation"]

    for frame in range(len(rotate_frames_data)):
        # Calculate the start rotation of the molecule

        if frame != 0 and step in [val for val in range(rotate_frames_data[frame-1]+1,
                                                        rotate_frames_data[frame]+1)]:

            print("(rotate) if: {}".format(obj))
            # rotate the object to the place equevelent to the step
            if mother:
                radians = calculate_radians([rotate_frames_data[frame-1], rotate_frames_data[frame]],
                                             rotate_endpos_data[frame][1],
                                             )

                MOLECULES[obj].rotate([1, 1, 1], [radians[0]*-1, radians[1]*-1, radians[2]*-1])
                
            else:
                radians = calculate_radians([rotate_frames_data[frame-1], rotate_frames_data[frame]],
                                            rotate_endpos_data[frame][1],
                                            )
                
                MOLECULES[obj].rotate([1, 1, 1], radians)
            break

    return

def shown_objects(obj, step, render_list):
    shown_frames_data = ANIMATION_OBJECTS[obj]["keyframe_shown_frames"]
    shown_bool_data = ANIMATION_OBJECTS[obj]["keyframe_shown"]
    for frame in range(len(shown_frames_data)):
        if frame != 0 and step < shown_frames_data[frame] and shown_bool_data[frame-1]:
            print("(shown) if: {}".format(obj))
            render_list = put_object_in_render_list(obj, render_list)
            break
        
        elif frame == 0 and step <= shown_frames_data[frame] and shown_bool_data[frame]:
            print("(shown) elif1: {}".format(obj))
            render_list = put_object_in_render_list(obj, render_list)
            break
        
        elif shown_frames_data[frame] == shown_frames_data[-1] and step > shown_frames_data[frame] and shown_bool_data[frame]:
            print("(shown) elif2: {}".format(obj))
            render_list = put_object_in_render_list(obj, render_list)
            break
        else:
            if shown_frames_data[frame] == shown_frames_data[-1]:
                print("(shown) else: {} (object not shown)".format(obj))
            

            
    return render_list

def put_object_in_render_list(obj, render_list):
    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    if molecule_data[0] and molecule_data[1]:
        render_list = render_list + MOLECULES[obj]["molecule"].povray_molecule
    elif molecule_data[0]:
        render_list = render_list + MOLECULES[obj].povray_molecule
    elif not obj == "camera":
        render_list = render_list + MOLECULES[obj]
    return render_list
    

def try_dict_keys(dictionary, key):
    try:
        dictionary[key]
        return True
    except:
        return False

def make_frame(step):
    global MOLECULES
    
    # Basic objects for the scene
    cam = Camera("location", [0, 0, 100], "look_at", [0, 0, 0])
    light = LightSource([0, 0, 100], 1)
    render_list = [light]

    print("frame:{}----------------------------------------------------------------".format(step))

    # Is there another None molecule that needs to be created.
    for obj in MOLECULES:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_endpos_frames"]
        if MOLECULES[obj] is None and step >= keyframe_frames_data[0]:
            
            # Set the mother molecule on the start position of split.
            move_objects(ANIMATION_OBJECTS[molecule_data[2]]["name"], keyframe_frames_data[0], True)

            # Set the mother molecule on the start rotation of split.
            if try_dict_keys(ANIMATION_OBJECTS[ANIMATION_OBJECTS[molecule_data[2]]["name"]], "keyframe_rotation_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[ANIMATION_OBJECTS[molecule_data[2]]["name"]], "keyframe_rotation"):
                rotate_objects(ANIMATION_OBJECTS[molecule_data[2]]["name"], step)
                
            # Call make molecules to split the molecule
            split_molecule = MOLECULES[molecule_data[2]].divide(molecule_data[3],
                                                                obj,
                                                                offset=[0, 0, 0]
                                                                )
            MOLECULES[obj] = {"molecule": split_molecule,
                              "start": split_molecule.center.copy()
                              }
            # Set the mother molecule on the start rotation back before the split.
            if try_dict_keys(ANIMATION_OBJECTS[ANIMATION_OBJECTS[molecule_data[2]]["name"]], "keyframe_rotation_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[ANIMATION_OBJECTS[molecule_data[2]]["name"]], "keyframe_rotation"):
                rotate_objects(ANIMATION_OBJECTS[molecule_data[2]]["name"], step, True)

    # Move, Rotate and join objects
    for obj in ANIMATION_OBJECTS:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]

        if not MOLECULES[obj] is None:
            # Move object to the correct posision based on the step
            move_objects(obj, step)

            # Rotate object when possible 
            if try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation"):
                rotate_objects(obj, step)

            # Put the different objects in the render list
            if try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_shown_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_shown"):
                render_list = shown_objects(obj, step, render_list)
            else:
                render_list = put_object_in_render_list(obj, render_list)
            if obj == "camera":
                cam = Camera("location", MOLECULES[obj][0], "look_at", MOLECULES[obj][1])

    return Scene(cam, objects=render_list)


# Main
def main():
    global MOLECULES
    get_animation_data()
    MOLECULES = make_molecules(molecules={})
    pypovray.render_scene_to_png(make_frame, range(280))
    return 0


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
