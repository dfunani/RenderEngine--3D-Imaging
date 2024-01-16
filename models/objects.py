from models.images import ObjectImage
from models.vectors import Vector2, Vector3


class Model:
    def __init__(self, filename: str):
        self.verts: list[Vector3] = []
        self.faces: list[list[tuple[int, int, int]]] = []
        self.norms: list[Vector3] = []
        self.uv: list[Vector2] = []
        self.diffusemap = ObjectImage()
        self.normalmap = ObjectImage()
        self.specularmap = ObjectImage()

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
