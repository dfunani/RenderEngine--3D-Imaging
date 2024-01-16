"""
Module for TGAImage and Color classes.

This module provides functionality for reading, writing, and 
manipulating Truevision TGA image files.
"""

from typing import BinaryIO


class Color:
    """
    Represents a color with specified color channels and pixel information.

    Attributes:
    - red (int): Red channel value.
    - green (int): Green channel value.
    - blue (int): Blue channel value.
    - alpha (int): Alpha channel value.
    - value (int): Color value.
    - raw (bytearray): Raw representation of the color.
    - bytes_per_pixel (int): Bytes per pixel (1 or 4).

    Raises:
    - ValueError: If bytes_per_pixel is not 1 or 4.
    """

    def __init__(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
        alpha: int = 255,
        value: int = 0,
        bytes_per_pixel: int = 1,
    ) -> None:
        """
        Initialize Color with specified color channels and
        pixel information.

        Parameters:
        - red (int): Red channel value (default is 0).
        - green (int): Green channel value (default is 0).
        - blue (int): Blue channel value (default is 0).
        - alpha (int): Alpha channel value (default is 255).
        - value (int): Color value (default is 0).
        - bytes_per_pixel (int): Bytes per pixel (default
        is 1 or 4).

        Raises:
        - ValueError: If bytes_per_pixel is not 1 or 4.
        """
        self.blue = blue
        self.green = green
        self.red = red
        self.alpha = alpha
        self.raw = bytearray([0] * 4)
        self.value = value
        self.bytes_per_pixel = bytes_per_pixel

        if bytes_per_pixel not in [1, 4]:
            raise ValueError(
                "Invalid bytes_per_pixel value. Supported values are 1 and 4."
            )

        if value == 0:
            self.value = 0

    def copy(self) -> "Color":
        """
        Create a copy of the Color.

        Returns:
        - Color: Copy of the current Color instance.
        """
        return Color(
            self.red,
            self.green,
            self.blue,
            self.alpha,
            self.value,
            self.bytes_per_pixel,
        )

    def __eq__(self, other: "Color") -> bool:
        """
        Check if two Color instances are equal.

        Returns:
        - bool: True if equal, False otherwise.
        """
        return (
            self.bytes_per_pixel == other.bytes_per_pixel and self.value == other.value
        )

    def __ne__(self, other: "Color") -> bool:
        """
        Check if two Color instances are not equal.

        Returns:
        - bool: True if not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """
        Get a string representation of the Color.

        Returns:
        - str: String representation of the Color.
        """
        strings = []
        strings.extend([self.red, self.green, self.blue])
        strings.extend([self.alpha, self.value, self.bytes_per_pixel])
        return f"Color({strings})"

    def __setattr__(self, name: str, value: int) -> None:
        """
        Set an attribute value with range validation for color channels.

        Parameters:
        - name (str): Attribute name.
        - value (int): New value for the attribute.

        Raises:
        - ValueError: If color channel value is not in the range [0, 255].
        """
        if name in ["red", "green", "blue", "alpha"]:
            if not 0 <= value <= 255:
                raise ValueError("Color channel value should be in the range [0, 255].")
        super().__setattr__(name, value)

    @classmethod
    def from_raw(cls, pixel_data: list, bytes_per_pixel: int) -> "Color":
        """
        Create a Color instance from raw pixel data.

        Parameters:
        - pixel_data (list): List of pixel data.
        - bytes_per_pixel (int): Bytes per pixel.

        Returns:
        - Color: Color instance created from the raw pixel data.
        """
        color = cls()
        for i in range(bytes_per_pixel):
            color.raw[i] = pixel_data[i]
        return color


class Image:
    """
    Represents an image with specified width, height, and bytes per pixel.

    Attributes:
    - GRAYSCALE (int): Constant for grayscale image.
    - RGB (int): Constant for RGB image.
    - RGBA (int): Constant for RGBA image.
    - width (int): Image width.
    - height (int): Image height.
    - bytes_per_pixel (int): Number of bytes per pixel.
    - pixel_data (bytearray): Pixel data of the image.

    Methods:
    - read_image_file(filename: str) -> bool: Read image data from file.
    - write_image_file(filename: str, use_rle: bool = True) -> bool: Write image data to file.
    - load_rle_data(file: BinaryIO) -> bool: Load image data using run-length encoding.
    - unload_rle_data(file: BinaryIO) -> bool: Unload image data using run-length encoding.
    - flip_horizontally() -> bool: Flip the image horizontally.
    - flip_vertically() -> bool: Flip the image vertically.
    - get_pixel(x: int, y: int) -> Color: Get pixel color at given coordinates.
    - set_pixel(x: int, y: int, color: Color) -> bool: Set pixel color at given coordinates.
    - get_bytes_per_pixel() -> int: Get the number of bytes per pixel.
    - get_width() -> int: Get the image width.
    - get_height() -> int: Get the image height.
    - get_image_data() -> bytearray: Get the image pixel data.
    - clear_image(): Clear the image pixel data.
    - scale_image(new_width: int, new_height: int) -> bool: Scale the image to a new size.
    """

    GRAYSCALE = 1
    RGB = 3
    RGBA = 4

    def __init__(
        self, width: int = 0, height: int = 0, bytes_per_pixel: int = 0
    ) -> None:
        """
        Initialize Image object.

        Parameters:
        - width (int): Image width.
        - height (int): Image height.
        - bytes_per_pixel (int): Number of bytes per pixel.
        """
        self.pixel_data = None
        self.width = width
        self.height = height
        self.bytes_per_pixel = bytes_per_pixel

        if width > 0 and height > 0 and bytes_per_pixel > 0:
            data_size = width * height * bytes_per_pixel
            self.pixel_data = bytearray([0] * data_size)

    def __del__(self) -> None:
        """
        Destroyer for Image.
        """
        del self.pixel_data

    def read_image_file(self, filename: str) -> bool:
        """
        Read image from file.

        Parameters:
        - filename (str): Path to the image file.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            with open(filename, "rb") as file:
                header = file.read(18)

                if len(header) != 18:
                    print(f"Error: Couldn't read header from {filename}")
                    return False

                self.width = int.from_bytes(header[12:14], byteorder="little")
                self.height = int.from_bytes(header[14:16], byteorder="little")
                bits_per_pixel = header[16]

                # Calculate bytes per pixel based on bits per pixel
                self.bytes_per_pixel = bits_per_pixel // 8

                print(f"Width: {self.width}, Height: {self.height}, Bits per Pixel: {bits_per_pixel}, Bytes per Pixel: {self.bytes_per_pixel}")

                if (
                    self.width <= 0
                    or self.height <= 0
                    or (
                        self.bytes_per_pixel
                        not in [1, 3, 4]
                    )
                ):
                    print(
                        f"Error: Invalid width, height, or bytes per pixel in {filename}"
                    )
                    return False

                # Initialize pixel_data before reading data
                self.pixel_data = bytearray()

                data_size = self.width * self.height * self.bytes_per_pixel
                while len(self.pixel_data) < data_size:
                    chunk = file.read(data_size - len(self.pixel_data))
                    if not chunk:
                        print(f"Warning: Reached end of file before reading expected data size.")
                        break
                    self.pixel_data.extend(chunk)

                if not header[17] & 0x20:
                    self.flip_vertically()
                if header[17] & 0x10:
                    self.flip_horizontally()

                print(f"{self.width}x{self.height}/{bits_per_pixel}")
                return True

        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False



    def write_image_file(self, filename: str, use_rle: bool = True) -> bool:
        """
        Write image to file.

        Parameters:
        - filename (str): Path to the image file.
        - use_rle (bool): Use run-length encoding.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            with open(filename, "wb") as file:
                header = bytearray(18)
                header[:12] = b"TRUEVISION-XFILE"
                header[12:14] = (self.width).to_bytes(2, byteorder="little")
                header[14:16] = (self.height).to_bytes(2, byteorder="little")
                header[16] = self.bytes_per_pixel * 8
                header[17] = 0x20  # top-left origin
                file.write(header)

                if not use_rle:
                    file.write(self.pixel_data)
                else:
                    self.unload_rle_data(file)

                developer_area_ref = bytearray([0, 0, 0, 0])
                extension_area_ref = bytearray([0, 0, 0, 0])
                footer = b"TRUEVISION-XFILE."
                file.write(developer_area_ref)
                file.write(extension_area_ref)
                file.write(footer)

                return True

        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            return False

    def load_rle_data(self, file: BinaryIO) -> bool:
        """
        Load image data using run-length encoding.

        Parameters:
        - file (BinaryIO): The file object to read data from.

        Returns:
        - bool: True if successful, False otherwise.
        """
        pixelcount = self.width * self.height
        currentpixel = 0
        currentbyte = 0
        colorbuffer = Color()

        while currentpixel < pixelcount:
            chunkheader = file.read(1)
            if not chunkheader:
                print("Error: An error occurred while reading the data")
                return False

            chunkheader = ord(chunkheader)

            if chunkheader < 128:
                chunkheader += 1
                for _ in range(chunkheader):
                    colorbuffer.raw = file.read(self.bytes_per_pixel)
                    if not colorbuffer.raw:
                        print("Error: An error occurred while reading the header")
                        return False
                    for t in range(self.bytes_per_pixel):
                        self.pixel_data[currentbyte] = colorbuffer.raw[t]
                        currentbyte += 1
                    currentpixel += 1
                    if currentpixel > pixelcount:
                        print("Error: Too many pixels read")
                        return False
            else:
                chunkheader -= 127
                colorbuffer.raw = file.read(self.bytes_per_pixel)
                if not colorbuffer.raw:
                    print("Error: An error occurred while reading the header")
                    return False
                for _ in range(chunkheader):
                    for t in range(self.bytes_per_pixel):
                        self.pixel_data[currentbyte] = colorbuffer.raw[t]
                        currentbyte += 1
                    currentpixel += 1
                    if currentpixel > pixelcount:
                        print("Error: Too many pixels read")
                        return False

        return True

    def unload_rle_data(self, file: BinaryIO) -> bool:
        """
        Unload image data using run-length encoding.

        Parameters:
        - file (BinaryIO): Binary file object.

        Returns:
        - bool: True if successful, False otherwise.
        """
        max_chunk_length = 128
        npixels = self.width * self.height
        curpix = 0

        while curpix < npixels:
            chunkstart = curpix * self.bytes_per_pixel
            curbyte = curpix * self.bytes_per_pixel
            run_length = 1
            raw = True

            while curpix + run_length < npixels and run_length < max_chunk_length:
                succ_eq = all(
                    self.pixel_data[curbyte + t]
                    == self.pixel_data[curbyte + t + self.bytes_per_pixel]
                    for t in range(self.bytes_per_pixel)
                )
                curbyte += self.bytes_per_pixel

                if run_length == 1:
                    raw = not succ_eq

                if raw and succ_eq:
                    run_length -= 1
                    break

                if not raw and not succ_eq:
                    break

                run_length += 1

            curpix += run_length
            file.write(bytes([run_length - 1]) if raw else bytes([run_length + 127]))
            file.write(
                self.pixel_data[
                    chunkstart : chunkstart + run_length * self.bytes_per_pixel
                ]
                if raw
                else self.pixel_data[chunkstart : chunkstart + self.bytes_per_pixel]
            )

        return True

    def flip_horizontally(self) -> bool:
        """
        Flip the image horizontally.
        """
        if not self.pixel_data:
            return False

        half = self.width // 2
        for i in range(half):
            for j in range(self.height):
                c1 = self.get_pixel(i, j)
                c2 = self.get_pixel(self.width - 1 - i, j)
                self.set_pixel(i, j, c2)
                self.set_pixel(self.width - 1 - i, j, c1)

        return True

    def flip_vertically(self) -> bool:
        """
        Flip the image vertically.
        """
        if not self.pixel_data:
            return False

        bytes_per_line = self.width * self.bytes_per_pixel
        line = bytearray(bytes_per_line)
        half = self.height // 2

        for j in range(half):
            l1 = j * bytes_per_line
            l2 = (self.height - 1 - j) * bytes_per_line

            line[:] = self.pixel_data[l1 : l1 + bytes_per_line]
            self.pixel_data[l1 : l1 + bytes_per_line] = self.pixel_data[
                l2 : l2 + bytes_per_line
            ]
            self.pixel_data[l2 : l2 + bytes_per_line] = line

        return True

    def get_pixel(self, x: int, y: int) -> Color:
        """
        Get pixel color at given coordinates.

        Parameters:
        - x (int): X-coordinate.
        - y (int): Y-coordinate.

        Returns:
        - Color: Color of the pixel.
        """
        if not self.pixel_data or x < 0 or y < 0 or x >= self.width or y >= self.height:
            return Color()

        start_index = (x + y * self.width) * self.bytes_per_pixel
        return Color(
            self.pixel_data[start_index : start_index + self.bytes_per_pixel],
            self.bytes_per_pixel,
        )

    def set_pixel(self, x: int, y: int, color: Color) -> bool:
        """
        Set pixel color at given coordinates.

        Parameters:
        - x (int): X-coordinate.
        - y (int): Y-coordinate.
        - color (Color): Color to set.

        Returns:
        - bool: True if successful, False otherwise.
        """
        if not self.pixel_data or x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        start_index = (x + y * self.width) * self.bytes_per_pixel
        self.pixel_data[start_index : start_index + self.bytes_per_pixel] = color.raw
        return True

    def get_bytes_per_pixel(self) -> int:
        """
        Get the number of bytes per pixel.

        Returns:
        - int: Bytes per pixel.
        """
        return self.bytes_per_pixel

    def get_width(self) -> int:
        """
        Get the image width.

        Returns:
        - int: Image width.
        """
        return self.width

    def get_height(self) -> int:
        """
        Get the image height.

        Returns:
        - int: Image height.
        """
        return self.height

    def get_image_data(self) -> bytearray:
        """
        Get the image pixel data.

        Returns:
        - bytearray: Image pixel data.
        """
        return self.pixel_data

    def clear_image(self) -> None:
        """
        Clear the image pixel data.
        """
        self.pixel_data = bytearray(
            [0] * (self.width * self.height * self.bytes_per_pixel)
        )

    def scale_image(self, new_width: int, new_height: int) -> bool:
        """
        Scale the image to a new size.

        Parameters:
        - new_width (int): New width.
        - new_height (int): New height.

        Returns:
        - bool: True if successful, False otherwise.
        """
        if new_width <= 0 or new_height <= 0 or not self.pixel_data:
            return False

        new_data = bytearray([0] * (new_width * new_height * self.bytes_per_pixel))
        n_scanline = 0
        o_scanline = 0
        err_y = 0
        n_line_bytes = new_width * self.bytes_per_pixel
        o_line_bytes = self.width * self.bytes_per_pixel

        for _ in range(self.height):
            err_x = self.width - new_width
            n_x = -self.bytes_per_pixel
            o_x = -self.bytes_per_pixel

            for _ in range(self.width):
                o_x += self.bytes_per_pixel
                err_x += new_width

                while err_x >= self.width:
                    err_x -= self.width
                    n_x += self.bytes_per_pixel
                    new_data[
                        n_scanline + n_x : n_scanline + n_x + self.bytes_per_pixel
                    ] = self.pixel_data[
                        o_scanline + o_x : o_scanline + o_x + self.bytes_per_pixel
                    ]

                err_y += new_height
                o_scanline += o_line_bytes

                while err_y >= self.height:
                    if err_y >= self.height << 1:
                        new_data[
                            n_scanline + n_line_bytes : n_scanline + n_line_bytes * 2
                        ] = new_data[n_scanline : n_scanline + n_line_bytes]
                    err_y -= self.height
                    n_scanline += n_line_bytes

        self.pixel_data = new_data
        self.width = new_width
        self.height = new_height
        return True
