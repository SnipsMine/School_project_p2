class animation_object(object):

    def __init__(self, name, ani_object):

        self.name = name

        if ani_object == type(str):
            self.open_pdbfile(ani_object)

    def open_pdbfile(self, file):
        pass
