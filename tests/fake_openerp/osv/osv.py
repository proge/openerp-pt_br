object_map = {}


class osv(object):
    def __init__(self):
        object_map[self.__class__.__name__] = self


def get_object(name):
    return object_map[name]
