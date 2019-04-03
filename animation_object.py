import sys

class animation_object(object):

    def __init__(self, name, ani_object):

        self.name = name

        self.endpos = []
        self.endpos_frame = []

        self.rotation = []
        self.rotation_frame = []

        if ani_object == type(str):
            self.open_pdbfile(ani_object)

    def open_pdbfile(self, file):
        pass

    def add_endpos(self, frame_endpos, endpos):
        if type(frame_endpos) == list and type(endpos) == list:

            if len(frame_endpos) == len(endpos):

                if all(isinstance(x, int) for x in endpos) and all(isinstance(x, (int, float)) for x in frame_endpos):
                    self.endpos += endpos
                    self.endpos_frame += frame_endpos

                else:
                    sys.exit("Some objects in the lists are not int/float")

            else:
                sys.exit("One or more of the given arguments are not lists")

        elif type(frame_endpos) == int and type(endpos) == int or type(endpos) == float:
            self.endpos.append(endpos)
            self.endpos_frame.append(frame_endpos)

        else:
            sys.exit("The given arguments are not both lists or not both int/float")

    def add_rotation(self, frame_rotation, rotation):
        if type(frame_rotation) == list and type(rotation) == list:

            if len(frame_rotation) == len(rotation):

                if all(isinstance(x, int) for x in rotation) and all(isinstance(x, (int, float)) for x in frame_rotation):
                    self.rotation += rotation
                    self.rotation_frame += frame_rotation

                else:
                    sys.exit("Some objects in the lists are not int/float")

            else:
                sys.exit("One or more of the given arguments are not lists")

        elif type(frame_rotation) == int and type(rotation) == int or type(rotation) == float:
            self.rotation.append(rotation)
            self.rotation_frame.append(frame_rotation)

        else:
            sys.exit("The given arguments are not both lists or not both int/float")
        pass