#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py: Barren Land Analysis program
See README.md for details.

Args:
    none: use stdin to enter barren rectangles
Returns:
    All the fertile land area in square meters, sorted from smallest area to greatest, separated by a space.
Raises:
    SyntaxError when input data is invalid

     5
0 1 2 3 4 5
|-|-|-|-|-|
"""

import re
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


def parse_input():
    """
    Take in a string and return a list of pairs of coordinates

    >>> '{"0 292 399 307"}'
    [[0, 292, 399, 307]]
    >>> '{"48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547"}'
    [[48, 192, 351, 207],
     [48, 392, 351, 407],
     [120, 52, 135, 547],
     [260, 52, 275, 547]]
    """
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    line = '\n'.join(lines)

    # TODO: better error handling
    re_bracketed_set = r'\{.*?\}'
    re_rectangle = r'\d+\s+\d+\s+\d+\s+\d+'
    line = line.replace('\n', '')
    line = re.findall(re_bracketed_set, line)
    line = [re.findall(re_rectangle, x) for x in line]
    # line = line.strip('{}')
    # line = line.split(',')
    # line = [pairs.strip().strip('""') for pairs in line]
    line = [[rectangles.split() for rectangles in rect_set] for rect_set in line]
    line = [[[int(x) for x in rectangle] for rectangle in rect_set] for rect_set in line]

    # line = [[int(x) for x in pairs] for pairs in line]
    return line


def parse_output(fertile_areas):
    """ """
    print(' '.join(map(str, sorted(fertile_areas))))


def mark_barren(field, barren_rectangles):
    """
    Mark off the set of rectangles that contain the barren land from the field and return the altered field
    """
    for rectangle in barren_rectangles:
        # mnemonic assignment
        x_0, y_0, x_1, y_1 = rectangle
        for x in range(x_0, x_1 + 1):
            for y in range(y_0, y_1 + 1):
                field[x][y] = False
    return field


def flood_fill(field, coordinates):
    """
    Flood fill 4-ways with queue (https://en.wikipedia.org/wiki/Flood_fill)
    Args: boolean field (2D array) with barren marked, coordinates of a place to fill
    Returns: field with flooded area removed, size of area removed
    """
    if not field[coordinates[0]][coordinates[1]]:
        return field, 0
    # NOTE: queue is WAY slower than a set.  it hits every coordinate 4x vs up to 4x.
    # q = queue.Queue()
    # q.put(coordinates)
    # count = 0
    # while not q.empty():
    q = set()
    q.add(coordinates)
    count = 0
    while q:
        # n = q.get()
        n = q.pop()
        if field[n[0]][n[1]]:
            count += 1
            field[n[0]][n[1]] = False
            if n[0] >= 0:
                q.add((n[0] - 1, n[1]))  # up
            try:
                q.add((n[0] + 1, n[1]))  # down
            except IndexError:
                pass
            if n[1] >= 0:
                q.add((n[0], n[1] - 1))  # left
            try:
                q.add((n[0], n[1] + 1))  # right
            except IndexError:
                pass
    return field, count


def draw_field(field, field_size):
    """
    adapted from: https://stackoverflow.com/questions/53308708/how-to-display-an-image-from-a-numpy-array-in-tkinter
    """
    root = tk.Tk()
    array = np.ones(field_size) * 200 * field
    img = ImageTk.PhotoImage(image=Image.fromarray(array))
    canvas = tk.Canvas(root, height=field_size[0], width=field_size[1])
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=img)
    root.mainloop()


def main():
    """

    """
    # Assume bounds start at 0,0
    # field_bounds = [0, 0, 399, 599]
    field_size = (400, 600)
    rectangle_sets = parse_input()
    # barren_rectangles = parse_input()
    for barren_rectangles in rectangle_sets:
        field = np.ones(field_size, dtype=bool)
        field = mark_barren(field, barren_rectangles)

        # assorted tests
        # marked land
        # print(field)
        # draw_field(field, field_size)
        # arable land
        # print(np.sum(field))

        total = []
        for x in range(0, field_size[0]):
            for y in range(0, field_size[1]):
                if field[x][y]:
                    field, subtotal = flood_fill(field, (x, y))
                    total.append(subtotal)
        parse_output(total)


if __name__ == "__main__":
    main()
