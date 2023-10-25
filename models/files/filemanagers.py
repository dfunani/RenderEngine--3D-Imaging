from re import sub
from models.constants import Resolution


class FileManager():
    def __init__(self, filename: str, extension: str) -> None:
        self.filename = f'{FileManager.sanitize_filename(filename)}.{FileManager.sanitize_filename(extension, "")}'

    @staticmethod
    def sanitize_filename(filename: str, replacement_text: str = "_") -> str:
        # Define a regex pattern to match unwanted characters (e.g., spaces and special characters)
        pattern = r'[\\/:*?"<>|\.]'
        # Replace unwanted characters with an underscore
        sanitized_filename = sub(pattern, replacement_text, filename)
        return sanitized_filename

    def write(
        self, framebuffer: list, mode="wb", fileheader: bytes = "P6\n{} {}\n255\n"
    ):
        with open(self.filename, mode) as ofs:
            match mode:
                case "wb":
                    ofs.write(
                        fileheader.format(
                            Resolution.__WIDTH__, Resolution.__HEIGHT__
                        ).encode("utf-8")
                    )
                    for i in range(Resolution.__WIDTH__ * Resolution.__HEIGHT__):
                        for j in range(3):
                            ofs.write(
                                bytes(
                                    [int(250 * max(0.0, min(1.0, framebuffer[i][j])))]
                                )
                            )
