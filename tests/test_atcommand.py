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

from attila.atcommand import ATCommand

class TestATCommands(unittest.TestCase):
  """
    Test ATcommands instance, setters and getters
  """

  def __init__(self, methodName):
    super().__init__(methodName)

  def test_at_commands(self):
    cmd = ATCommand("AT+CSQ", "OK", 5, 1000, ["AT+CSQ=?{dbm},"], None)
    self.assertEqual(cmd.command, "AT+CSQ", "Expected command AT+CSQ, got %s" % cmd.command)
    self.assertEqual(cmd.expected_response, "OK", "Expected response OK, got %s" % cmd.expected_response)
    self.assertEqual(cmd.timeout, 5, "Expected timeout 5, got %d" % cmd.timeout)
    self.assertEqual(cmd.delay, 1000, "Expected delay 1000, got %d" % cmd.delay)
    self.assertEqual(len(cmd.collectables), 1, "Expected collectables length 1, got %d" % len(cmd.collectables))
    self.assertEqual(cmd.collectables[0], "AT+CSQ=?{dbm},", "Expected collectable 'AT+CSQ=?{dbm},', got %s" % cmd.collectables[0])

if __name__ == "__main__":
  unittest.main()
