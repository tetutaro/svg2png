# svg2png

convert svg to png using CairoSVG

- create a transparent png
    - of the specified color
    - of the specified size and resize svg appropriately

## Install

`> pip install "git+https://github.com/tetutaro/svg2png.git"`

## Usage

```
usage: svg2png [-h] [--size SIZE [SIZE]] [--color COLOR] [--png PNG] svg

convert svg to png using CairoSVG.

positional arguments:
  svg                   svg filepath you want to convert

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE [SIZE]    <size> or <width> <height> of png
                        default: the same as svg
  --color COLOR         HTML color (#RRGGBB)
                        default: #000000
  --png PNG             output png filepath
                        default: os.path.basename(svg).replace('.svg', '.png')
```
