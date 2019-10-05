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

class ATSerialPortError(Exception):
  """
  ATSerialPortError class provides an exception in case of an error on the serial port
  """

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr(self.message)

  def __repr__(self):
    return str(self.message)

class ATScriptNotFound(Exception):
  """
  ATScriptNotFound class provides an exception in case of an at script not found
  """

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr(self.message)

  def __repr__(self):
    return str(self.message)

class ATScriptSyntaxError(Exception):
  """
  ATScriptSyntaxError class provides an exception in case of a syntax error in an ATScript
  """

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr(self.message)

  def __repr__(self):
    return str(self.message)

class ATREUninitializedError(Exception):
  """
  ATREUninitializedError class provides an exception in case of uninitialized ATRE
  """

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr(self.message)

  def __repr__(self):
    return str(self.message)

class ATRuntimeError(Exception):
  """
  ATRuntimeError class provides an exception in case of a Runtime Error
  """

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr(self.message)

  def __repr__(self):
    return str(self.message)
