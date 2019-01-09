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

Upcomming functions:
- Joining multiple molecules together into one molecuele
- Rotation of molecules
- Stop showing objects
"""

__author__ = "Micha Beens"

__version__ = "1.0.0"

# Imports
import sys
from vapory import Sphere, Camera, LightSource, Scene
from pypovray import pypovray, models, pdb

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
            - False (file_path) pdb document
        - False (vapory components) components {!!These components are static and cant move!!}
    - (list) frame range keyframes
    - (list) keyframe end position xyz
    """

    global ANIMATION_OBJECTS

    ethanol = {"name": "ethanol",
               "molecule": [True, False, "pdb/ethanol2.pdb"],
               "keyframe_frames": [0, 10],
               "keyframe_endpos": [[60, 0, 0],
                                   [30, 0, 0],
                                   ]
               }

    water = {"name": "water",
               "molecule": [True, False, "pdb/water.pdb"],
               "keyframe_frames": [0],
               "keyframe_endpos": [[0, 0, 0],
                                   ]
             }
    
    NAD = {"name": "NAD",
               "molecule": [True, False, "pdb/NAD.pdb"],
               "keyframe_frames": [0, 10, 20],
               "keyframe_endpos": [[-30, 50, 0],
                                   [-30, 50, 0],
                                   [15, 15, 0],
                                   ]
           }

    enzyme1 = {"name": "enzyme1",
               "molecule": [False, Sphere([30, 0, -10], 4, models.default_sphere_model)],
               "keyframe_frames": [0],
               "keyframe_endpos": [[30, 0, -10],
                                   ]
               }

    enzyme2 = {"name": "enzyme2",
               "molecule": [False, Sphere([-30, 0, -10], 4, models.default_sphere_model)],
               "keyframe_frames": [0],
               "keyframe_endpos": [[-30, 0, -10],
                                   ]
               }

    waterstof = {"name": "waterstof",
               "molecule": [True, True, "ethanol", [3]],
               "keyframe_frames": [20, 25],
               "keyframe_endpos": [[0, 0, 0],
                                   [0, -4, 0],
                                   ]
               }

    hNAD = {"name": "hNAD",
               "molecule": [True, True, "ethanol", [8]],
               "keyframe_frames": [20, 25],
               "keyframe_endpos": [[0, 0, 0],
                                   [-4, 0, 0],
                                   ]
            }
    h_movement = {"name": "h_movement",
               "molecule": [True, True, "ethanol", [4]],
               "keyframe_frames": [20, 25],
               "keyframe_endpos": [[0, 0, 0],
                                   [0.1, -0.3, -0.8],
                                   ]
               }

    ANIMATION_OBJECTS = {"ethanol": ethanol,
                         "water": water,
                         "NAD": NAD,
                         "enzyme1": enzyme1,
                         "enzyme2": enzyme2,
                         "waterstof": waterstof,
                         "hNAD": hNAD,
                         "h_movement": h_movement,
                         }
    return


def molecules(frame = None, molecules = {}):

    sorted_animation_objects = sort_molecules()
    
    for obj in sorted_animation_objects:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        
        if molecule_data[0] and not molecule_data[1] and frame == None:
            # Making normal molecules from pdb file
            molecule = pdb.PDBMolecule(molecule_data[2], center=True)
            
        elif not molecule_data[0] and frame == None:
            # Making basic vapory objects
            molecule = molecule_data[1:]

        elif molecule_data[0] and molecule_data[1]:
            # Split a larger molecule to create a atom
            if not frame == None and frame >= ANIMATION_OBJECTS[obj]["keyframe_frames"][0]:
                split_molecule = MOLECULES[molecule_data[2]].divide(molecule_data[3],
                                                              obj,
                                                              offset=[0, 0, 0]
                                                              )
                molecule = {"molecule": split_molecule,
                            "start": split_molecule.center.copy()
                            }
                print(obj+":", molecule["start"])
                
            else:
                # Make the molecule a None object if it is not time to split the moleucle
                molecule = None
        else:

            # Make molecule the object in the dictionary
            molecule = molecules[obj]

        molecules[obj] = molecule
    return molecules


def sort_molecules():
    """Sorts the animaion objects so that there are no split errors happen"""
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
    mother_list = list(set([special_object_list[index][1] for index in range(len(special_object_list))]))

    for mother in mother_list:
        high_2_low = get_highest(mother, special_object_list, [])
        print("SORTED:",high_2_low)
        for obj in high_2_low:
            if not obj in sorted_animation_objects:
                sorted_animation_objects.append(obj)

    # Print objects in sorter for debugging
    for obj in sorted_animation_objects:
        #print("DEBUG:", obj)
        pass

    return sorted_animation_objects


