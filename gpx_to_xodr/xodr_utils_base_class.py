"""
Released under the following license
https://github.com/xqgex/SecurityofCyberPhysicalSystems_Formats/blob/main/LICENSE
"""

from abc import ABC
from typing import List


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class Route(ABC, List[Point]):
    ...
