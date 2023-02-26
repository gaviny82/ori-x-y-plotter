#!/usr/bin/python
import os.path
import sys
import numpy
import matplotlib.image

version = "0.1"

#pixel_size_mm = 2.0
pixel_size_mm = 0.2
half_pixel_size_mm = pixel_size_mm * 0.5
quarter_pixel_size_mm = pixel_size_mm * 0.25
fifth_pixel_size_mm = pixel_size_mm * 0.2

pen_up_gcode = "M8\n"
pen_down_gcode = "M9\n"

initial_gcode = "G21\nG91\nG92 X0 Y0 Z0\nF2000\nG01 X0 Y" + str(half_pixel_size_mm) + " Z0\n"
final_gcode = "G28\n"

pen_up = False
backwards = False

def penUp():
  global pen_up
  gcode = ""
  if (not pen_up):
    gcode = pen_up_gcode
    pen_up = True
  return gcode

def penDown():
  global pen_up
  gcode = ""
  if (pen_up):
    gcode = pen_down_gcode
    pen_up = False
  return gcode

def advanceY():
  global backwards
  gcode = penUp()
  gcode += "G01 X0 Y" + str(pixel_size_mm) + " Z0\n"
  backwards = not backwards
  return gcode

def advanceX(x_mm):
  global backwards
  gcode = " X"
  if (backwards):
    gcode += "-"
  gcode += str(x_mm)
  return gcode

def drawSpace():
  global backwards
  gcode = penUp()
  gcode += "G00"
  gcode += advanceX(pixel_size_mm)
  gcode += " Y0 Z0\n"
  return gcode

def drawPixel1():
  global backwards
  gcode = penDown()
  gcode += "G01"
  gcode += advanceX(pixel_size_mm)
  gcode += " Y0 Z0\n"
  return gcode

def drawPixel2():
  global backwards
  gcode = penDown()
  gcode += "G01"
  gcode += advanceX(quarter_pixel_size_mm)
  gcode += " Y" + str(quarter_pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(half_pixel_size_mm)
  gcode += " Y-" + str(half_pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(quarter_pixel_size_mm)
  gcode += " Y" + str(quarter_pixel_size_mm) + " Z0\n"
  return gcode

def drawPixel3():
  global backwards
  gcode = penDown()
  gcode += "G01"
  gcode += advanceX(fifth_pixel_size_mm)
  gcode += " Y" + str(half_pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(fifth_pixel_size_mm)
  gcode += " Y-" + str(pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(fifth_pixel_size_mm)
  gcode += " Y" + str(pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(fifth_pixel_size_mm)
  gcode += " Y-" + str(pixel_size_mm) + " Z0\n"
  gcode += "G01"
  gcode += advanceX(fifth_pixel_size_mm)
  gcode += " Y" + str(half_pixel_size_mm) + " Z0\n"
  return gcode

def drawPixel(pixel):
  #print(pixel)

  #value = numpy.mean(pixel)
  value = pixel[0]

  #if (value <= 0.25):
  #  gcode = drawPixel3()
  #elif (value <= 0.5):
  #  gcode = drawPixel2()
  #elif (value <= 0.95):
  #  gcode = drawPixel1()
  #else:
  #  gcode = drawSpace()
  
  # if (value > 0.95):
  #   gcode = drawSpace()
  # elif (value > 0.85):
  #   gcode = drawPixel1()
  # elif (value > 0.65):
  #   gcode = drawPixel2()
  # else:
  #   gcode = drawPixel3()

  if (value > 0.90):
    gcode = drawSpace()
  else:
    gcode = drawPixel1()

  return gcode

def drawTestImage():
  gcode = ""
  gcode += drawSpace() + drawSpace() + drawPixel3() + drawPixel3() + drawSpace() + drawPixel3()
  gcode += advanceY()
  gcode += drawSpace() + drawSpace() + drawPixel2() + drawPixel2() + drawSpace() + drawPixel2()
  gcode += advanceY()
  gcode += drawSpace() + drawSpace() + drawPixel1() + drawPixel1() + drawSpace() + drawPixel1()
  gcode += advanceY()
  gcode += drawSpace() + drawSpace() + drawPixel1() + drawPixel2() + drawPixel3() + drawSpace()
  return gcode

def help():
  print("  Command: python imagetogcode.py image_filename [output_filename]\n")

def main():
  argc = len(sys.argv)
  print("Image to G-Code v" + version)

  if (argc < 2):
    help()
    sys.exit(2)

  image_filename = sys.argv[1]
  if (not os.path.exists(image_filename)):
    print("File not found: " + image_filename)
    sys.exit(1)

  print("Reading image file: " + image_filename)
  img = matplotlib.image.imread(image_filename)
  height = len(img)
  width = len(img[0])
  channels = len(img[0][0])

  print("Width: " + str(width) + ", Height: " + str(height) + ", Channels: " + str(channels))

  # Initialise G-Code
  gcode = initial_gcode
  gcode += penUp()

  # Plot image
  #gcode += drawTestImage()
  reverse = False
  for y in range(height-1, 0, -1):
    if (reverse):
      for x in range(width-1, -1, -1):
        gcode += drawPixel(img[y][x])
    else:
      for x in range(width):
        gcode += drawPixel(img[y][x])

    gcode += advanceY()
    reverse = not reverse

  # Finalise G-Code
  gcode += penUp()
  gcode += final_gcode

  if (argc > 2):
    output_filename = sys.argv[2]
    file = open(output_filename, "w+")
    print("Writing GCode to: " + output_filename)
    file.write(gcode)
    file.close()
  else:
    print(gcode)


if __name__ == '__main__':
  main()
