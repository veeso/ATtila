#!/usr/bin/python3

from setuptools import find_packages, setup
from pathlib import Path

# The directory containing this file
ROOT = Path(__file__).parent

# The text of the README file
README = (ROOT / "README.md").read_text()

setup(
  name='ATtila',
  version='1.0.0',
  description='Python module for to communicate easily with modems and rf modules using AT commands',
  long_description=README,
  long_description_content_type="text/markdown",
  author='Christian Visintin',
  author_email='christian.visintin1997@gmail.com',
  url='https://github.com/ChristianVisintin/ATtila',
  license="MIT",
  python_requires='>=3',
  install_requires=[
    'pyserial>=3'
  ],
  packages=find_packages(exclude=("tests",)),
  keywords=['AT commands', 'IOT', 'wireless', 'radio frequency', 'modem', 'rf modules'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Telecommunications Industry',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Software Development :: Libraries',
    'Topic :: Home Automation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
  ]
)
