G91 ;relative
G91 ;relative
G21 ;mm
G92 X0 Y0 Z0 ;reset origin
F2000;motion speed
G90 ;absolute
G1 X0.000000 Y10.000000 Z0.000000
G91 ;relative
G01 X0 Y0 Z-3.3
M9
G90 ;absolute
G1 X0.000000 Y10.000000 Z0.000000
G91 ;relative
G90 ;absolute
G1 X0.000000 Y0.000000 Z0.000000
G91 ;relative
G90 ;absolute
G1 X10.000000 Y0.000000 Z0.000000
G91 ;relative
M8
G01 X0 Y0 Z3.3