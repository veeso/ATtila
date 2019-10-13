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

import unittest

from os.path import dirname

from attila.esk import ESK, ESKValue

class TestParser(unittest.TestCase):
  """
    Test ATRuntime Environment commands preparation and evaluation
    NOTE: this tests doesn't test communicator!
  """

  def __init__(self, methodName):
    super().__init__(methodName)

  def test_esks_to_string(self):
    self.assertIsNotNone(ESK.get_esk_from_string("DEVICE"))
    self.assertIsNotNone(ESK.get_esk_from_string("BAUDRATE"))
    self.assertIsNotNone(ESK.get_esk_from_string("TIMEOUT"))
    self.assertIsNotNone(ESK.get_esk_from_string("BREAK"))
    self.assertIsNotNone(ESK.get_esk_from_string("AOF"))
    self.assertIsNotNone(ESK.get_esk_from_string("SET"))
    self.assertIsNotNone(ESK.get_esk_from_string("GETENV"))
    self.assertIsNotNone(ESK.get_esk_from_string("PRINT"))
    self.assertIsNotNone(ESK.get_esk_from_string("EXEC"))
    #Try to fail
    self.assertIsNone(ESK.get_esk_from_string("FOOBAR"))

  def tests_esks_to_eskvalue(self):
    self.assertIsNotNone(ESK.to_ESKValue(ESK.DEVICE, "/dev/ttyUSB0"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.BAUDRATE, 9600))
    self.assertIsNone(ESK.to_ESKValue(ESK.BAUDRATE, "ABC"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.TIMEOUT, 5))
    self.assertIsNone(ESK.to_ESKValue(ESK.TIMEOUT, "ABC"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "CRLF"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "LF"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "CR"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "NONE"))
    self.assertIsNone(ESK.to_ESKValue(ESK.BREAK, "ABC"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.AOF, "True"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.AOF, "False"))
    self.assertIsNone(ESK.to_ESKValue(ESK.AOF, "ABC"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.SET, "foo=bar"))
    self.assertIsNone(ESK.to_ESKValue(ESK.SET, "ABC"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.GETENV, "CSQ"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.PRINT, "SAMPLE TEXT"))
    self.assertIsNotNone(ESK.to_ESKValue(ESK.EXEC, "echo foobar"))

if __name__ == "__main__":
  unittest.main()
