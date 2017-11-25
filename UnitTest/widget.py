class WidGet(object):
    """Class to be test"""
    def __init__(self, size=(40, 40)):
        self.__size = size

    def get_size(self):
        return self.__size

    def resize(self, width, height):
        if width == 0 or height < 0:
            raise (ValueError, "Illegal size")
        self.__size = (width, height)

    def dispose(self):
        pass
