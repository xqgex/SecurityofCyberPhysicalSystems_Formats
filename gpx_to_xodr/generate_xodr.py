"""
Released under the following license
https://github.com/xqgex/SecurityofCyberPhysicalSystems_Formats/blob/main/LICENSE
"""

from collections import namedtuple

from enum import Enum
from math import cos
from typing import List
from xml.etree import ElementTree

from xodr_utils_base_class import Point, Route
from xodr_utils_xml import build_footer, build_header, build_road

_Coordinate = namedtuple('_Coordinate', ['latitude', 'longitude'])

# Update the following variables:
_GPX_FILE_PATH = './example/route_TailOfTheDragon.gpx'
_MAP_IMAGES_FOLDER = './GoogleMap/OddlotMapImages/35.497000-83.944306satellite2525'
_MAP_CORNER_TOP_LEFT = _Coordinate(latitude=35.516726, longitude=-83.968387)
_MAP_CORNER_BOTTOM_RIGHT = _Coordinate(latitude=35.482971, longitude=-83.925888)
_MAP_NAME = 'TailOfTheDragon'
_MAP_ODDLOT_CENTER = _Coordinate(latitude=35.497000, longitude=-83.944306)
_XODR_FILE_PATH = './example/TailOfTheDragon.xodr'

_DEFAULT_BLOCK_SIZE = 13
_EARTH_RADIUS_KM = 6371
_IMAGE_EXT = 'png'
_IMAGE_NAME_PREFIX = 'image'
_IMAGE_SIZE = 128
_MAP_MAX_DISTANCE_FROM_CENTER = 1800
_NEW_LINE_CHAR = '\n'


class _Sign(Enum):
    NEGATIVE = '-'
    POSITIVE = ''

    def __str__(self) -> str:
        return self.value

    def flip(self) -> '_Sign':
        return _Sign.NEGATIVE if self is _Sign.POSITIVE else _Sign.POSITIVE


class _Point(Point):
    @classmethod
    def from_coordinate(cls, coordinate: _Coordinate) -> '_Point':
        x_average = (_MAP_CORNER_TOP_LEFT.latitude + _MAP_CORNER_BOTTOM_RIGHT.latitude) / 2
        x = _EARTH_RADIUS_KM * coordinate.longitude * cos(x_average)
        y = _EARTH_RADIUS_KM * coordinate.latitude
        return cls(x, y)


class _Route(Route):
    @classmethod
    def from_gpx_file(cls, gpx_file_path: str) -> '_Route':
        points = []
        screen_x_y = _ScreenXY()
        gpx = ElementTree.parse(gpx_file_path).getroot()
        for checkpoint in gpx.iter('{http://www.topografix.com/GPX/1/1}trkpt'):
            coordinate = _Coordinate(latitude=float(checkpoint.attrib['lat']), longitude=float(checkpoint.attrib['lon']))
            points.append(screen_x_y.x_y_for_earth_coordinate(coordinate))
        return cls(points)


class _ScreenXY:
    def __init__(self) -> None:
        self._earth_bottom_right = _Point.from_coordinate(_MAP_CORNER_BOTTOM_RIGHT)
        self._screen_bottom_right = _Point(x=_DEFAULT_BLOCK_SIZE * _IMAGE_SIZE, y=(1 - _DEFAULT_BLOCK_SIZE) * _IMAGE_SIZE)
        self._earth_top_left = _Point.from_coordinate(_MAP_CORNER_TOP_LEFT)
        self._screen_top_left = _Point(x=(1 - _DEFAULT_BLOCK_SIZE) * _IMAGE_SIZE, y=_DEFAULT_BLOCK_SIZE * _IMAGE_SIZE)

    @property
    def earth_height(self) -> float:
        return self._earth_top_left.y - self._earth_bottom_right.y

    @property
    def earth_width(self) -> float:
        return self._earth_top_left.x - self._earth_bottom_right.x

    @property
    def screen_height(self) -> float:
        return self._screen_top_left.y - self._screen_bottom_right.y

    @property
    def screen_width(self) -> float:
        return self._screen_top_left.x - self._screen_bottom_right.x

    @property
    def height_ratio(self) -> float:
        return self.screen_height / self.earth_height

    @property
    def width_ratio(self) -> float:
        return self.screen_width / self.earth_width

    def x_y_for_earth_coordinate(self, coordinate: _Coordinate) -> None:
        point = _Point.from_coordinate(coordinate)
        screen_x = self._screen_top_left.x + self.width_ratio * (point.x - self._earth_top_left.x)
        screen_y = self._screen_top_left.y + self.height_ratio * (point.y - self._earth_top_left.y)
        return _Point(x=screen_x, y=screen_y)


def _scenery() -> List[str]:
    map_images = []
    for quadrant in QUADRANTS:
        map_images += _scenery_block(x_sign=quadrant[0], y_sign=quadrant[1], start_id=len(map_images))
    return map_images


def _scenery_block(x_sign: _Sign, y_sign: _Sign, block_size: int=_DEFAULT_BLOCK_SIZE, start_id: int=0) -> List[str]:
    ret = []
    for i in range(block_size):
        for j in range(block_size):
            if (x_sign == _Sign.NEGATIVE and j == 0) or (y_sign.flip() == _Sign.NEGATIVE and i == 0):
                continue  # Skip `-0`
            x = f'{x_sign}{j * _IMAGE_SIZE}'
            y = f'{y_sign}{i * _IMAGE_SIZE}'
            image_id = f'map{start_id + i * block_size + j}'
            image_name = f'{_IMAGE_NAME_PREFIX}{x_sign}{j}{y_sign.flip()}{i}.{_IMAGE_EXT}'
            ret += ['    <scenery>',
                    f'        <map width="{_IMAGE_SIZE}" y="{y}" x="{x}" height="{_IMAGE_SIZE}" filename="{_MAP_IMAGES_FOLDER}/{image_name}" id="{image_id}"/>',
                    '    </scenery>']
    return ret


QUADRANTS = (
    (_Sign.NEGATIVE, _Sign.POSITIVE), (_Sign.POSITIVE, _Sign.POSITIVE),
    (_Sign.NEGATIVE, _Sign.NEGATIVE), (_Sign.POSITIVE, _Sign.NEGATIVE),
    )


if __name__ == '__main__':
    header = build_header(_MAP_NAME, _MAP_MAX_DISTANCE_FROM_CENTER)
    road = build_road(_Route.from_gpx_file(_GPX_FILE_PATH))
    scenery = _scenery()
    footer = build_footer()
    with open(_XODR_FILE_PATH, 'w') as outfile:
        outfile.write(_NEW_LINE_CHAR.join(header + road + scenery + footer))
