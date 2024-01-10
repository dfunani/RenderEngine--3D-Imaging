WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image

def frame_buffer(width: int = WIDTH, height: int = HEIGHT):
    return [
        [[255, 255, 255] for _ in range(width)] for _ in range(height)
    ]  # Initialize image with white color