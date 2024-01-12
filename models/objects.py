class Model:
    def __init__(self, filename: str) -> None:
        self.verts = []
        self.faces = []
        self.load_model(filename)

    def load_model(self, filename: str) -> None:
        with open(filename, "r") as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue  # Skip empty lines

                if parts[0] == "v":
                    # Vertex line
                    x, y, z = map(float, parts[1:])
                    self.verts.append((x, y, z))
                elif parts[0] == "f":
                    # Face line
                    indices = [int(idx.split("/")[0]) for idx in parts[1:]]
                    self.faces.append(indices)

    def get_vertex(self, index: int) -> tuple:
        return self.verts[index - 1]  # Vertices in OBJ files are 1-indexed

    def get_face(self, index: int) -> list:
        return self.faces[index - 1]  # Faces in OBJ files are 1-indexed
