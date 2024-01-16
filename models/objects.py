"""
Module: model.py
This module defines the Model class for loading and representing 3D models.
"""

from models.vectors import Vector3f, Vector3i, Vector2f, Vector2i
from models.images import Image, Color


class Model:
    """
    Class representing a 3D model.

    Attributes:
        verts (List[Vector3f]): List of 3D vertices.
        faces (List[List[Vector3i]]): List of faces, where each face contains vertex/uv/normal indices.
        norms (List[Vector3f]): List of vertex normals.
        uv (List[Vector2f]): List of texture coordinates.
        diffusemap (Image): Image representing the diffuse texture map.

    Methods:
        __init__(filename: str) -> None:
            Constructor to initialize the Model object by loading the model from a file.

        load_model(filename: str) -> None:
            Load the model data from the specified file.

        load_texture(filename: str, suffix: str, img: Image) -> None:
            Load and set the texture for the model.

        nverts() -> int:
            Get the number of vertices in the model.

        nfaces() -> int:
            Get the number of faces in the model.

        face(idx: int) -> List[int]:
            Get the indices of vertices for the specified face.

        vert(i: int) -> Vector3f:
            Get the 3D coordinates of the vertex at the specified index.

        diffuse(uv: Vector2i) -> Color:
            Get the color from the diffuse texture map at the specified UV coordinates.

        uv(iface: int, nvert: int) -> Vector2i:
            Get the UV coordinates for a vertex in a face.

    """

    def __init__(self, filename: str) -> None:
        """
        Constructor to initialize the Model object by loading the model from a file.

        Args:
            filename (str): The path to the model file.
        """
        self.verts: list[Vector3f] = []
        self.faces: list[list[Vector3i]] = []  # Vector3i means vertex/uv/normal
        self.norms: list[Vector3f] = []
        self.uv: list[Vector2f] = []
        self.diffusemap: Image = Image()
        self.load_model(filename)

    def load_model(self, filename: str) -> None:
        """
        Load the model data from the specified file.

        Args:
            filename (str): The path to the model file.

        Returns:
            None
        """
        with open(filename, "r") as file:
            for line in file:
                # Strip leading and trailing whitespaces from the line
                line = line.strip()
                if not line:
                    # Skip empty lines
                    continue

                tokens = line.split()
                if not tokens:
                    # Skip lines with no tokens
                    continue

                if tokens[0] == "v":
                    vertex = Vector3f(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    self.verts.append(vertex)
                elif tokens[0] == "vn":
                    normal = Vector3f(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    self.norms.append(normal)
                elif tokens[0] == "vt":
                    uv = Vector2f(float(tokens[1]), float(tokens[2]))
                    self.uv.append(uv)
                elif tokens[0] == "f":
                    face = []
                    for i in range(1, len(tokens)):
                        indices = [int(idx) - 1 for idx in tokens[i].split("/")]
                        face.append(Vector3i(indices[0], indices[1], indices[2]))
                    self.faces.append(face)

        print(
            "# v# {}, f# {}, vt# {}, vn# {}".format(
                len(self.verts), len(self.faces), len(self.uv), len(self.norms)
            )
        )
        self.load_texture(filename, "_diffuse.tga", self.diffusemap)

    def load_texture(self, filename: str, suffix: str, img: Image) -> None:
        """
        Load and set the texture for the model.

        Args:
            filename (str): The path to the model file.
            suffix (str): The suffix for the texture file.
            img (Image): The Image object to store the texture.

        Returns:
            None
        """
        texfile = filename.split(".")[0] + suffix
        print(texfile)
        print(
            "texture file {} loading {}".format(
                texfile, "ok" if img.read_image_file(texfile) else "failed"
            )
        )
        img.flip_vertically()

    def nverts(self) -> int:
        """
        Get the number of vertices in the model.

        Returns:
            int: Number of vertices.
        """
        return len(self.verts)

    def nfaces(self) -> int:
        """
        Get the number of faces in the model.

        Returns:
            int: Number of faces.
        """
        return len(self.faces)

    def face(self, idx: int) -> list[int]:
        """
        Get the indices of vertices for the specified face.

        Args:
            idx (int): Index of the face.

        Returns:
            list[int]: list of vertex indices.
        """
        return [vertex[0] for vertex in self.faces[idx]]

    def vert(self, i: int) -> Vector3f:
        """
        Get the 3D coordinates of the vertex at the specified index.

        Args:
            i (int): Index of the vertex.

        Returns:
            Vector3f: 3D coordinates of the vertex.
        """
        return self.verts[i]

    def diffuse(self, uv: Vector2i) -> Color:
        """
        Get the color from the diffuse texture map at the specified UV coordinates.

        Args:
            uv (Vector2i): UV coordinates.

        Returns:
            Color: Color from the texture map.
        """
        return self.diffusemap.get(uv.x, uv.y)

    def get_uv(self, iface: int, nvert: int) -> Vector2i:
        """
        Get the UV coordinates for a vertex in a face.

        Args:
            iface (int): Index of the face.
            nvert (int): Index of the vertex in the face.

        Returns:
            Vector2i: UV coordinates.
        """
        idx = self.faces[iface][nvert][1]
        return Vector2i(
            int(self.uv[idx].x * self.diffusemap.get_width()),
            int(self.uv[idx].y * self.diffusemap.get_height()),
        )
