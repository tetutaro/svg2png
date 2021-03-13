#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import List, Optional
import os
import re
from argparse import (
    ArgumentParser, RawTextHelpFormatter,
    Action, Namespace, ArgumentTypeError
)
import numpy as np
from cairosvg import svg2png
from PIL import Image


class Converter(object):
    def _load_svg(self: Converter, svg: str) -> None:
        if not svg.endswith('.svg'):
            raise ValueError(f'you have to indicate svg file ({svg})')
        if not os.path.isfile(svg):
            raise ValueError(f'svg file is not found ({svg})')
        tmpfile = '.tmp.png'
        svg2png(url=svg, write_to=tmpfile)
        self.image = Image.open(tmpfile)
        os.remove(tmpfile)
        return

    def _load_size(
        self: Converter,
        size: Optional[List[int, int]]
    ) -> None:
        assert self.image is not None
        if size is None:
            self.scale = 1
            self.re_size = None
            self.offset = (0, 0)
            self.new_size = None
            return
        assert len(size) == 2
        if size[0] <= 0:
            raise ValueError(f'width must be > 0 ({size})')
        if size[1] <= 0:
            raise ValueError(f'height must be > 0 ({size})')
        self.scale = min(
            size[0] / self.image.size[0],
            size[1] / self.image.size[1]
        )
        self.re_size = (
            int(self.image.size[0] * self.scale),
            int(self.image.size[1] * self.scale)
        )
        self.offset = (
            (size[0] - self.re_size[0]) // 2,
            (size[1] - self.re_size[1]) // 2
        )
        self.new_size = tuple(size)
        return

    def _load_color(self: Converter, color: Optional[str]) -> None:
        if color is None:
            self.new_color = None
            return
        if not re.match(r'^#?[0-9a-fA-F]+$', color):
            raise ValueError(f'invalid charactor of color ({color})')
        value = color.lstrip('#').lower()
        lenv = len(value)
        if lenv not in [3, 6]:
            raise ValueError(f'color should be #RGB or #RRGGBB ({color})')
        step = lenv // 3
        rgba = list()
        for i in range(0, lenv, step):
            v = value[i:i + step]
            if step == 1:
                v = v * 2
            rgba.append(int(v, 16))
        rgba.append(0)
        self.new_color = tuple(rgba)
        return

    def _set_png(self: Converter, svg: str, png: Optional[str]) -> None:
        if png is None:
            self.output = os.path.basename(svg).replace('.svg', '.png')
        else:
            if not png.endswith('.png'):
                raise ValueError('output must be XXX.png ({png})')
            self.output = png
        return

    def __init__(
        self: Converter,
        svg: str,
        size: Optional[List[int, int]],
        color: Optional[str],
        png: Optional[str]
    ) -> None:
        self.image = None
        self._load_svg(svg=svg)
        self._load_size(size=size)
        self._load_color(color=color)
        self._set_png(svg=svg, png=png)
        self.colored = None
        self.resized = None
        self.new_image = None
        return

    def _color_image(self: Converter) -> None:
        assert self.image is not None
        if self.new_color is None:
            self.colored = self.image.copy()
            return
        colored = Image.new('RGBA', self.image.size, color=self.new_color)
        new_color_array = np.array(colored)
        new_color_array[..., 3] = np.array(self.image)[..., 3]
        self.colored = Image.fromarray(new_color_array, mode='RGBA')
        return

    def _resize_image(self: Converter) -> None:
        assert self.colored is not None
        if self.scale > 1:
            self.resized = self.colored.resize(
                self.re_size, resample=Image.BICUBIC
            )
        elif self.scale < 1:
            self.resized = self.colored.resize(
                self.re_size, resample=Image.LANCZOS
            )
        else:
            self.resized = self.colored.copy()
        return

    def _paste_image(self: Converter) -> None:
        assert self.resized is not None
        if self.offset[0] == 0 and self.offset[1] == 0:
            self.new_image = self.resized.copy()
            return
        if self.new_color is None:
            new_color = (0, 0, 0, 0)
        else:
            new_color = self.new_color
        self.new_image = Image.new('RGBA', self.new_size, color=new_color)
        self.new_image.paste(self.resized, self.offset)
        return

    def convert(self: Converter) -> None:
        self._color_image()
        self._resize_image()
        self._paste_image()
        return

    def save(self: Converter) -> None:
        assert self.new_image is not None
        self.new_image.save(self.output)
        print(f'save png in {self.output}')
        return


def size_or_width_height():
    class SizeOrWidthHeight(Action):
        def __call__(
            self: SizeOrWidthHeight,
            parser: ArgumentParser,
            namespace: Namespace,
            values: List,
            option_string: Optional[str] = None
        ) -> None:
            if not len(values) in [1, 2]:
                raise ArgumentTypeError(
                    'size must be SIZE or WIDTH HEIGHT'
                )
            if len(values) == 1:
                values *= 2
            setattr(namespace, self.dest, values)
            return
    return SizeOrWidthHeight


def main() -> None:
    parser = ArgumentParser(
        description='convert svg to png using CairoSVG',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        'svg', type=str,
        help='svg filepath you want to convert'
    )
    parser.add_argument(
        '--size', type=int, nargs='+', default=None,
        action=size_or_width_height(),
        help=(
            '<size> or <width> <height> of png\n'
            'default: the save as svg'
        )
    )
    parser.add_argument(
        '--color', type=str, default=None,
        help=(
            'HTML color (#RRGGBB)\n'
            'default: #000000'
        )
    )
    parser.add_argument(
        '--png', type=str, default=None,
        help=(
            'output png filepath\n'
            "default: os.path.basename(svg).replace('.svg', '.png')"
        )
    )
    try:
        args = parser.parse_args()
        converter = Converter(**vars(args))
        converter.convert()
        converter.save()
    except Exception as e:
        print(f'{e}')
    return


if __name__ == '__main__':
    main()
