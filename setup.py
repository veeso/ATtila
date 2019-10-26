#!/usr/bin/python3

from setuptools import find_packages, setup, Extension
from pathlib import Path
from os import path

# The directory containing this file
ROOT = Path(__file__).parent

README = (ROOT / "README.md").read_text()

setup(
  name='attila',
  version='1.1.0',
  description='Python module to communicate easily with modems and RF modules using AT commands',
  long_description=README,
  long_description_content_type="text/markdown",
  author='Christian Visintin',
  author_email='christian.visintin1997@gmail.com',
  url='https://github.com/ChristianVisintin/ATtila',
  license="MIT",
  python_requires='>=3.4',
  include_package_data = True,
  install_requires=[
    'pyserial>=3'
  ],
  entry_points={
    'console_scripts': [
      'attila = attila.__main__:main'
    ]
  },
  packages=find_packages(exclude=("tests",)),
  keywords=['AT commands', 'IOT', 'wireless', 'radio frequency', 'modem', 'rf modules'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Telecommunications Industry',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Software Development :: Libraries',
    'Topic :: Home Automation',
    'Topic :: Communications :: Telephony',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
  ]
)
