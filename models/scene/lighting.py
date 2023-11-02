from models.objects.vectors import Vector3Float


class Lighting:
    def __init__(self, position: Vector3Float = Vector3Float(), intensity: float= 1.0) -> None:
        self.position = position
        self.intensity = intensity

    
