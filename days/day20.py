import operator
import re
from collections import defaultdict
from functools import reduce
from typing import List, Dict

from utils.all import *

test1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

tile_re = re.compile(r"Tile (\d+):")

EDGE_TOP = 0
EDGE_LEFT = 1
EDGE_RIGHT = 2
EDGE_BOTTOM = 3


class Mosaic:
    def __init__(self, tiles):
        self.tiles: Dict[int, Tile] = {tile.id: tile for tile in tiles}
        # edge to id
        self.edges = defaultdict(list)
        # id to tiles
        self.raster = defaultdict(set)
        self.process_tiles()
        self.solve_mosaic()

    def process_tiles(self):
        for tile in self.tiles.values():
            for edge in tile.edges:
                self.edges[edge].append(tile.id)
                self.edges[edge[::-1]].append(tile.id)

    def solve_mosaic(self):
        for tile in self.tiles.values():
            for edge in tile.edges:
                for e in self.edges[edge]:
                    if e != tile.id:
                        self.raster[tile.id].add(e)
                for e in self.edges[edge[::-1]]:
                    if e != tile.id:
                        self.raster[tile.id].add(e)

    def edge_product(self):
        return reduce(operator.mul, (k for k, e in self.raster.items() if len(e) == 2))

    def create_image(self):
        """Figure out how to combine our raster"""
        CENTER = 4
        image = [[]] * 9
        tile_key = [[]] * 9
        corners = None
        for k, e, length in sorted(((k, e, len(e)) for k, e in self.raster.items()), reverse=True,
                                   key=lambda x: len(x[1])):
            if length == 4:
                image[CENTER] = self.tiles[k]
                tile_key[CENTER] = k
                top, left, right, bottom = self.tiles[k].edges
                for i, m, edge_search in [(-3, EDGE_BOTTOM, top), (-1, EDGE_RIGHT, left), (1, EDGE_LEFT, right),
                                          (3, EDGE_TOP, bottom)]:
                    for edge_id in e:
                        for side, search_edge in enumerate(self.tiles[edge_id].edges):
                            if edge_search == search_edge:
                                tile_key[CENTER + i] = edge_id
                                if m != side:
                                    self.tiles[edge_id].mirror()
                                    image[CENTER + i] = self.tiles[edge_id]
                                else:
                                    image[CENTER + i] = self.tiles[edge_id]
                # t3 (tx, ty, ex, ey)
                corners = ((0, {tile_key[1], tile_key[3]}, ((1, EDGE_LEFT, EDGE_RIGHT), (3, EDGE_TOP, EDGE_BOTTOM))),
                           (2, {tile_key[1], tile_key[5]}, ((1, EDGE_RIGHT, EDGE_LEFT), (5, EDGE_TOP, EDGE_BOTTOM))),
                           (6, {tile_key[7], tile_key[3]}, ((3, EDGE_BOTTOM, EDGE_TOP), (7, EDGE_LEFT, EDGE_RIGHT))),
                           (8, {tile_key[7], tile_key[5]}, ((5, EDGE_BOTTOM, EDGE_TOP), (7, EDGE_RIGHT, EDGE_LEFT))))
            # Solve corner cases
            elif length == 2:
                for c in corners:
                    if e == c[1]:
                        tile_key[c[0]] = k
                        tile_1, tile_2 = c[2]
                        # 0 id, 1 match edge, 2 search edge
                        # mirror or rotate tile match
                        matched_normal = self.check_regular(image, k, tile_1, tile_2)
                        if matched_normal:
                            image[c[0]] = matched_normal
                            break
                        matched_rotation = self.check_rotations(image, k, tile_1, tile_2)
                        if matched_rotation:
                            image[c[0]] = matched_normal
                            break
                        self.tiles[k].mirror()

                        matched_mirror = self.check_regular(image, k, tile_1, tile_2)
                        if matched_mirror:
                            image[c[0]] = matched_mirror
                            break
                        # reset mirror
                        matched_mirror_rotation = self.check_rotations(image, k, tile_1, tile_2)
                        if matched_mirror_rotation:
                            image[c[0]] = matched_mirror_rotation
                            break
                        # flip back
                        self.tiles[k].mirror()
                        self.tiles[k].flip()

                        matched_flip = self.check_regular(image, k, tile_1, tile_2)
                        if matched_flip:
                            image[c[0]] = matched_flip
                            break

                        matched_flip_rotation = self.check_rotations(image, k, tile_1, tile_2)
                        if matched_flip_rotation:
                            image[c[0]] = matched_flip_rotation
                            break

                        self.tiles[k].mirror()
                        matched_mirror_flip = self.check_regular(image, k, tile_1, tile_2)
                        if matched_mirror_flip:
                            image[c[0]] = matched_mirror_flip
                            break

                        matched_mirror_flip_rotation = self.check_rotations(image, k, tile_1, tile_2)
                        if matched_mirror_flip_rotation:
                            image[c[0]] = matched_mirror_flip_rotation
                            break

        return image

    def check_rotations(self, image, k, tile_1, tile_2):
        for edges in self.tiles[k].rotations():
            if edges:
                if edges[tile_1[2]] == image[tile_1[0]].edges[tile_1[1]] and \
                        edges[tile_2[2]] == \
                        image[tile_2[0]].edges[tile_2[1]]:
                    return self.tiles[k]

    def check_regular(self, image, k, tile_1, tile_2):
        if self.tiles[k].edges[tile_1[2]] == image[tile_1[0]].edges[tile_1[1]] and self.tiles[k].edges[tile_2[2]] == \
                image[tile_2[0]].edges[tile_2[1]]:
            return self.tiles[k]

    def print_image(self):
        tile_size = 10
        image = self.create_image()
        image_str = ""
        steps = list(range(0, 12, 3))

        for start, stop in [steps[i - 1:i + 1] for i in range(1, 4)]:
            for row in range(tile_size):
                for col in range(start, stop):
                    if image[col]:
                        image_str += image[col].tile[row % tile_size]
                    else:
                        image_str += ("." * tile_size)
                image_str += "\n"
        print(image_str)


