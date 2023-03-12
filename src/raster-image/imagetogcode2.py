#!/usr/bin/python
import os.path
import sys
import numpy
import matplotlib.image
from mecode import GMatrix
from mecode_helpers import get_gmatrix


def pen_down(g: GMatrix) -> None:
    """Lower the pen.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
    """



    # This command actually lowers the pen.
    g.write("M9")


def pen_up(g: GMatrix) -> None:
    """Raise the pen.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
    """



    # This command actually raises the pen.
    g.write("M8")




version = "0.1"

#pixel_size_mm = 2.0
pixel_size_mm = 0.2
half_pixel_size_mm = pixel_size_mm * 0.5
quarter_pixel_size_mm = pixel_size_mm * 0.25
fifth_pixel_size_mm = pixel_size_mm * 0.2

pen_up_gcode = "M8\n"
pen_down_gcode = "M9\n"

initial_gcode = "G21\nG91\nG92 X0 Y0 Z0\nF2000\nG01 X0 Y" + \
    str(half_pixel_size_mm) + " Z0\n"
final_gcode = "G28\n"

backwards = False

def advanceX(x_mm):
    global backwards
    gcode = " X"
    if (backwards):
        gcode += "-"
    gcode += str(x_mm)
    return gcode


def is_solid(pixel: float, threshold: float):
    # white = 1.0, black = 0.0
    return pixel.mean() < threshold


def help():
    print(
        "  Command: python imagetogcode.py image_filename [output_filename]\n")


def main():
    # argc = len(sys.argv)
    # print("Image to G-Code v" + version)

    # if (argc < 2):
    #     help()
    #     sys.exit(2)

    # image_filename = sys.argv[1]
    # if (not os.path.exists(image_filename)):
    #     print("File not found: " + image_filename)
    #     sys.exit(1)

    threshold = 0.8
    image_filename = "C:\\Users\\jinch\\Desktop\\Untitled-2.png"

    print("Reading image file: " + image_filename)
    img = matplotlib.image.imread(image_filename)
    height = len(img)
    width = len(img[0])
    channels = len(img[0][0])

    print("Width: " + str(width) + ", Height: " +
          str(height) + ", Channels: " + str(channels))

    # Initialise G-Code
    g = get_gmatrix("output1.gcode")

    # Move to a reasonable starting position
    pen_up(g)
    g.move(35, 30)

    # Plot image
    #gcode += drawTestImage()
    reverse = False
    for y in range(height-1, 0, -1):
        
        # Draw line
        draw_line(img, y, g, threshold, reverse)
        
        # Move to the next line
        g.move(y=pixel_size_mm)

        # Reverse direction after each line is drawn
        reverse = not reverse

    # Finish printing task
    pen_up(g)
    g.abs_move(210, 310) # Send out A4 paper 210x297 mm
    pen_down(g)


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



if __name__ == '__main__':
    main()
