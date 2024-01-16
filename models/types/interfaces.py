class IShader:
    def __init__(self):
        pass

    def vertex(self, iface, nthvert):
        raise NotImplementedError("vertex method must be implemented in derived classes")

    def fragment(self, bar, color):
        raise NotImplementedError("fragment method must be implemented in derived classes")