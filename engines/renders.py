from models.images import Color, Image
from models.geometry import Matrix
from models.objects import Model
from models.primitives import Triangle
from models.vectors import Vector3f

WIDTH = 800  # WIDTH of the image
HEIGHT = 600  # HEIGHT of the image
DEPTH = 255

def m2v(m: "Matrix") -> Vector3f:
    return Vector3f(m[0][0]/m[3][0], m[1][0]/m[3][0], m[2][0]/m[3][0])


def v2m(v: "Vector3f") -> Vector3f:
    m = Matrix(4, 1)
    m[0][0] = v.x
    m[1][0] = v.y
    m[2][0] = v.z
    m[3][0] = 1.
    return m

def viewport(x: int, y: int, w: int, h: int) -> Matrix:
    m = Matrix.identity(4)
    m[0][3] = x + w / 2.0
    m[1][3] = y + h / 2.0
    m[2][3] = DEPTH / 2.0

    m[0][0] = w / 2.0
    m[1][1] = h / 2.0
    m[2][2] = DEPTH / 2.0
    return m

def render_model() -> None:
    light_dir = Vector3f(0,0,-1)
    camera = Vector3f(0,0,3)
    model = Model("obj/african_head.obj")

    zbuffer = [float('-inf')] * (WIDTH * HEIGHT)

    projection = Matrix.identity(4)
    view_port = viewport(WIDTH // 8, HEIGHT // 8, WIDTH * 3 // 4, HEIGHT * 3 // 4)
    projection[3][2] = -1.0 / camera.z

    image = Image(WIDTH, HEIGHT, Image.RGB)

    for i in range(model.nfaces()):
        face = model.face(i)
        screen_coords = []
        world_coords = []

        for j in range(3):
            v = model.vert(face[j])
            screen_coords.append(m2v(view_port * projection * v2m(v)))
            world_coords.append(v)

        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = n * light_dir

        if intensity is not None and intensity.norm() > 0:
            uv = [model.get_uv(i, k) for k in range(3)]
            triangle = Triangle(screen_coords[0], screen_coords[1], screen_coords[2],
                                uv[0], uv[1], uv[2], intensity, zbuffer)
            triangle.render(image, model, WIDTH, HEIGHT)

    image.flip_vertically()
    image.write_image_file("output.tga")

    zbimage = Image(WIDTH, HEIGHT, Image.GRAYSCALE)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            idx = i + j * WIDTH
            if zbuffer[idx] > float('-inf'):
                zbimage.set_pixel(i, j, Color(int(zbuffer[idx]), 1))
            else:
                # Set color for infinite z-buffer values to red (255, 0, 0)
                zbimage.set_pixel(i, j, Color(255, 0, 0))


    zbimage.flip_vertically()
    zbimage.write_image_file("zbuffer.tga")
