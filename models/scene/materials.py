from models.objects.vectors import RGB, Vector4Float


class Material:
    def __init__(
        self,
        color: RGB = RGB(),
        albedo: Vector4Float = Vector4Float(2, 0, 0, 0),
        specular: float = 0.0,
        refraction: float = 1.0
    ):
        if not isinstance(color, RGB):
            raise TypeError("Color must be RGB")
        if not isinstance(albedo, Vector4Float):
            raise TypeError("albedo must be RGB")
        if not isinstance(specular, float):
            raise TypeError("specular must be Float")
        if not isinstance(refraction, float):
            raise TypeError("refraction must be Float")
        self.__color__: RGB = color
        self.__albedo__: Vector4Float = albedo
        self.__specular__: float = specular
        self.__refraction__: float = refraction

    @property
    def color(self):
        return self.__color__

    @color.setter
    def color(self, value):
        if not isinstance(value, RGB):
            raise TypeError("Color must be RGB")
        self.__color__ = value

    @property
    def albedo(self):
        return self.__albedo__

    @albedo.setter
    def albedo(self, value):
        if not isinstance(value, Vector4Float):
            raise TypeError("albedo must be Vector4Float")
        self.__albedo__ = value

    @property
    def specular(self):
        return self.__specular__

    @specular.setter
    def specular(self, value):
        if not isinstance(value, float):
            raise TypeError("specular must be float")
        self.__specular__ = value

    @property
    def refraction(self):
        return self.__refraction__

    @refraction.setter
    def refraction(self, value):
        if not isinstance(value, float):
            raise TypeError("refraction must be float")
        self.__refraction__ = value
