# Simple rotating pattern
#
# arguments:
#  [1] = angle in degrees (=130)
#  [2] = line count (=40)
#  [3] = line length (=50)
#
# Usage: python gcodepattern01.py <angle> <count> <length>
#

import sys
import math
from mecode import GMatrix

# Useful GCode snippets
pen_up_gcode = "M8\nG01 X0 Y0 Z3.3"
pen_down_gcode = "G01 X0 Y0 Z-3.3\nM9"
start_code = "G91 ;relative\nG21 ;mm\nG92 X0 Y0 Z0 ;reset origin\nF2000 ;motion speed"
end_code = ""

# Extract program parameters, with defaults
argc = len(sys.argv)
angle_deg = 130 if argc <= 1 else float(sys.argv[1])
count     =  40 if argc <= 2 else   int(sys.argv[2])
length    =  50 if argc <= 3 else float(sys.argv[3])

# Calculate further working parameters
offset = length * 1.25
angle = math.pi * angle_deg / 180.0

# Initialise GCode generation and write start code
g = GMatrix()
g.push_matrix()
g.write(start_code)

# Move the pen to a reasonable starting position
g.write(pen_up_gcode)
g.move(offset, offset)
g.write(pen_down_gcode)

# Draw the pattern
for i in range(count):
    g.move(length, 0)
    g.rotate(angle)

# Write end code
g.pop_matrix()
g.write(end_code)
