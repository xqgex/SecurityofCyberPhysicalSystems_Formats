"""
Released under the following license
https://github.com/xqgex/SecurityofCyberPhysicalSystems_Formats/blob/main/LICENSE
"""

from datetime import datetime
from math import atan2, sqrt
from typing import List, Optional, Tuple

from xodr_utils_base_class import Point, Route

_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def _road_block(road: Point, next_road: Optional[Point], road_start: float) -> Tuple[float, List[str]]:
    if not next_road or road == next_road:
        return 0.0, []
    road_hdg = atan2(next_road.y - road.y, next_road.x - road.x) if next_road else 0.0
    road_length = sqrt(pow(road.x - next_road.x, 2) + pow(road.y - next_road.y, 2)) if next_road else 0.0
    return road_length, [f'            <geometry s="{road_start}" x="{road.x}" y="{road.y}" hdg="{road_hdg}" length="{road_length}">',
                         '                <line/>',
                         '            </geometry>']


def build_footer() -> List[str]:
    return ['</OpenDRIVE>']


def build_header(map_name: str, max_axis_value: float) -> List[str]:
    return ['<?xml version="1.0" encoding="UTF-8"?>',
            '<OpenDRIVE>',
            f'    <header name="{map_name}" date="{datetime.now().strftime(_DATETIME_FORMAT)}" revMajor="1" revMinor="2" version="1" north="{max_axis_value}" east="{max_axis_value}" south="-{max_axis_value}" west="-{max_axis_value}">',
#            f'        <geoReference><![CDATA[+lat_0={_MAP_ODDLOT_CENTER.latitude} +lon_0={_MAP_ODDLOT_CENTER.longitude}]]></geoReference>',
            f'        <geoReference><![CDATA[+proj=utm +zone=32 +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0]]></geoReference>',
            f'        <userData value="{map_name}" code="tile"/>',
            '    </header>']


def build_road(route: Route) -> List[str]:
    roads = []
    roads_length = 0.0
    for road_id, current_road in enumerate(route):
        next_road = route[road_id + 1] if road_id + 1 < len(route) else None
        loop_road_length, loop_road = _road_block(current_road, next_road, roads_length)
        roads += loop_road
        roads_length += loop_road_length
    prefix = [f'    <road name="Road 0" length="{roads_length}" id="0" junction="-1">',
              '        <type s="0" type="rural">',
              '            <speed max="50" unit="mph"/>',
              '        </type>',
              '        <planView>']
    suffix = ['        </planView>',
              '        <elevationProfile>',
              '            <elevation s="0" a="0" b="0" c="0" d="0"/>',
              '        </elevationProfile>',
              '        <lanes>',
              '            <laneOffset s="0" a="0" b="0" c="0" d="0"/>',
              '            <laneSection s="0">',
              '                <left>',
              '                    <lane type="driving" level="false" id="1">',
              '                        <width sOffset="0" a="3.1" b="0" c="0" d="0"/>',
              '                        <roadMark type="solid" sOffset="0" height="0" laneChange="none" width="0.125" weight="standard" material="standard" color="white"/>',
              '                        <userData>',
              '                            <vectorLane travelDir="backward"/>',
              '                        </userData>',
              '                    </lane>',
              '                </left>',
              '                <center>',
              '                    <lane type="none" level="false" id="0">',
              '                        <roadMark type="broken" sOffset="0" height="0" laneChange="none" width="0.125" weight="standard" material="standard" color="yellow"/>',
              '                    </lane>',
              '                </center>',
              '                <right>',
              '                    <lane type="driving" level="false" id="-1">',
              '                        <width sOffset="0" a="3.1" b="0" c="0" d="0"/>',
              '                        <roadMark type="solid" sOffset="0" height="0" laneChange="none" width="0.125" weight="standard" material="standard" color="white"/>',
              '                        <userData>',
              '                            <vectorLane travelDir="forward"/>',
              '                        </userData>',
              '                    </lane>',
              '                </right>',
              '            </laneSection>',
              '        </lanes>',
              '    </road>']
    return prefix + roads + suffix