def get_mothers(object_list):
    """Outputs a list of all mother molecuels that are needed for the molecule spliting"""
    mother_list = []

    for index in range(len(object_list)):
        if not object_list[index][1] in mother_list:
            mother_list.append(object_list[index][1])
    
    return mother_list


def get_highest(mother, object_list, high_2_low = []):
    """outputs a list from high to low"""
    highest = -1
    highest_molecule = ""
    for index in range(len(object_list)):
        if object_list[index][1] == mother and object_list[index][2][0] > highest:
            highest = object_list[index][2][0]
            highest_molecule = object_list[index][0]
    
    high_2_low.append(highest_molecule)
    object_list.pop(object_list.index([highest_molecule, mother, [highest]]))
    
    print(highest_molecule)
    print(high_2_low)
    if is_mother_in_list(mother, object_list):
        get_highest(mother, object_list, high_2_low)
    print(high_2_low)
    return  high_2_low


def is_mother_in_list(mother, object_list):
    """Outputs a bool to see if there are objects with te same mother"""
    output = False
    for index in range(len(object_list)):
        if mother in object_list[index]:
            output = True
            break     
    return output


def calculate_distance(frames, ends, step, molecule_start, offset = False):
    """Calculates the step size for the movement"""

    distance_list = []

    time = (frames[1]) - frames[0]

    for xyz in range(len(molecule_start)):
        start = molecule_start[xyz]
        if offset:
            end = ends[xyz]
        else:
            end = ends[xyz] - start
        distance = start + end / time * (step - frames[0])
        distance_list.append(distance)

    return distance_list


def move_objects(obj, step, mother = False):
    
    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_frames"]
    keyframe_endpos_data = ANIMATION_OBJECTS[obj]["keyframe_endpos"]
    
    for frame in range(len(keyframe_frames_data)):
        if frame != 0 and step > keyframe_frames_data[frame-1] and step <= keyframe_frames_data[frame]:
            print("if:", obj)
            if molecule_data[1]:
                distance = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                                    keyframe_endpos_data[frame],
                                                    step,
                                                    MOLECULES[obj]["start"],
                                                    True)

                MOLECULES[obj]["molecule"].move_to(list(distance))
            elif mother:
                MOLECULES[obj].move_to(keyframe_endpos_data[frame-1])
                
            else:
                distance = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                                keyframe_endpos_data[frame],
                                                step,
                                                keyframe_endpos_data[frame-1])

                MOLECULES[obj].move_to(list(distance))
            break
                    
        elif frame == 0 and step == keyframe_frames_data[frame] and molecule_data[0]:
            # if true move objects to start position and go to the next molecule
            print("elif1:", obj)
            #print(MOLECULES[obj])
            if not molecule_data[1]:
                MOLECULES[obj].move_to(keyframe_endpos_data[frame])
            break
        
        elif molecule_data[0] and molecule_data[1]:
            # If the other statment are false do this
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("elif2:", obj)
            distance = MOLECULES[obj]["start"].copy()
            for index in range(frame+1):
                distance += keyframe_endpos_data[index]
            MOLECULES[obj]["molecule"].move_to(distance)
            
        elif molecule_data[0]:
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("elif3:", obj)
            MOLECULES[obj].move_to(keyframe_endpos_data[frame])


def frame(step):
    global MOLECULES

    cam = Camera("location", [0, 0, 100], "look_at", [0, 0, 0])
    light = LightSource([0, 0, 100], 1)
    render_list = [light]
    print("frame:{}----------------------------------------------------------------".format(step))  
    # Is there another None molecule that needs to be created.
    for obj in MOLECULES:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_frames"]
        if MOLECULES[obj] == None and step >= keyframe_frames_data[0]:
            # Set the mother molecule on the start position of split.
            print(ANIMATION_OBJECTS[molecule_data[2]]["name"])
            move_objects(ANIMATION_OBJECTS[molecule_data[2]]["name"], keyframe_frames_data[0])
            MOLECULES = molecules(step, MOLECULES)


    for obj in ANIMATION_OBJECTS:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        
        if not MOLECULES[obj] == None:
            # Move object to the correct posision based on the step
            move_objects(obj, step)

            # Put the different objects in the render list
            if molecule_data[0] and molecule_data[1]:
                render_list = render_list + MOLECULES[obj]["molecule"].povray_molecule
            elif molecule_data[0]:
                render_list = render_list + MOLECULES[obj].povray_molecule
            else:
                render_list = render_list + MOLECULES[obj]                                  
    return Scene(cam, objects=render_list)


# Main
def main():
    global MOLECULES
    get_animation_data()
    MOLECULES = molecules()
    pypovray.render_scene_to_png(frame, range(19, 30))

    print(MOLECULES["ethanol"])
    
    return 0


if __name__ == "__main__":
    exitcode = main()
    sys.exit(exitcode)
