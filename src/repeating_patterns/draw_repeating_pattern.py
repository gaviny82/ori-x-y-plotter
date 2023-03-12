from mecode import GMatrix
from .draw_unit import draw_unit
from ..helpers.gmatrix_extensions import pen_up, pen_down


def draw_repeating_pattern(
        g: GMatrix,
        width: float,
        height: float,
        path: list[list[tuple[float, float]]],
        scale: float,
        repeat: tuple[int, int]
) -> None:
    """Draw a unit of the repeating pattern. This method assumes the pen is raised at the starting position when called.

    Args:
        g (GMatrix): GMatrix instance to use for GCode generation.
        width (float): Width of the pattern in mm. This is the distance moved in x-direction after each pattern is drawn.
        height (float): Height of the pattern in mm. This is the distance moved in y-direction after each line of patterns is drawn.
        path (list[list[tuple[float, float]]]): List of strokes to draw. Each stroke is a list of points.
        scale (float): Scale factor to apply to the pattern.
        repeat (tuple[int, int]): Number of times to repeat the pattern in the x and y directions, respectively.
    """

    # Check if there is any point in path that is outside the limit of width and height
    for stroke in path:
        for x, y in stroke:
            if x > width or y > height:
                raise ValueError("Path is outside the dimension limit")

    # Scale the pattern
    path = [[(x * scale, y * scale) for x, y in stroke] for stroke in path]
    width = width * scale
    height = height * scale

    # Check if the repeating pattern takes more space than the page
    # Page limit: 205x275 mm
    if width * repeat[0] > 205 or height * repeat[1] > 275:
        raise ValueError("Repeating pattern is outside the dimension limit")

    # Set to absolute mode for drawing repeating patterns
    g.absolute()

    # Draw the pattern from the current position
    x_initial = g.current_position['x']
    y_initial = g.current_position['y']
    x = x_initial
    y = y_initial
    for y_rep in range(repeat[1]):

        # Draw each row of the pattern
        for x_rep in range(repeat[0]):
            draw_unit(g, path)
            x += width
            g.abs_move(x, y, rapid=True)

        # Move to the next row
        x = x_initial
        y += height
        g.abs_move(x_initial, y, rapid=True)

    # Set to relative mode
    g.relative()
