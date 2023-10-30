from models.objects.vectors import Vector3Float


class Lighting:
    def __init__(self, position: Vector3Float, intensity: float) -> None:
        self.position = position
        self.intensity = intensity

    
