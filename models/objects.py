"""
Module Summary: Contains a class for handling 3D model data.

Returns:
    Classes:
        Model: Represents a 3D model loaded from an OBJ file.

Description:
    This module provides a class, Model, for handling 3D model data loaded from an OBJ file.
    The Model class includes methods for loading model data, retrieving vertices, faces,
    and converting 3D coordinates to 2D screen coordinates.

Classes:
    Model:
        Represents a 3D model loaded from an OBJ file.

        Attributes:
            verts (list[Vector3]): List of 3D vertices in the model.
            faces (list[Vector3]): List of faces, each represented by vertex indices.

        Methods:
            __init__: Initializes a Model object by loading data from an OBJ file.
            load_model: Loads model data from the specified OBJ file.
            get_vertex: Retrieves a 3D vertex by index.
            get_point: Converts a 3D vertex to a 2D screen coordinate.
            get_face: Retrieves a face by index.
            draw_model: Draw the 3D model on an image with shading 
            based on light direction.
            get_normal: Get the normal vector and screen coordinates 
            for a given face.

Example:
    ```
    from models.vectors import Vector2, Vector3
    from utils.generators import WIDTH, HEIGHT

    model = Model("example.obj")
    vertex = model.get_vertex(1)
    screen_coord = model.get_point(vertex)
    print(f"Vertex 1: {vertex}, Screen Coordinate: {screen_coord}")
    ```

Note: This docstring assumes the existence of a valid OBJ 
file formatted with vertices ('v') and faces ('f').
"""

from models.primitives import Triangle
from models.vectors import Vector2, Vector3
from utils.generators import WIDTH, HEIGHT


class Model:
    """
    Represents a 3D model loaded from an OBJ file.

    Attributes:
        verts (list[Vector3]): List of 3D vertices in the model.
        faces (list[Vector3]): List of faces, each represented by vertex indices.

    Methods:
        __init__: Initializes a Model object by loading data from an OBJ file.
        load_model: Loads model data from the specified OBJ file.
        get_vertex: Retrieves a 3D vertex by index.
        get_point: Converts a 3D vertex to a 2D screen coordinate.
        get_face: Retrieves a face by index.
        draw_model: Draw the 3D model on an image with shading
        based on light direction.
        get_normal: Get the normal vector and screen coordinates
        for a given face.

    Example:
        ```
        from models.vectors import Vector2, Vector3
        from utils.generators import WIDTH, HEIGHT

        model = Model("example.obj")
        vertex = model.get_vertex(1)
        screen_coord = model.get_point(vertex)
        print(f"Vertex 1: {vertex}, Screen Coordinate: {screen_coord}")
        ```
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes a Model object by loading data from an OBJ file.

        Args:
            filename (str): The filename of the OBJ file.
        """
        self.verts: list[Vector3] = []
        self.faces: list[Vector3] = []
        self.load_model(filename)

    def load_model(self, filename: str) -> None:
        """
        Loads model data from the specified OBJ file.

        Args:
            filename (str): The filename of the OBJ file.
        """
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue  # Skip empty lines

                if parts[0] == "v":
                    # Vertex line
                    x, y, z = map(float, parts[1:])
                    self.verts.append(Vector3(x, y, z))
                elif parts[0] == "f":
                    # Face line
                    indices = [int(idx.split("/")[0]) for idx in parts[1:]]
                    self.faces.append(Vector3(*indices))

    def get_vertex(self, index: int) -> Vector3:
        """
        Retrieves a 3D vertex by index.

        Args:
            index (int): The index of the vertex.

        Returns:
            Vector3: The 3D vertex.
        """
        return self.verts[index - 1]  # Vertices in OBJ files are 1-indexed

    def get_point(self, v: Vector3) -> Vector2:
        """
        Converts a 3D vertex to a 2D screen coordinate.

        Args:
            v (Vector3): The 3D vertex.

        Returns:
            Vector2: The 2D screen coordinate.
        """
        return Vector2((v.x + 1.0) * WIDTH / 2.0, (v.y + 1.0) * HEIGHT / 2.0)

    def get_face(self, index: int) -> Vector3:
        """
        Retrieves a face by index.

        Args:
            index (int): The index of the face.

        Returns:
            Vector3: The face represented by vertex indices.
        """
        return self.faces[index - 1]  # Faces in OBJ files are 1-indexed

    def draw_model(self, image: list, color) -> list:
        """
        Draw the 3D model on an image with shading based on light direction.

        Args:
            image (list): The image representation as a list.
            color: Color of the model.

        Returns:
            list: The updated image with the shaded model.

        Note:
            The light direction is assumed to be coming from (0, 0, -1).

        """
        light_dir = Vector3(0, 0, -1)

        for face_index in range(1, len(self.faces) + 1):  # Faces are 1-indexed
            face = self.get_face(face_index)
            normal, screen_coordinates = self.get_normal(face)
            normal.normalize()

            # Calculate the intensity of the light on the triangle
            intensity = normal.dot(light_dir)

            if intensity > 0:
                # Create a shaded triangle and draw it on the image
                shaded_triangle = Triangle(
                    screen_coordinates[0],
                    screen_coordinates[1],
                    screen_coordinates[2],
                    color,
                )
                image = shaded_triangle.draw_triangle(image)
        return image

    def get_normal(self, face: Vector3):
        """
        Get the normal vector and screen coordinates for a given face.

        Args:
            face (Vector3): The face represented by vertex indices.

        Returns:
            tuple: A tuple containing the normal vector and screen coordinates.

        """
        screen_coordinates: list[Vector2] = []
        world_coordinates: list[Vector3] = []

        # Convert 3D world coordinates to 2D screen coordinates
        for i in range(3):
            vertex = self.get_vertex(face[i])
            screen_coord = self.get_point(vertex)
            screen_coordinates.append(screen_coord)
            world_coordinates.append(vertex)

        # Calculate the normal vector for shading
        normal = (world_coordinates[2] - world_coordinates[0]) ^ (
            world_coordinates[1] - world_coordinates[0]
        )
        return normal, screen_coordinates
