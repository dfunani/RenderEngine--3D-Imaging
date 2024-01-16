import math
import numpy as np
from typing import List

Model = None  # Assume that you'll instantiate the Model class in your actual code
width = 800
height = 800

light_dir = Vec3f(1, 1, 1)
eye = Vec3f(0, -1, 3)
center = Vec3f(0, 0, 0)
up = Vec3f(0, 1, 0)

class GouraudShader(IShader):
    def __init__(self):
        self.varying_intensity = Vec3f()

    def vertex(self, iface, nthvert):
        gl_Vertex = embed(model.vert(iface, nthvert), 4)
        gl_Vertex = Viewport @ Projection @ ModelView @ gl_Vertex
        self.varying_intensity[nthvert] = max(0.0, model.normal(iface, nthvert) @ light_dir)
        return gl_Vertex

    def fragment(self, bar, color):
        intensity = self.varying_intensity @ bar
        color[0] = color[1] = color[2] = int(255 * intensity)
        return False

def embed(v, length):
    ret = Vec4f()
    for i in range(length):
        ret[i] = v[i] if i < len(v) else 1.0
    return ret

def main(argc, argv):
    global model
    if argc == 2:
        model = Model(argv[1])
    else:
        model = Model("obj/african_head.obj")

    lookat(eye, center, up)
    viewport(width / 8, height / 8, width * 3 / 4, height * 3 / 4)
    projection(-1.0 / (eye - center).norm())
    light_dir.normalize()

    image = TGAImage(width, height, TGAImage.RGB)
    zbuffer = TGAImage(width, height, TGAImage.GRAYSCALE)

    shader = GouraudShader()
    for i in range(model.nfaces()):
        screen_coords = [shader.vertex(i, j) for j in range(3)]
        triangle(screen_coords, shader, image, zbuffer)

    image.flip_vertically()
    zbuffer.flip_vertically()
    image.write_tga_file("output.tga")
    zbuffer.write_tga_file("zbuffer.tga")

if __name__ == "__main__":
    main(2, ["program_name", "path/to/your/obj/file"])
