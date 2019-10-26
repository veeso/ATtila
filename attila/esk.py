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

from enum import Enum

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
    :type value: Any
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
  def value(self, val):
    self._value = val


class ESK(Enum):
  """
  This class represents an Environment Setup Keyword
  """
  DEVICE = 0
  BAUDRATE = 1
  TIMEOUT = 2
  BREAK = 3
  AOF = 4
  SET = 5
  GETENV = 6
  PRINT = 7
  EXEC = 8

  @staticmethod
  def get_esk_from_string(esk_string):
    """
    Get ESK enum value from its string representation

    :param esk_string
    :type esk_string: String
    :returns ESK or None if invalid
    """
    if esk_string == "DEVICE":
      return ESK.DEVICE
    elif esk_string == "BAUDRATE":
      return ESK.BAUDRATE
    elif esk_string == "TIMEOUT":
      return ESK.TIMEOUT
    elif esk_string == "BREAK":
      return ESK.BREAK
    elif esk_string == "AOF":
      return ESK.AOF
    elif esk_string == "SET":
      return ESK.SET
    elif esk_string == "GETENV":
      return ESK.GETENV
    elif esk_string == "PRINT":
      return ESK.PRINT
    elif esk_string == "EXEC":
      return ESK.EXEC
    else:
      return None

  @staticmethod
  def to_ESKValue(esk, attr):
    """
    Check if attributes for this esk have a valid syntax

    :param esk
    :param attr
    :type esk: ESK
    :type attr: String
    :returns ESKValue (None in case of errors)
    """
    if not esk:
      return False
    elif esk is ESK.DEVICE:
      if attr:
        return ESKValue(esk, attr)
      else:
        return None
    elif esk is ESK.BAUDRATE:
      try:
        baud = int(attr)
        return ESKValue(esk, baud)
      except ValueError: #NaN
        return None
    elif esk is ESK.TIMEOUT:
      try:
        timeout = int(attr)
        return ESKValue(esk, timeout)
      except ValueError: #NaN
        return None
    elif esk is ESK.BREAK:
      if attr == "LF":
        return ESKValue(esk, "\n")
      elif attr == "CRLF":
        return ESKValue(esk, "\r\n")
      elif attr == "CR":
        return ESKValue(esk, "\r")
      elif attr == "NONE":
        return ESKValue(esk, None)
      else:
        return None
    elif esk is ESK.AOF:
      check = attr.lower()
      if check == "true":
        return ESKValue(esk, True)
      elif check == "false":
        return ESKValue(esk, False)
      else:
        return None
    elif esk is ESK.SET:
      key_val = attr.split("=")
      if len(key_val) == 2:
        return ESKValue(esk, (key_val[0], key_val[1])) #Tuple of key and value
      else:
        return None
    elif esk is ESK.GETENV:
      if attr:
        return ESKValue(esk, attr)
      else:
        return None
    elif esk is ESK.PRINT:
      if attr:
        return ESKValue(esk, attr)
      else:
        return None
    elif esk is ESK.EXEC:
      if attr:
        return ESKValue(esk, attr)
      else:
        return None
    else:
      return None
