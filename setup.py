#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup
import svg2png

setup(
    name='svg2png',
    version=svg2png.__version__,
    license='MIT',
    description='convert svg to png using CairoSVG',
    author='tetutaro',
    author_email='tetsutaro.maruyama@gmail.com',
    url='https://github.com/tetutaro/svg2png',
    install_requires=[
        'CairoSVG',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'svg2png = svg2png:main',
        ],
    },
    packages=[
        'svg2png',
    ]
)
