"""Module providing ObjectImage class for handling TGA images."""

from os import listdir, remove
from pytest import raises
from models.images import ObjectImage

from models.types.exceptions import ObjectImageError

image = ObjectImage()


def test_image_init():
    """
    Test initialization of the ObjectImage class.

    The `image` attribute should be initially set to None.
    """
    assert not image.image


def test_image_read():
    """
    Test reading a TGA file into the ObjectImage instance.

    The `read_file` method should successfully read a TGA file,
    and the `image` attribute should be set accordingly.
    """
    assert image.read_file("tests/obj/african_head_diffuse.tga")
    assert image.image


def test_image_read_error():
    """
    Test handling an error when reading an unknown TGA file.

    The `read_file` method should raise an ObjectImageError when attempting
    to read a TGA file that does not exist or is of an unknown format.
    """
    with raises(ObjectImageError):
        assert image.read_file("tests/obj/unknown.tga")


def test_image_write():
    """
    Test writing the ObjectImage instance to a TGA file.

    The `write_file` method should successfully write the image to a TGA file,
    and the file should be present in the specified output directory.
    """
    assert image.write_file("tests/output/african_head_diffuse.tga")
    assert "african_head_diffuse.tga" in listdir("tests/output/")
    remove("tests/output/african_head_diffuse.tga")


def test_image_write_error():
    """
    Test handling an error when writing to an unknown file format.

    The `write_file` method should raise an ObjectImageError when attempting
    to write the ObjectImage instance to a file with an unknown format.
    """
    with raises(ObjectImageError):
        assert image.write_file("tests/output/unknown.obj")
