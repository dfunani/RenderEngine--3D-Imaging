import math
import numpy as np
from typing import List

from models.vectors import Vector2, Vector3

def cross(v1, v2):
    return Vector3(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)

def proj(dim, v):
    return Vector2(v.x, v.y) if dim == 2 else Vector3(v.x, v.y, v.z)


def lookat(eye, center, up):
    z = (eye - center).normalize()
    x = cross(up, z).normalize()
    y = cross(z, x).normalize()

    ModelView = Matrix.identity()
    for i in range(3):
        ModelView[0, i] = x[i]
        ModelView[1, i] = y[i]
        ModelView[2, i] = z[i]
        ModelView[i, 3] = -center[i]

def viewport(x, y, w, h):
    Viewport = Matrix.identity()
    Viewport[0, 3] = x + w / 2
    Viewport[1, 3] = y + h / 2
    Viewport[2, 3] = 255 / 2
    Viewport[0, 0] = w / 2
    Viewport[1, 1] = h / 2
    Viewport[2, 2] = 255 / 2

def projection(coeff):
    Projection = Matrix.identity()
    Projection[3, 2] = coeff

def barycentric(A, B, C, P):
    s = [Vector3(C[i] - A[i], B[i] - A[i], A[i] - P[i]) for i in range(2)]
    u = cross(s[0], s[1])
    if abs(u[2]) > 1e-2:
        return Vector3(1 - (u.x + u.y) / u.z, u.y / u.z, u.x / u.z)
    return Vector3(-1, 1, 1)

def triangle(pts, shader, image, zbuffer):
    bboxmin = Vector2(float('inf'), float('inf'))
    bboxmax = Vector2(-float('inf'), -float('inf'))

    for i in range(3):
        for j in range(2):
            bboxmin[j] = min(bboxmin[j], pts[i][j] / pts[i][3])
            bboxmax[j] = max(bboxmax[j], pts[i][j] / pts[i][3])

    P = Vec2i()
    color = TGAColor()

    for P.x in range(int(bboxmin.x), int(bboxmax.x) + 1):
        for P.y in range(int(bboxmin.y), int(bboxmax.y) + 1):
            c = barycentric(proj(2, pts[0] / pts[0][3]), proj(2, pts[1] / pts[1][3]),
                            proj(2, pts[2] / pts[2][3]), proj(2, P))
            z = pts[0][2] * c.x + pts[1][2] * c.y + pts[2][2] * c.z
            w = pts[0][3] * c.x + pts[1][3] * c.y + pts[2][3] * c.z
            frag_depth = max(0, min(255, int(z / w + 0.5)))

            if c.x < 0 or c.y < 0 or c.z < 0 or zbuffer.get(P.x, P.y)[0] > frag_depth:
                continue

            discard = shader.fragment(c, color)

            if not discard:
                zbuffer.set(P.x, P.y, TGAColor(frag_depth))
                image.set(P.x, P.y, color)

if __name__ == "__main__":
    # Main program entry
    pass