class Tile(object):
    def __init__(self, _id, tile):
        self.id = _id
        self.tile: List[str] = tile
        self.edges = [""] * 4
        self.set_edges()

    def set_edges(self):
        """Edges are top, left, right, bottom"""
        # reset edges
        self.edges = [""] * 4
        self.edges[0] = self.tile[0]
        for row in self.tile:
            self.edges[1] += row[0]
            self.edges[2] += row[-1]
        self.edges[3] = self.tile[-1]

    def flip(self):
        self.tile = self.tile[::-1]
        self.set_edges()

    def mirror(self):
        for i, line in enumerate(self.tile):
            self.tile[i] = "".join(list(reversed(line)))
        self.set_edges()

    def rotate(self):
        data = [[char for char in line] for line in self.tile]
        for _ in range(3):
            # for each row
            for x in range(len(data)):
                # for each character
                for y in range(len(data[x])):
                    data[x][y] = self.tile[len(self.tile[x]) - y - 1][x]
        self.tile = ["".join(line) for line in data]
        self.set_edges()

    def rotations(self):
        for i in range(4):
            self.rotate()
            self.set_edges()
            yield self.edges


def parse_input(input_data: List[str]) -> Mosaic:
    tile_id = None
    tiles = defaultdict(list)
    processed_tiles = []
    for line in input_data:
        match = tile_re.match(line)
        if match:
            tile_id = int(match.group(1))
        else:
            if line:
                tiles[tile_id].append(line)
    for id, tile in tiles.items():
        processed_tiles.append(Tile(id, tile))
    return Mosaic(processed_tiles)


def part1(input_data: List[str]):
    mosaic = parse_input(input_data)
    return mosaic.edge_product()


def part2(input_data: List[str]):
    mosaic = parse_input(input_data)
    mosaic.print_image()


if __name__ == '__main__':
    advent.setup(2020, 20)
    fin = advent.get_input()
    input_data = fin.read()
    t1 = part1(test1.splitlines())
    assert t1 == 20899048083289
    # advent.submit_answer(1, part1(input_data.splitlines()))
    t2 = part2(test1.splitlines())
    print(t2)
