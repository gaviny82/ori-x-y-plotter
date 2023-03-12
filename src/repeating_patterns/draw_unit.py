from mecode import GMatrix
from ..helpers.gmatrix_extensions import pen_up, pen_down


def draw_unit(g: GMatrix, path: list[list[tuple[float, float]]]) -> None:
    """Draw a unit of the repeating pattern. This method assumes the pen is raised at the starting position when called.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
        path (list[list[tuple[float, float]]]): List of strokes to draw. Each stroke is a list of points. The coordinates are relative to the current position.
    """

    # Set to absolute coordinates
    is_relative = g.is_relative
    if is_relative:
        g.absolute()

    # Convert path in relative coordinates to absolute coordinates, based on the current position
    # Important: make a copy of the path, so that the original path is not modified
    path = path.copy()
    current_x = g.current_position['x']
    current_y = g.current_position['y']
    for i, stroke in enumerate(path):
        path[i] = [(x + current_x, y + current_y)
                   for x, y in stroke]

    for stroke in path:
        # Move to the first point of the stroke and start drawing
        x0, y0 = stroke[0]
        g.abs_move(x0, y0)
        pen_down(g)

        # Draw the stroke by moving to each point
        for x, y in stroke[1:]:
            g.abs_move(x, y)

        # Finish drawing the stroke. Raise the pen to prepare for the next stroke.
        pen_up(g)

    # Restore the coordinate mode
    if is_relative:
        g.relative()
