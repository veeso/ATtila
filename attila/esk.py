# ATtila
# Developed by Christian Visintin
# 
# MIT License
# Copyright (c) 2019 Christian Visintin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from enum import Enum, auto

class ESKValue(object):
  """
  This class represents an Environment Setup Keyword value
  """

  def __init__(self, keyword, value):
    """
    Class constructor. Instantiates a new :class:`.ESKValue.` object with the provided paramters

    :param keyword: keyword type
    :param value associated
    :type keyword: ESK
    :type value: string
    """
    self._keyword = keyword
    self._value = value

  @property
  def keyword(self):
    return self._keyword

  @keyword.setter
  def keyword(self, kw):
    self._keyword = kw

  @property
  def value(self):
    return self._value

  @value.setter
  def expected_response(self, val):
    self._value = val


class ESK(Enum):
  """
  This class represents an Environment Setup Keyword
  """
  DEVICE = auto()
  BAUDRATE = auto()
  TIMEOUT = auto()
  BREAK = auto()
  AOF = auto()
  SET = auto()
  GETENV = auto()
  PRINT = auto()
  EXEC = auto()
