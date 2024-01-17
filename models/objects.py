from math import isclose
from PIL import UnidentifiedImageError, Image
from numpy import array, dot, fliplr, flipud, uint8, zeros
from engines.renders import embed
from models.geometry import (
    ModelView,
    Projection,
    Viewport,
    lookat,
    proj,
    projection,
    viewport,
)
from models.types.exceptions import ObjectImageError
from models.vectors import Matrix, Vector2, Vector3

"""
imaging Module

This module provides the ObjectImage class for reading, writing, and 
performing operations on Object image files.

Classes:
- ObjectImage: Class for reading and writing Object image files and performing 
image operations.

Usage:
from images import ObjectImage

# Create a ObjectImage object
image = ObjectImage()

# Read a Object image file
image.read_file("input.ext")

# Perform operations (e.g., flip horizontally)
image.flip_horizontally()

# Write the modified image to a new Object image file
image.write_file("output.ext")
"""

from math import isclose
from PIL import Image, UnidentifiedImageError
from numpy import array, fliplr, flipud, zeros, uint8
from engines.renders import embed
from models.geometry import (
    ModelView,
    Projection,
    Viewport,
    lookat,
    proj,
    projection,
    viewport,
)
from models.types.exceptions import ObjectImageError
from models.types.interfaces import IShader
from models.vectors import Matrix, Vector2, Vector3


class ObjectCamera:
    def __init__(self, eye=Vector3(0, -1, 3), center=Vector3(), up=Vector3(0, 1, 0)):
        self.eye = eye
        self.center = center
        self.up = up


class ObjectColor:
    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


ModelView = Matrix.identity()
Viewport = Matrix.identity()
Projection = Matrix.identity()


class ObjectShader(IShader):
    def __init__(self, model, light_dir):
        self.varying_intensity = Vector3()
        self.model = model
        self.light_dir = light_dir

    def set_matrices(self, model_view, projection, viewport):
        self.model_view_matrix = model_view
        self.projection_matrix = projection
        self.viewport_matrix = viewport

    def vertex(self, iface, nthvert):
        vertex_list = [self.model.vert(iface, nthvert)[i] for i in range(3)]
        gl_Vertex = embed(vertex_list, 4)
        gl_Vertex = dot(gl_Vertex, dot(Viewport, dot(Projection, ModelView)))
        self.varying_intensity[nthvert] = max(
            0.0, self.model.normal(iface, nthvert) * self.light_dir
        )
        return gl_Vertex

    def fragment(self, bar, color):
        intensity = self.varying_intensity @ bar
        color[0] = color[1] = color[2] = int(255 * intensity)
        return False


class ObjectImage:
    """
    ObjectImage class for reading and writing Object image files and performing
    image operations.
    """

    def __init__(
        self, width, height, color_format=ObjectColor, light_dir=Vector3(1, 1, 1)
    ) -> None:
        """
        Initialize ObjectImage object.
        """
        self.width = width
        self.height = height
        self.color_format = color_format
        self.pixels = zeros((width, height, 4), dtype=uint8)
        self.model_view_matrix = Matrix.identity()
        self.projection_matrix = Matrix.identity()
        self.viewport_matrix = Matrix.identity()
        self.light_dir = light_dir

    def set_matrices(self, model_view, projection, viewport):
        self.model_view_matrix = model_view
        self.projection_matrix = projection
        self.viewport_matrix = viewport

    def render_model(self, model, camera) -> None:
        self.model = model

        # Set up transformation matrices
        lookat(camera.eye, camera.center, camera.up)
        viewport(
            self.width // 8, self.height // 8, self.width * 3 // 4, self.height * 3 // 4
        )
        projection(-1 / (camera.eye - camera.center).norm())

        # Initialize shader and set matrices
        gouraud_shader = ObjectShader(self.model, self.light_dir)
        gouraud_shader.set_matrices(
            self.model_view_matrix, self.projection_matrix, self.viewport_matrix
        )

        # Set matrices for ObjectImage
        self.set_matrices(
            self.model_view_matrix, self.projection_matrix, self.viewport_matrix
        )

        # Set up ObjectImage and zbuffer
        self.image = ObjectImage(self.width, self.height, ObjectColor)
        self.zbuffer = ObjectImage(self.width, self.height, ObjectColor)

        # Render the model using the shader
        self.shader_triangle(gouraud_shader)

        # Additional processing if needed

        # Flip images
        self.image.flip_vertically()
        self.zbuffer.flip_vertically()

        # Write to files
        self.image.write_file("output.tga")
        self.zbuffer.write_file("zbuffer.tga")

    def shader_triangle(self, shader):
        for i in range(self.model.nfaces()):
            screen_coords = [shader.vertex(i, j) for j in range(3)]
            self.triangle(screen_coords, shader)

    def triangle(self, pts, shader):
        bboxmin = Vector2(float("inf"), float("inf"))
        bboxmax = Vector2(-float("inf"), -float("inf"))

        for i in range(3):
            for j in range(2):
                bboxmin[j] = min(bboxmin[j], pts[i][j] / pts[i][3])
                bboxmax[j] = max(bboxmax[j], pts[i][j] / pts[i][3])

        P = Vector2()
        color = ObjectColor()

        for P.x in range(int(bboxmin.x), int(bboxmax.x) + 1):
            for P.y in range(int(bboxmin.y), int(bboxmax.y) + 1):
                bary_coords = self.barycentric(
                    proj(2, pts[0] / pts[0][3]),
                    proj(2, pts[1] / pts[1][3]),
                    proj(2, pts[2] / pts[2][3]),
                    proj(2, P),
                )
                if any(
                    coord < 0 or not isclose(coord, 0, abs_tol=1e-2)
                    for coord in bary_coords
                ):
                    continue

                z = sum(pts[i][2] * bary_coords[i] for i in range(3))
                w = sum(pts[i][3] * bary_coords[i] for i in range(3))
                frag_depth = max(0, min(255, int(z / w + 0.5)))

                if self.zbuffer.get(P.x, P.y)[0] > frag_depth:
                    continue

                discard = shader.fragment(bary_coords, color)

                if not discard:
                    self.zbuffer.set(P.x, P.y, ObjectColor(frag_depth))
                    self.image.set(P.x, P.y, color)

    def set(self, x, y, color):
        self.pixels[x, y] = [color.r, color.g, color.b, color.a]

    def get(self, x, y):
        return self.pixels[x, y]

    def read_file(self, filename: str) -> bool:
        """
        Read a Object image file and store it as a PIL Image.

        Parameters:
        - filename (str): The path to the Object image file.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            with Image.open(filename) as img:
                data = array(img)
                self.pixels = Image.fromarray(data)
            return True
        except (TypeError, ValueError, FileNotFoundError, UnidentifiedImageError) as e:
            raise ObjectImageError(str(e)) from e

    def write_file(self, filename: str) -> bool:
        """
        Write the current image to a Object image file.

        Parameters:
        - filename (str): The path to save the Object image file.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            self.pixels.save(filename)
            return True
        except (TypeError, ValueError, FileNotFoundError, UnidentifiedImageError) as e:
            raise ObjectImageError(str(e)) from e

    def flip_horizontally(self) -> bool:
        """
        Flip the image horizontally.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.pixels:
            self.pixels = Image.fromarray(fliplr(array(self.pixels)))
            return True
        return False

    def flip_vertically(self) -> bool:
        """
        Flip the image vertically.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.pixels:
            self.pixels = Image.fromarray(flipud(array(self.pixels)))
            return True
        return False


