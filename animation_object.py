from pypovray import pdb
from math import pi


class AnimationObject():

    def __init__(self, name, metadata, endpos=(), rotation=(), shown=(), ):
        """
        Arguments:
        - (string) name: This argument contains the name of the Animation object
        - (list) metadata: contains the meta_data of the Animation object and consists out of,
            - (bool) isMolecule: If the animation object is a molecule this must be true
            - True:
                - (bool) isSplitMolecule: if the animation object is a split molecule this must br true
                - True:
                    - (string) nameMother: Is the name of the molecule that the Animation object split from.
                    - (list) splitMolecules: Is a list with all the molecules that need to be split
                        - (int) splitMolecule: Is the molecule that is split
                - False:
                    - (string) filePathOfMolecule: Is a string that that links to a file that contains al the data for
                                                   the Animation object
            - False:
                - (list) vaporyObjects: A list that contains objects from the Vapory package
                    - (vaporyObject) basicObject: Is a object from the package Vapory
        Usage:
        This module is called when the Object is created.
        """
        self.name = name

        self.metadata = metadata
        self.molecule = {"molecule": None,
                         "start": None,
                         "text": None}

        self.endpos = list(endpos)

        self.rotation = list(rotation)

        self.shown = list(shown)

        if tuple(self.metadata[0:2]) == (True, False):
            self.open_pdbfile(self.metadata[2])

        elif tuple(self.metadata[0:2]) == (True, True):
            self.molecule["molecule"] = None

        else:
            self.molecule["molecule"] = self.metadata[1:]

    def open_pdbfile(self, file):
        """
        Arguments:
        - (string) file: This variable contains the file path of the molecule

        Usage:
        When called it will open the file and assign the contents to the object variable molecule["molecule"]
        """
        self.molecule["molecule"] = pdb.PDBMolecule(file, center=True)

    def add(self, add_type, add_value):
        if all(isinstance(x, tuple) for x in add_value):
            if add_type == "endpos":
                self.add_endpos_list(add_value)

            elif add_type == "rotation":
                self.add_rotation_list(add_value)

            elif add_type == "shown":
                self.add_shown_list(add_value)

            else:
                raise ValueError("The given add_type is invalid. Valid types are 'endframe', 'rotation' or 'shown'")

        else:
            if add_type == "endpos":
                self.add_endpos_single(add_value)

            elif add_type == "rotation":
                self.add_rotation_single(add_value)

            elif add_type == "shown":
                self.add_shown_single(add_value)
            else:
                raise ValueError("The given add_type is invalid. Valid types are 'endframe', 'rotation' or 'shown'")

# ----------------------------------------------------------------------------------------------------------------------
    def add_endpos_list(self, endpos):
        if all(isinstance(x, tuple) for x in endpos):
            self.endpos += endpos

        else:
            raise TypeError("Some objects in the lists are not int/list")

    def add_endpos_single(self, endpos):
        if isinstance(endpos, tuple):
            self.endpos.append(endpos)

        else:
            raise TypeError("The given arguments are not int/list")

# ----------------------------------------------------------------------------------------------------------------------

    def add_rotation_list(self, rotation):
        if all(isinstance(x, tuple) for x in rotation):
            self.rotation += rotation
        else:
            raise TypeError("Some objects in the lists are not int/list")

    def add_rotation_single(self, rotation):
        if isinstance(rotation, tuple):
            self.rotation.append(rotation)
        else:
            raise TypeError("The given arguments are not int/list")

# ----------------------------------------------------------------------------------------------------------------------

    def add_shown_list(self, shown):
        if all(isinstance(x, tuple) for x in shown):
            self.shown += shown
        else:
            raise TypeError("Some objects in the lists are not bool")

    def add_shown_single(self, shown):
        if isinstance(shown, tuple):
            self.shown.append(shown)
        else:
            raise TypeError("The given arguments are not int/bool")

# ----------------------------------------------------------------------------------------------------------------------

    def split_molecule(self, step, mother_aniobject):
        if tuple(self.metadata[0:2]) == (True, True) \
                and self.molecule["molecule"] is None \
                and step >= self.endpos[0][0]:

            if mother_aniobject.name == self.metadata[2]:
                # Get the mother molecule
                mother_name = mother_aniobject.name

                # Move the Mother molecule
                # To be Added

                # Rotate the Mother molecule
                # To be Added

                # Split molecule from mother
                self.molecule["moleucle"] = mother_aniobject.molecule["molecule"].divide(self.metadata[3],
                                                                                         self.name,
                                                                                         offset=[0, 0, 0]
                                                                                         )
                self.molecule["start"] = self.molecule["molecule"].center.copy()

# ----------------------------------------------------------------------------------------------------------------------

    def __str__(self):
        """
        Print the animation_data to see what is in there.
        """
        printed_string = ""
        molecule_data = self.molecule["molecule"]

        printed_string += "---------------------------------------------------------------------\n"

        printed_string += "object: {}\n".format(self.name)

        # if object is a molecule, print the name type, if molecule is split and the name of the file
        if self.metadata[0]:
            printed_string += "(molecule) molecule: {}, split: {}, document/mother: {}\n".format(self.metadata[0],
                                                                                                 self.metadata[1],
                                                                                                 self.metadata[2])

        # if obj is not camera, print the type and name of the vapory object
        else:
            for ani_object in molecule_data[1:]:
                printed_string += "(molecule) molecule: {}, type: {}\n".format(molecule_data[0], type(ani_object))

        printed_string += "\n"

        # For every end possision and the coresponding frames print the data
        for frame in range(len(self.endpos)):
            printed_string += "(endpos) frame {}: {}\n".format(self.endpos[frame][0], self.endpos[frame][1])

        printed_string += "\n"

        # For every rotation and the coresponding frames print the data
        for frame in range(len(self.rotation)):
            printed_string += "(rotation) frame {}: {}\n".format(self.rotation[frame][0], self.rotation[frame][1])

        printed_string += "\n"

        # For every time the obect needs to be shown and the coresponding frames print the data
        for frame in range(len(self.shown)):
            printed_string += "(shown) frame {}: {}\n".format(self.shown[frame][0], self.shown[frame][1])
        return printed_string


if __name__ == "__main__":

    i = AnimationObject(name="ethanol1_1",
                        metadata=[True, False, "pdb/ethanol2.pdb"],
                        endpos=[(20, [60, 0, 0]), (29, [60, 0, 0]), (30, [60, 0, 0]), (75, [30, 0, 0]),
                                (90, [30, 0, 0, "join", False, "h_movement1_1"]), (140, [0, 0, 0]),
                                (141, [0, 0, 0]), (190, [-30, 0, 0]),
                                (205, [-30, 0, 0, "join", False, "water1_3"]),
                                (250, [-60, 0, 0]),
                                ],
                        rotation=[(29, [[0, 0, 0], [0, 0, 0]]),
                                  (30, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (75, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (90, [[0, 0, 0], [0, 0, 0]]),
                                  (140, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (141, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (190, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (205, [[0, 0, 0], [0, 0, 0]]),
                                  (250, [[1, 1, 1], [pi * 2, pi * 2, pi * 2]]),
                                  (500, [[1, 1, 1], [pi * 8, pi * 8, pi * 8]]),
                                  ],
                        shown=[(0, True), (0, True), (250, True)],
                        )

    print(i)
    i.add("endpos", (0, [100, 100, 100]))
    print(i)
    exit(1)
