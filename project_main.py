#!/usr/bin/env python3

"""
This program creates a series of frames that can be combined to form a animation
of the metabolic proces of ethanol in humans.

Current functions:
- Create a molecule from a pbb file.
- Move molecules from start position to end position
- Split atoms form larger molecules
- Move the atoms to offset
- Create basic vapory objects
- Joining multiple molecules together into one molecule
- Rotation of molecules (only with single core renders)
- Start and stop showing objects (default is always shown)
- Added support for moving Camera objects.

Upcomming functions:
- Rotation of molecules with multi core render support
- Reading the animation data from a .micdes animation file
- Add support for splits with multiple atoms at a time
- Add support for moving vapory objects.
- Showing labels

Known bugs:
- After splitting a molecule the molecule auto centers itself. This couses the molecule to moves a
  bit.
"""

__author__ = "Micha Beens"

__version__ = "1.0.0"

# Imports
import sys
from vapory import Camera, LightSource, Scene
from pypovray import pypovray, pdb
from project_animation_data_ethanol_2_acetic_acid import get_animation_data as ethanol_2_acetic_acid
from project_sorted_molecules import sort_molecules
from animation_object import AnimationObject


# Globals
MOLECULES = {}
ANIMATION_OBJECTS = {}


# Functions
def get_animation_data(show_name):
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

    animatie_data_0 = ethanol_2_acetic_acid(show_name=show_name)
    animatie_data_1 = ethanol_2_acetic_acid(1, 270, [[60, 20, 0], [0, 0, 0], [-60, 10, 0]], 80, 0, 15, show_name)
    animatie_data_2 = ethanol_2_acetic_acid(2, 270, [[60, 10, 0], [0, 20, 0], [-60, 10, 0]], 160, 400, 15, show_name)
    animatie_data_3 = ethanol_2_acetic_acid(3, 270, [[60, 00, 0], [0, 0, 0], [-60, 0, 0]], 0, 0, 15, show_name)
    animatie_data_4 = ethanol_2_acetic_acid(4, 270, [[60, -10, 0], [0, -10, 0], [-60, -10, 0]], 120, 30, 15, show_name)
    animatie_data_5 = ethanol_2_acetic_acid(5, 270, [[60, -20, 0], [0, -20, 0], [-60, -20, 0]], 40, 400, 15, show_name)
    animation_data = [animatie_data_0,
                      animatie_data_1,
                      animatie_data_2,
                      animatie_data_3,
                      animatie_data_4,
                      animatie_data_5,]

    for animation_dict in animation_data:
        for obj in animation_dict:
            ANIMATION_OBJECTS[obj] = animation_dict[obj]

def make_molecules(molecules):
    """
    make_molecules([frame, molecules])
    """
    for obj in ANIMATION_OBJECTS:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]

        if molecule_data[0] and not molecule_data[1]:
            # Making normal molecules from pdb file
            mol = pdb.PDBMolecule(molecule_data[2], center=True)
            molecule = {"molecule": mol,
                        "reset": [0, mol.atoms.copy()],
                        "text": None
                        }

        elif not molecule_data[0]:
            # Making basic vapory objects
            molecule = {"molecule": molecule_data[1:]}

        else:
            # Make the molecule a None object until it is time to split the moleucle
            molecule = None

        molecules[obj] = molecule
    return molecules


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
    """
    move_objects(obj, step, [mother])

    arguments:
    - obj: string
    - step: int
    - mother: bool

    Move the object to the right position based on the step. If no mother is given the default is False
    """
    global MOLECULES

    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_endpos_frames"]
    keyframe_endpos_data = ANIMATION_OBJECTS[obj]["keyframe_endpos"]

    for frame in range(len(keyframe_frames_data)):
        #Move object if step is in range
        if frame != 0 and step in [val for val in range(keyframe_frames_data[frame-1]+1,
                                                        keyframe_frames_data[frame]+1)]:
            move_object_in_range(step, frame, obj, mother)
            break

        # if step is lower than the keyframe move object to that position
        elif frame == 0 and step <= keyframe_frames_data[frame]:
            # if true move objects to start position and go to the next molecule
            print("(move) elif1:", obj)
            if molecule_data[0] and not molecule_data[1]:
                MOLECULES[obj]["molecule"].move_to(keyframe_endpos_data[frame])
            elif obj == "camera":
                MOLECULES[obj]["molecule"] = [keyframe_endpos_data[frame][0], keyframe_endpos_data[frame][1]]

            break

        # if object is a molecule and a split molecule move the object with a offset
        elif molecule_data[0] and molecule_data[1]:
            # If the other statment are false do this
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("(move) elif2:", obj)
            distance = MOLECULES[obj]["start"].copy()
            for index in range(frame+1):
                distance += keyframe_endpos_data[index]
            MOLECULES[obj]["molecule"].move_to(distance)

        # if object is a molecule move object to the position of frame
        elif molecule_data[0]:
            if keyframe_frames_data[-1] == keyframe_frames_data[frame]:
                print("(move) elif3:", obj)
            MOLECULES[obj]["molecule"].move_to(keyframe_endpos_data[frame][:3])

            # if molecules need to be joined
            if step >= keyframe_frames_data[frame] and try_dict_keys(keyframe_endpos_data[frame], 3) and not mother and not keyframe_endpos_data[frame][4]:
                for mol in range(5, 5+len(keyframe_endpos_data[frame][5:])):
                    print("join {} and {} at frame {}".format(obj, keyframe_endpos_data[frame][mol], keyframe_frames_data[frame]))
                    # Set the molecules that is
                    move_objects(keyframe_endpos_data[frame][mol], keyframe_frames_data[frame])
                    MOLECULES[obj]["molecule"] = molecule_maker(MOLECULES[obj]["molecule"], MOLECULES[keyframe_endpos_data[frame][mol]]["molecule"], obj)
                keyframe_endpos_data[frame][4] = True

        else:
            if keyframe_frames_data[-1] == keyframe_frames_data[frame] and not obj == "camera":
                print("(move) else: {}".format(obj))
            if obj == "camera":
                MOLECULES[obj]["molecule"] = [keyframe_endpos_data[frame][0], keyframe_endpos_data[frame][1]]


