import numpy
import matplotlib.image
from mecode import GMatrix
from ..helpers.gmatrix_extensions import get_gmatrix, pen_up, pen_down


# Constants
pixel_size_mm = 0.2


def is_solid(pixel: float, threshold: float) -> bool:
    # white = 1.0, black = 0.0
    return pixel.mean() < threshold


def get_image(img_path: str) -> numpy.ndarray:
    print("Reading image file: " + img_path)
    img = matplotlib.image.imread(img_path)

    height = len(img)
    width = len(img[0])
    channels = len(img[0][0])
    print(f"Width: {str(width)}, Height: {str(height)}, Channels: {str(channels)}")

    return img


def draw_line(
        image: numpy.ndarray,
        y: int,
        g: GMatrix,
        threshold: float,
        reverse: bool = False):
    width = len(image[0])
    x_range = range(width-1, 0, -1) if reverse else range(width)
    x = x_range[0]
    while True:
        if reverse and x <= 0:
            return
        if not reverse and x >= width - 1:
            return
        
        # Skip white space
        x_next = next_solid_pixel(image, x, y, threshold, reverse)
        if x_next is None:
            # Go to the end of the line and finish
            x_next = 0 if reverse else width - 1
            g.move((x_next - x) * pixel_size_mm, 0, 0, rapid=True)
            return

        if x_next != x:
            g.move((x_next - x) * pixel_size_mm, 0, 0, rapid=True)
        x = x_next
        
        # Draw a segment
        pen_down(g)
        x_next = next_white_pixel(image, x, y, threshold, reverse)
        if x_next is None:
            # Go to the end of the line
            x_next = 0 if reverse else width - 1
            
        if x_next != x:
          g.move((x_next - x) * pixel_size_mm, 0, 0)
        pen_up(g)
        x = x_next


def next_solid_pixel(
    image: numpy.ndarray,
    x: int,
    y: int,
    threshold: float,
    reverse: bool = False
    ):
    
    width = len(image[0])
    x_range = range(x, -1, -1) if reverse else range(x, width)

    for x in x_range:
        pixel = image[y][x]
        if is_solid(pixel, threshold):
            return x
        
    return None


def next_white_pixel(
    image: numpy.ndarray,
    x: int,
    y: int,
    threshold: float,
    reverse: bool = False
    ):
    
    width = len(image[0])
    x_range = range(x, -1, -1) if reverse else range(x, width)

    for x in x_range:
        pixel = image[y][x]
        if not is_solid(pixel, threshold):
            return x
        
    return None


def convert_to_gcode(img_path: str, output_path: str, threshold: float) -> None:
    # Load image
    img = get_image(img_path)
    height = len(img)
    width = len(img[0])

    # Initialise G-Code writer
    g = get_gmatrix(output_path)

    # Move to a reasonable starting position
    pen_up(g)
    g.move(35, 30, rapid=True)

    # Plot image
    reverse = False
    for y in range(height-1, 0, -1):

        # Draw line
        draw_line(img, y, g, threshold, reverse)

        # Move to the next line
        g.move(y=pixel_size_mm, rapid=True)

        # Reverse direction after each line is drawn
        reverse = not reverse

    # Finish printing task
    pen_up(g)
    g.abs_move(210, 310, rapid=True)  # Send out A4 paper 210x297 mm
    pen_down(g)