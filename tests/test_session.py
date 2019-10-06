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
    self.__test_doppelganger()
    self.__test_collectables()

  def __test_doppelganger(self):
    """
    Test doppelganger feature in ATSession using AT+CPIN
    """
    #First prepare its doppelganger
    cpin_enter_pin = ATCommand("AT+CPIN=${SIM_PIN}", "OK")
    #Let's define an AT Command (AT+CPIN?)
    cpin_command = ATCommand("AT+CPIN?", "READY", 10, 0, None, cpin_enter_pin)
    #Add command to session
    self.session.add_command(cpin_command)
    #Add SIM PIN to session storage
    sim_pin = 7782
    self.session.set_session_value("SIM_PIN", 7782)
    #Verify session storage
    read_pin = self.session.get_session_value("SIM_PIN")
    self.assertEqual(sim_pin, read_pin, "SIM PIN should be %d, but is %d" % (sim_pin, read_pin))
    #Get command
    next_command = self.session.get_next_command()
    #Verify command
    self.assertEqual(next_command.command, "AT+CPIN?", "Next command should be AT+CPIN?, but is %s" % next_command.command)
    #Let's create a fake response
    serial_response = ["CPIN:SIM PIN", "OK"]
    response = self.session.validate_response(serial_response, 100)
    #Last command should have failed (we expected READY)
    self.assertTrue(self.session.last_command_failed)
    print("%s (expected %s) has response: %s" % (next_command.command, next_command.expected_response, response.full_response))
    self.assertEqual(response.full_response, serial_response, "Response associated to command is different from the response got from serial device")
    #Let's get the next command, that should be the doppelganger
    next_command = self.session.get_next_command()
    self.assertEqual(next_command.command, "AT+CPIN=%d" % sim_pin, "The next command should be the doppelganger, but is %s" % next_command.command)
    print("Next command is doppelganger with replaced session value: %s" % next_command.command)
    #Let's invent a response for it, let's say it's OK
    serial_response = ["OK"]
    response = self.session.validate_response(serial_response, 100)
    #Last command should have succeded
    self.assertFalse(self.session.last_command_failed)
    print("%s (expected %s) has response: %s" % (next_command.command, next_command.expected_response, response.response))
    self.assertEqual(response.response, next_command.expected_response, "The response should be OK, but is %s" % response.response)

  def __test_collectables(self):
    """
    Test collectables feature in ATSession using AT+CSQ
    """
    csq_command = ATCommand("AT+CSQ", "OK", 10, 0, ["AT+CSQ=?{rssi},"])
    self.session.add_command(csq_command)
    #Let's get command
    next_command = self.session.get_next_command()
    #Invent a response for it
    serial_response = ["AT+CSQ=31,1", "OK"]
    response = self.session.validate_response(serial_response, 50)
    #Last command should have succeded
    self.assertFalse(self.session.last_command_failed)
    #Verify if collectable has actually been collected
    try:
      rssi = self.session.get_session_value("rssi")
      self.assertEqual(rssi, "31", "rssi should be 31, but is %s" % rssi)
    except KeyError as err:
      raise err

if __name__ == "__main__":
  unittest.main()

