#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import List
from setuptools import setup
import svg2png


def read_requirements() -> List[str]:
    with open('requirements.txt', 'rt') as rf:
        required = rf.read().strip().splitlines()
    return required


setup(
    name='svg2png',
    version=svg2png.__version__,
    license='MIT',
    description='convert svg to png using CairoSVG',
    author='tetutaro',
    author_email='tetsutaro.maruyama@gmail.com',
    url='https://github.com/tetutaro/svg2png',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'svg2png = svg2png:main',
        ],
    },
    packages=[
        'svg2png',
    ]
)
