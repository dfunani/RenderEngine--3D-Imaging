from models.vectors import Vector3i, Vector2i, Vector3f
from models.objects import Model
from engines.imaging import Image, Color
from models.geometry import Matrix


class Triangle:
    def __init__(
        self,
        t0: Vector3i,
        t1: Vector3i,
        t2: Vector3i,
        uv0: Vector2i,
        uv1: Vector2i,
        uv2: Vector2i,
        intensity: float,
        zbuffer: list[int],
    ):
        self.t0 = t0
        self.t1 = t1
        self.t2 = t2
        self.uv0 = uv0
        self.uv1 = uv1
        self.uv2 = uv2
        self.intensity = intensity
        self.zbuffer = zbuffer

    def render(self, image: Image, model: Model, width: int, height: int) -> None:
        if self.t0.y == self.t1.y and self.t0.y == self.t2.y:
            return image  # I don't care about degenerate triangles

        if self.t0.y > self.t1.y:
            self.t0, self.t1 = self.t1, self.t0
            self.uv0, self.uv1 = self.uv1, self.uv0
        if self.t0.y > self.t2.y:
            self.t0, self.t2 = self.t2, self.t0
            self.uv0, self.uv2 = self.uv2, self.uv0
        if self.t1.y > self.t2.y:
            self.t1, self.t2 = self.t2, self.t1
            self.uv1, self.uv2 = self.uv2, self.uv1

        total_height = self.t2.y - self.t0.y
        for i in range(int(total_height)):
            second_half = i > self.t1.y - self.t0.y or self.t1.y == self.t0.y
            segment_height = (
                self.t2.y - self.t1.y if second_half else self.t1.y - self.t0.y
            )
            alpha = i / total_height
            beta = (i - (self.t1.y - self.t0.y) if second_half else 0) / segment_height
            A = self.t0 + (self.t2 - self.t0) * alpha
            B = (
                self.t1 + (self.t2 - self.t1) * beta
                if second_half
                else self.t0 + (self.t1 - self.t0) * beta
            )
            uvA = self.uv0 + (self.uv2 - self.uv0) * alpha
            uvB = (
                self.uv1 + (self.uv2 - self.uv1) * beta
                if second_half
                else self.uv0 + (self.uv1 - self.uv0) * beta
            )

            if A.x > B.x:
                A, B = B, A
                uvA, uvB = uvB, uvA

            for j in range(int(A.x), int(B.x + 1)):
                phi = 1.0 if B.x == A.x else (j - A.x) / (B.x - A.x)
                P = Vector3f(A) + (Vector3f(B - A) * phi)
                uvP = uvA + (uvB - uvA) * phi

                # Ensure the coordinates are within the image bounds
                if isinstance(P.x, (int, float)) and isinstance(P.y, (int, float)):
                    x_coord = max(0, min(int(P.x), width - 1))
                    y_coord = max(0, min(int(P.y), height - 1))

                    idx = x_coord + y_coord * width

                    if self.zbuffer[idx] < P.z:
                        self.zbuffer[idx] = P.z
                        color = model.diffuse(uvP)
                        
                        image.set_pixel(
                            x_coord,
                            y_coord,
                            Color(
                                color.r * self.intensity,
                                color.g * self.intensity,
                                color.b * self.intensity,
                            ),
                        )
