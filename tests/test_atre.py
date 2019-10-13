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

from attila.atre import ATRuntimeEnvironment
from attila.atcommand import ATCommand
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError
from attila.esk import ESK, ESKValue

from os.path import dirname

SCRIPT = "commands_esk.ats"

class TestParser(unittest.TestCase):
  """
    Test ATRuntime Environment commands preparation and evaluation
    NOTE: this tests doesn't test communicator!
  """

  def __init__(self, methodName):
    super().__init__(methodName)
    self.atre = ATRuntimeEnvironment()
    self.script_dir = "%s/scripts/" % dirname(__file__)
    
  def test_session_reset(self):
    #Try to reset session
    cmd = ATCommand("AT", "OK")
    cmds = [cmd]
    self.atre.init_session(cmds)
  
  def set_esks(self):
    #Try to set ESK
    esks = []
    esk = ESK.to_ESKValue(ESK.get_esk_from_string("AOF"), "True")
    self.assertIsNotNone(esk, "Could not parse ESK")
    esks.append((esk, 0))
    self.atre.set_ESKs(esks)

  def parse_script(self):
    #Try to parse script
    try:
      self.atre.parse_ATScript("%s%s" % (self.script_dir, SCRIPT))
    except ATScriptNotFound as err:
      raise err
    except ATScriptSyntaxError as err:
      raise err

  def test_session_key(self):
    #Try to get unexisting key
    with self.assertRaises(KeyError):
      self.atre.get_session_value("foobar")

if __name__ == "__main__":
  unittest.main()