class ObjectModel:
    def __init__(self, filename: str):
        self.verts: list[Vector3] = []
        self.faces: list[list[tuple[int, int, int]]] = []
        self.norms: list[Vector3] = []
        self.uv: list[Vector2] = []
        self.diffusemap = ObjectImage(800, 600)
        self.normalmap = ObjectImage(800, 600)
        self.specularmap = ObjectImage(800, 600)

        # Load model data from the .obj file
        self.load_model_data(filename)

    def load_model_data(self, filename: str):
        vertices, normals, tex_coords, faces = self.load_obj(filename)

        # Load vertices
        self.verts = [Vector3(*vertex) for vertex in vertices]

        # Load normals
        self.norms = [Vector3(*normal) for normal in normals]

        # Load texture coordinates
        self.uv = [Vector2(*tex_coord) for tex_coord in tex_coords]

        # Load faces
        self.faces = faces

        # Load textures
        self.load_texture(filename, "_diffuse.tga", self.diffusemap)
        self.load_texture(filename, "_nm.tga", self.normalmap)
        self.load_texture(filename, "_spec.tga", self.specularmap)

    def load_texture(self, filename: str, suffix: str, img: ObjectImage):
        texfile = filename.split(".")[0] + suffix
        print(
            f"Texture file {texfile} loading {'ok' if img.read_file(texfile) else 'failed'}"
        )
        img.flip_vertically()

    def load_obj(
        self, filename: str
    ) -> tuple[
        list[tuple[float, float, float]],
        list[tuple[float, float, float]],
        list[tuple[float, float]],
        list[list[tuple[int, int, int]]],
    ]:
        vertices = []
        normals = []
        tex_coords = []
        faces = []

        with open(filename, "r") as file:
            for line in file:
                tokens = line.split()

                if not tokens:
                    continue

                if tokens[0] == "v":
                    vertices.append(tuple(map(float, tokens[1:4])))
                elif tokens[0] == "vn":
                    normals.append(tuple(map(float, tokens[1:4])))
                elif tokens[0] == "vt":
                    tex_coords.append(tuple(map(float, tokens[1:3])))
                elif tokens[0] == "f":
                    face = [
                        (
                            int(v.split("/")[0]) - 1,
                            int(v.split("/")[1]) - 1,
                            int(v.split("/")[2]) - 1,
                        )
                        for v in tokens[1:]
                    ]
                    faces.append(face)

        return vertices, normals, tex_coords, faces

    def nverts(self) -> int:
        return len(self.verts)

    def nfaces(self) -> int:
        return len(self.faces)

    def normal(self, iface: int, nthvert: int) -> Vector3:
        idx = self.faces[iface][nthvert][2]
        return self.norms[idx].normalize()

    def vert(self, i: int) -> Vector3:
        return self.verts[i]

    def vert(self, iface: int, nthvert: int) -> Vector3:
        return self.verts[self.faces[iface][nthvert][0]]

    def face(self, idx: int) -> list[int]:
        return [self.faces[idx][i][0] for i in range(len(self.faces[idx]))]

    def uv(self, iface: int, nthvert: int) -> Vector2:
        return self.uv[self.faces[iface][nthvert][1]]

    def diffuse(self, uvf: Vector2) -> ObjectImage:
        uv = Vector2(
            uvf.x * self.diffusemap.get_width(), uvf.y * self.diffusemap.get_height()
        )
        return self.diffusemap.get(int(uv.x), int(uv.y))

    def specular(self, uvf: Vector2) -> float:
        uv = Vector2(
            uvf.x * self.specularmap.get_width(), uvf.y * self.specularmap.get_height()
        )
        return self.specularmap.get(int(uv.x), int(uv.y))[0] / 1.0
