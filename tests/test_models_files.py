from models.files.filemanagers import FileManager
from os import listdir, remove
from models.objects.primitives import Object

def test_filemanager():
    filemanager: FileManager = FileManager("testing*filename", "test")
    assert filemanager.filename == "testing_filename.test"
    assert FileManager.sanitize_filename("testing**filename", "&&") == "testing&&&&filename"
    filemanager.write(Object.frameBuffer())
    assert "testing_filename.test" in listdir()
    remove("testing_filename.test")