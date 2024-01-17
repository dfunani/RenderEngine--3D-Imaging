from models.vectors import Matrix, Vector2, Vector3

ModelView = Matrix.identity()
Viewport = Matrix.identity()
Projection = Matrix.identity()

def cross(v1, v2):
    return Vector3(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x
    )


def proj(dim, v):
    return Vector2(v.x, v.y) if dim == 2 else Vector3(v.x, v.y, v.z)


def lookat(eye, center, up):
    global ModelView 
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
    global Viewport  #
    Viewport = Matrix.identity()
    Viewport[0, 3] = x + w / 2
    Viewport[1, 3] = y + h / 2
    Viewport[2, 3] = 255 / 2
    Viewport[0, 0] = w / 2
    Viewport[1, 1] = h / 2
    Viewport[2, 2] = 255 / 2


def projection(coeff):
    global Projection  #
    Projection = Matrix.identity()
    Projection[3, 2] = coeff


def barycentric(A, B, C, P):
    s = [Vector3(C[i] - A[i], B[i] - A[i], A[i] - P[i]) for i in range(2)]
    u = cross(s[0], s[1])
    if abs(u[2]) > 1e-2:
        return Vector3(1 - (u.x + u.y) / u.z, u.y / u.z, u.x / u.z)
    return Vector3(-1, 1, 1)
