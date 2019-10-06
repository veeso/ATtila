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

from attila.atsession import ATSession
from attila.atcommand import ATCommand

class TestParser(unittest.TestCase):

  def __init__(self, methodName):
    super().__init__(methodName)
    self.session = ATSession()
    
  def test_commands(self):
    """
    Test ATSession commands preparation and evaluation
    """
    #Let's define an AT Command (AT+CPIN?)
    #First prepare its doppelganger
    cpin_enter_pin = ATCommand("AT+CPIN=${SIM_PIN}", "OK")
    cpin_command = ATCommand("AT+CPIN?", "READY", 10, 0, None, cpin_enter_pin)

if __name__ == "__main__":
  unittest.main()