def move_object_in_range(step, frame, obj, mother):
    """
    move_object_in_range(step, frame, obj, mother)

    Arguments:
    - step: int
    - frame: int
    - obj: string
    - mother: bool

    Moves the object to the place equevelent to the step
    """
    # move the object to the place equevelent to the step

    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_endpos_frames"]
    keyframe_endpos_data = ANIMATION_OBJECTS[obj]["keyframe_endpos"]

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

    #if object is mother move the object to previous frame
    elif mother and step != keyframe_frames_data[frame]:
        MOLECULES[obj]["molecule"].move_to(keyframe_endpos_data[frame-1])

    # if object is a molecule move it as a molecule
    elif molecule_data[0]:
        distance = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                      keyframe_endpos_data[frame][:3],
                                      step,
                                      keyframe_endpos_data[frame-1][:3])

        MOLECULES[obj]["molecule"].move_to(list(distance))

    # if object is a vapory object
    elif not molecule_data[0]:
        # move the camera
        if obj == "camera":
            location = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                          keyframe_endpos_data[frame][0][:3],
                                          step,
                                          keyframe_endpos_data[frame-1][0][:3])

            look_at = calculate_distance([keyframe_frames_data[frame-1], keyframe_frames_data[frame]],
                                         keyframe_endpos_data[frame][1][:3],
                                         step,
                                         keyframe_endpos_data[frame-1][1][:3])

            MOLECULES[obj]["molecule"] = [location, look_at]

    # if molecules need to be joined
    if step == keyframe_frames_data[frame] and try_dict_keys(keyframe_endpos_data[frame], 3) and not mother and not keyframe_endpos_data[frame][4]:
        for mol in range(5, 5+len(keyframe_endpos_data[frame][5:])):
            print("join {} and {} at frame {}".format(obj, keyframe_endpos_data[frame][mol], step))
            # Set the molecules that is
            move_objects(keyframe_endpos_data[frame][mol], step)
            MOLECULES[obj]["molecule"] = molecule_maker(MOLECULES[obj]["molecule"], MOLECULES[keyframe_endpos_data[frame][mol]]["molecule"], obj)

            keyframe_endpos_data[frame][4] = True

def rotate_objects(obj, step, mother=False):
    """
    rotate_objects(obj, step, [mother])

    arguments:
    - obj: string
    - step: int
    - mother: True

    Rotate the objects for the right value not based on the step.
    If no mother is given default is False
    """
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

                MOLECULES[obj]["molecule"].rotate([1, 1, 1], [radians[0]*-1, radians[1]*-1, radians[2]*-1])

            else:
                radians = calculate_radians([rotate_frames_data[frame-1], rotate_frames_data[frame]],
                                            rotate_endpos_data[frame][1],
                                            )

                MOLECULES[obj]["molecule"].rotate([1, 1, 1], radians)
            break


