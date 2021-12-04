from typing import List

from sentinelhub import BBox, CRS


def getBbox(coord_list: List) -> BBox:
    bbox = []
    for i in (0, 1):
        res = sorted(coord_list, key=lambda x: x[i])
        bbox.append((res[0][i], res[-1][i]))
    return BBox(bbox=(bbox[0][0], bbox[1][0], bbox[0][1], bbox[1][1]), crs=CRS.WGS84)
