from models.objects.vectors import RGB

class Material:
    def __init__(self, color: RGB):
        if not isinstance(color, RGB):
            raise TypeError("Color must be RGB")
        self.__color__: RGB = color
    
    @property
    def color(self):
        return self.__color__

    @color.setter
    def color(self, value):
        if not isinstance(value, RGB):
            raise TypeError("Color must be RGB")
        self.__color__ = value
