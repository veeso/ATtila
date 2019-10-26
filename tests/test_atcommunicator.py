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
from attila.atcommunicator import ATCommunicator, ATSerialPortError

class TestATCommunicator(unittest.TestCase):
  """
    Test ATCommunicator instance, setters and getters
  """

  def __init__(self, methodName):
    super().__init__(methodName)

  def test_communicator(self):
    #Test setters / getters
    com = ATCommunicator("/dev/ttyS0", 9600)
    self.assertEqual(com.serial_port, "/dev/ttyS0")
    self.assertEqual(com.baud_rate, 9600)
    self.assertEqual(com.default_timeout, 10)
    self.assertEqual(com.line_break, "\r\n")
    com.serial_port = "/dev/ttyfoobar"
    self.assertEqual(com.serial_port, "/dev/ttyfoobar")
    com.baud_rate = 115200
    self.assertEqual(com.baud_rate, 115200)
    com.default_timeout = 15
    self.assertEqual(com.default_timeout, 15)
    com.default_timeout = -5
    self.assertEqual(com.default_timeout, 10)
    com.default_timeout = None
    self.assertEqual(com.default_timeout, 10)
    com.line_break = "\r"
    self.assertEqual(com.line_break, "\r")
    with self.assertRaises(ATSerialPortError):
      com.open()
    com.serial_port = None
    with self.assertRaises(ATSerialPortError):
      com.open()
    with self.assertRaises(ATSerialPortError):
      com.close()
    self.assertFalse(com.is_open())
    with self.assertRaises(ATSerialPortError):
      com.exec("AT")

if __name__ == "__main__":
  unittest.main()