def shown_objects(obj, step, render_list):
    """
    shown_objects(obj, step, render_list)

    arguments:
    - obj: String
    - step: int
    - render_list: list

    Move/rotate the objects and put them in the render_list
    """
    shown_frames_data = ANIMATION_OBJECTS[obj]["keyframe_shown_frames"]
    shown_bool_data = ANIMATION_OBJECTS[obj]["keyframe_shown"]

    # Rotate object when possible
    if try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation_frames") and\
       try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation"):
        rotate_objects(obj, step)

    for frame in range(len(shown_frames_data)):
        if frame != 0 and step in [val for val in range(shown_frames_data[frame-1], shown_frames_data[frame])] and shown_bool_data[frame-1] or \
           frame == 0 and step <= shown_frames_data[frame]:
            print("(shown): {}".format(obj))
            # Move object to the correct posision based on the step
            move_objects(obj, step)

            # Put object in render_list
            if ANIMATION_OBJECTS[obj]["show_name"]:
                render_list = put_object_in_render_list(obj, render_list, text=True)

            render_list = put_object_in_render_list(obj, render_list)
            break

        if shown_bool_data[frame] or \
           shown_frames_data[frame] == shown_frames_data[-1] and step > shown_frames_data[frame] and shown_bool_data[frame]:
            print("(shown): {}".format(obj))
            # Move object to the correct posision based on the step
            move_objects(obj, step)

            # Put object in render_list
            if ANIMATION_OBJECTS[obj]["show_name"]:
                render_list = put_object_in_render_list(obj, render_list, text=True)

            render_list = put_object_in_render_list(obj, render_list)
            break

        elif shown_frames_data[frame] == shown_frames_data[-1]:
            print("(shown) elif: {} (object not shown)".format(obj))

    return render_list


def put_object_in_render_list(obj, render_list, text=False):
    """
    Puts the object in the render_list so it will be renderd.
    """
    molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
    if molecule_data[0]:
        render_list = render_list + MOLECULES[obj]["molecule"].povray_molecule
    elif not obj == "camera":
        render_list = render_list + MOLECULES[obj]["molecule"]

    if text:
        render_list = render_list + [MOLECULES[obj]["text"]]

    return render_list


def try_dict_keys(dictionary, key):
    """
    This function trys a dict and key together to see if it returns a key/slice error and
    returns a bool based on that.
    """
    try:
        dictionary[key]
        return True
    except:
        return False


def make_frame(step):
    """
    meke_frame(step)

    arguments:
    - step: int

    Create the scene that coresponds to the step.
    """
    global MOLECULES

    # Basic objects for the scene
    cam = Camera("location", [0, 0, 100], "look_at", [0, 0, 0])
    light = LightSource([0, 0, 100], 1)
    render_list = [light]

    print("frame:{}----------------------------------------------------------------".format(step))

    sorted_animation_objects = sort_molecules(ANIMATION_OBJECTS)

    # Is there another None molecule that needs to be created.
    for obj in sorted_animation_objects:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]
        keyframe_frames_data = ANIMATION_OBJECTS[obj]["keyframe_endpos_frames"]
        if MOLECULES[obj] is None and step >= keyframe_frames_data[0]:
            mother_name = ANIMATION_OBJECTS[molecule_data[2]]["name"]

            # Set the mother molecule on the start position of split.
            move_objects(mother_name, keyframe_frames_data[0], True)

            # Set the mother molecule on the start rotation of split.
            if try_dict_keys(ANIMATION_OBJECTS[mother_name], "keyframe_rotation_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[mother_name], "keyframe_rotation"):
                rotate_objects(mother_name, step)
            print(obj)
            # Call make molecules to split the molecule
            split_molecule = MOLECULES[molecule_data[2]]["molecule"].divide(molecule_data[3],
                                                                            obj,
                                                                            offset=[0, 0, 0]
                                                                            )

            MOLECULES[obj] = {"molecule": split_molecule,
                              "start": split_molecule.center.copy(),
                              "reset": split_molecule.atoms,
                              "text": None
                              }

            # Set the mother molecule on the start rotation back before the split.
            if try_dict_keys(ANIMATION_OBJECTS[mother_name], "keyframe_rotation_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[mother_name], "keyframe_rotation"):
                rotate_objects(mother_name, step, True)

    # Move, Rotate and join objects
    for obj in ANIMATION_OBJECTS:
        molecule_data = ANIMATION_OBJECTS[obj]["molecule"]

        if not MOLECULES[obj] is None:
            # Put the different objects in the render list
            if try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_shown_frames") and\
               try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_shown"):

                # Move, rotate the objects and put them in the render_list
                render_list = shown_objects(obj, step, render_list)
            else:
                # Move object to the correct posision based on the step
                move_objects(obj, step)

                # Rotate object when possible
                if try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation_frames") and\
                   try_dict_keys(ANIMATION_OBJECTS[obj], "keyframe_rotation"):
                    rotate_objects(obj, step)

                #Put object in render_list
                render_list = put_object_in_render_list(obj, render_list)

            if obj == "camera":
                cam = Camera("location", MOLECULES[obj]["molecule"][0], "look_at", MOLECULES[obj]["molecule"][1])
    return Scene(cam, objects=render_list)


# Main
def main():
    """
    main()

    Main activates the program and renders the animation
    """
    global MOLECULES
    get_animation_data(False)
    MOLECULES = make_molecules(molecules={})
    pypovray.render_scene_to_mp4(make_frame, range(700))
    return 0


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
