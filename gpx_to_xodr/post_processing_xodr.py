""" This script cuts the map according to the top right corner to match CARLA map limit.

Released under the following license
https://github.com/xqgex/SecurityofCyberPhysicalSystems_Formats/blob/main/LICENSE
"""

from typing import List
from xml.etree import ElementTree

from xodr_utils_base_class import Point, Route
from xodr_utils_xml import build_footer, build_header, build_road

# Update the following variables:
_INPUT_XODR_FILE_PATH = './example/TailOfTheDragon.xodr'
_MAP_NAME = 'TailOfTheDragon'
_OUTPUT_XODR_FILE_PATH = './example/TailOfTheDragon_sliced.xodr'

_MAX_MAP_SIZE = 1900  # CARLA max size is 2000
_MIN_DISTANCE_FROM_EDGE = 50
_NEW_LINE_CHAR = '\n'


class _Box:
    def __contains__(self, point: Point) -> bool:
        """ Note, The function takes into consideration the value of `_MIN_DISTANCE_FROM_EDGE`. """
        return self.is_point_inside_safe_boundaries(point)

    def __init__(self, top_right: Point, bottom_left: Point) -> None:
        self.bottom_left = bottom_left
        self.top_right = top_right

    def __str__(self) -> str:
        padding = ' ' * len(str(self.bottom_left))
        return f'\n{padding}┌──────────────────┐{self.top_right}\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{padding}│                  │\n' \
               f'{self.bottom_left}└──────────────────┘'

    def is_point_inside_safe_boundaries(self, point: Point) -> bool:
        """ Check if a given point is inside the box safe boundaries. """
        return self.bottom_left.x + _MIN_DISTANCE_FROM_EDGE <= point.x <= self.top_right.x - _MIN_DISTANCE_FROM_EDGE and \
               self.bottom_left.y + _MIN_DISTANCE_FROM_EDGE <= point.y <= self.top_right.y - _MIN_DISTANCE_FROM_EDGE

    @classmethod
    def from_top_right_corner(cls, top_right: Point) -> '_Box':
        bottom_left = Point(top_right.x - _MAX_MAP_SIZE, top_right.y - _MAX_MAP_SIZE)
        return cls(top_right=top_right, bottom_left=bottom_left)


def _align_the_map(input_points: List[Point]) -> List[Point]:
    max_x = max(p.x for p in input_points) + _MIN_DISTANCE_FROM_EDGE
    max_y = max(p.y for p in input_points) + _MIN_DISTANCE_FROM_EDGE
    map_box = _Box.from_top_right_corner(Point(max_x, max_y))
    points_filtered = [p for p in input_points if p in map_box]
    alignment_x = _shift_value(min(p.x for p in points_filtered), max(p.x for p in points_filtered))
    alignment_y = _shift_value(min(p.y for p in points_filtered), max(p.y for p in points_filtered))
    return [Point(p.x + alignment_x, p.y + alignment_y) for p in points_filtered]


def _load_points_from_xodr(file_path: str) -> List[Point]:
    xodr = ElementTree.parse(file_path).getroot()
    points = []
    for line in xodr.iter('geometry'):
        points.append(Point(float(line.attrib['x']), float(line.attrib['y'])))
    return points


def _shift_value(min_values: float, max_values: float) -> int:
    """
    To understand the logic, see the following one dimension example,

     -3 -2 -1  0  1  2  3  4  5  6  7  8  9 10 11
    ----------------------------------------------
    |  |AA|  |  |  |  |  |  |  |  |  |  |  |  |  |
    ----------------------------------------------

    new_max_x = (max(values) - min(values)) // 2 == ((11) - (-3)) // 2 == 7
    shift_value_x = new_max_x - max(values) = 7 - (11) == -4

    After increasing each index with `shift_value_x`, the data is:

     -7 -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7
    ----------------------------------------------
    |  |AA|  |  |  |  |  |  |  |  |  |  |  |  |  |
    ----------------------------------------------
    """
    return int(((max_values - min_values) // 2) - max_values)


if __name__ == '__main__':
    points = _align_the_map(_load_points_from_xodr(_INPUT_XODR_FILE_PATH))
    header = build_header(_MAP_NAME, _MAX_MAP_SIZE // 2)
    road = build_road(Route(points))
    footer = build_footer()
    with open(_OUTPUT_XODR_FILE_PATH, 'w') as outfile:
        outfile.write(_NEW_LINE_CHAR.join(header + road + footer))
