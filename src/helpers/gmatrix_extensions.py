from mecode import GMatrix


def pen_down(g: GMatrix, show_z_paths: bool = False) -> None:
    """Lower the pen.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
        show_z_paths (bool, optional): Whether to show the Z axis path. Defaults to False.
    """

    # This represents lowering the pen, but does not have any real effect as this plotter only prints in 2D.
    if show_z_paths:
        if g.is_relative:
            g.move(z=-3.3, rapid=True)
        else:
            g.move(x=g.current_position['x'], y=g.current_position['y'], z=0, rapid=True)

    # This command actually lowers the pen.
    g.write("M9")


def pen_up(g: GMatrix, show_z_paths: bool = False) -> None:
    """Raise the pen.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
        show_z_paths (bool, optional): Whether to show the Z axis path. Defaults to False.
    """

    # This represents raising the pen, but does not have any real effect as this plotter only prints in 2D.
    if show_z_paths:
        if g.is_relative:
            g.move(z=3.3, rapid=True)
        else:
            g.move(x=g.current_position['x'],
                y=g.current_position['y'], z=3.3, rapid=True)

    # This command actually raises the pen.
    g.write("M8")


def get_gmatrix(outfile: str = None) -> GMatrix:
    """Create a GMatrix instance and write the starting GCode.

    Args:
        outfile (str, optional): Path to the output file. Defaults to None.

    Returns:
        GMatrix: GMatrix instance.
    """

    start_code = "G91 ;relative\nG21 ;mm\nG92 X0 Y0 Z0 ;reset origin\nF2000;motion speed"
    g = GMatrix(outfile=outfile)
    g.push_matrix()
    g.write(start_code)
    return g
