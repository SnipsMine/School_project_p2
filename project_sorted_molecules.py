"""
Sorts the aninimation_data with the split molecule data sorted so there will be no errors.
This module sorts the split molecule atom number in order for the split ca. high to low.

This module only supports only single atom splits
"""

__author__ = "Micha Beens, Des Beekhuis"

__version__ = "1.0.0"

# Imports

# Funtions
def sort_molecules(animation_objects):
    """
    Sorts the animaion objects so that there are no split errors happen
    """
    sorted_animation_objects = []

    special_object_list = []

    for obj in animation_objects:
        molecule_data = animation_objects[obj]["molecule"]
        if molecule_data[0] and molecule_data[1]:
            # Molecuels that have to be created bij spliting bigger molecules
            molecule_name = obj
            mother_molecule = animation_objects[obj]["molecule"][2]
            split_atom = animation_objects[obj]["molecule"][3]
            special_object_list.append([molecule_name, mother_molecule, split_atom])
        else:
            # Objects that do not need to be split
            sorted_animation_objects.append(obj)

    # Get a list of mother molecules from the special object list
    mother_list = list({special_object_list[index][1]
                        for index in range(len(special_object_list))})

    for mother in mother_list:
        high_2_low = get_highest(mother, special_object_list, [])
        print("SORTED {}: {}".format(mother, high_2_low))
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
