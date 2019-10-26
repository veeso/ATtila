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

from attila.atscriptparser import ATScriptParser
from attila.exceptions import ATScriptNotFound, ATScriptSyntaxError
from attila.esk import ESK

SCRIPT_1 = "basic_command.ats"
SCRIPT_2 = "commands_response.ats"
SCRIPT_3 = "command_complex.ats"
SCRIPT_4 = "commands_esk.ats"
SCRIPT_ERR = "errors.ats"

class TestParser(unittest.TestCase):

  def __init__(self, methodName):
    super().__init__(methodName)
    self.script_dir = "%s/scripts/" % dirname(__file__)

  def test_file_parser(self):
    """
    Test File parser; files used for tests can be found in scripts/
    """
    print("Test: test_file_parser")
    #Instance new Script parser
    script_parser = ATScriptParser()
    #Let's check if a file not found raises an exceptionù
    with self.assertRaises(ATScriptNotFound):
      script_parser.parse_file("%s%s" % (self.script_dir, "null"))
    self.__test_parse_script1(script_parser)
    self.__test_parse_script2(script_parser)
    self.__test_parse_script3(script_parser)
    self.__test_parse_script4(script_parser)

  def __test_parse_script1(self, script_parser):
    """
    Test script 1 (basic commands)

    :param script_parser
    :type script_parser: ATScriptParser
    """
    #Start with basic commands
    print("Testing parse_file: %s" % SCRIPT_1)
    try:
      script = script_parser.parse_file("%s%s" % (self.script_dir, SCRIPT_1))
    except ATScriptNotFound as err:
      raise err
    except ATScriptSyntaxError as err:
      raise err
    #Let's check if returned script is correct
    commands = script[0]
    esks = script[1]
    #There mustn't be any ESK in response
    self.assertEqual(len(esks), 0, "There shouldn't be any esks in script %s" % SCRIPT_1)
    #We expect 3 commands
    self.assertEqual(len(commands), 3, "There should be only 3 commands; found %d in script %s" % (len(commands), SCRIPT_1))
    self.assertEqual(commands[0].command, "AT", "The first command should be AT but is %s" % commands[0].command)
    #Iterate over commands
    for command in commands:
      print("Command: %s" % command.command)
      self.assertIsNone(command.expected_response, "expected response should be None, found %s" % str(command.expected_response))

  def __test_parse_script2(self, script_parser):
    """
    Test script 2 (commands_response)

    :param script_parser
    :type script_parser: ATScriptParser
    """
    #Start with basic commands
    print("Testing parse_file: %s" % SCRIPT_2)
    try:
      script = script_parser.parse_file("%s%s" % (self.script_dir, SCRIPT_2))
    except ATScriptNotFound as err:
      raise err
    except ATScriptSyntaxError as err:
      raise err
    #Let's check if returned script is correct
    commands = script[0]
    esks = script[1]
    #There mustn't be any ESK in response
    self.assertEqual(len(esks), 0, "There shouldn't be any esks in script %s" % SCRIPT_2)
    #We expect 3 commands
    self.assertEqual(len(commands), 3, "There should be only 3 commands; found %d in script %s" % (len(commands), SCRIPT_2))
    self.assertEqual(commands[0].command, "AT", "The first command should be AT but is %s" % commands[0].command)
    self.assertEqual(commands[0].expected_response, "OK", "The first command should have OK as response, got %s" % commands[0].expected_response)
    self.assertEqual(commands[2].command, "AT+CREG?", "The third command should be AT+CREG? but is %s" % commands[2].command)
    self.assertEqual(commands[2].expected_response, "OK", "The third command should have OK as response, got %s" % commands[2].expected_response)
    #Iterate over commands
    for command in commands:
      print("Command: %s; Response: %s" % (command.command, command.expected_response))
      self.assertIsNotNone(command.expected_response, "expected response should be something, found None")

  def __test_parse_script3(self, script_parser):
    """
    Test script 3 (command complex)

    :param script_parser
    :type script_parser: ATScriptParser
    """
    #Start with basic commands
    print("Testing parse_file: %s" % SCRIPT_3)
    try:
      script = script_parser.parse_file("%s%s" % (self.script_dir, SCRIPT_3))
    except ATScriptNotFound as err:
      raise err
    except ATScriptSyntaxError as err:
      raise err
    #Let's check if returned script is correct
    commands = script[0]
    esks = script[1]
    #There mustn't be any ESK in response
    self.assertEqual(len(esks), 0, "There shouldn't be any esks in script %s" % SCRIPT_3)
    #We expect 4 commands
    self.assertEqual(len(commands), 4, "There should be only 4 commands; found %d in script %s" % (len(commands), SCRIPT_3))
    #Verify command 0
    self.assertEqual(commands[0].command, "ATH0", "The first command should be ATH0 but is %s" % commands[0].command)
    self.assertEqual(commands[0].delay, 5000, "The first command should have 5000 ms of delay but has %d" % commands[0].delay)
    #Verify command 1
    self.assertEqual(commands[1].command, "AT+CPIN?", "The second command should be AT+CPIN? but is %s" % commands[1].command)
    self.assertEqual(commands[1].expected_response, "READY", "The second command should have as response READY but has %s" % commands[1].expected_response)
    self.assertEqual(commands[1].delay, 0, "The second command should have 0 ms of delay but has %d" % commands[1].delay)
    self.assertEqual(commands[1].timeout, 5, "The second command should have 5 s of timeout but has %d" % commands[1].timeout)
    self.assertEqual(commands[1].doppel_ganger.command, "AT+CPIN=7782", "The second command should have AT+CPIN=7782 as doppel_ganger, but has %s" % commands[1].doppel_ganger.command)
    self.assertEqual(commands[1].doppel_ganger.expected_response, "OK", "The second command should have OK as doppel ganger response, but has %s" % commands[1].doppel_ganger.expected_response)
    print("%s => %s; if fails: %s => %s" % (commands[1].command, commands[1].expected_response, commands[1].doppel_ganger.command, commands[1].doppel_ganger.expected_response))
    #Veridy command 3
    self.assertEqual(len(commands[2].collectables), 1, "The third command should have 1 collectables, but has %d" % len(commands[2].collectables))
    self.assertEqual(commands[2].collectables[0], "AT+CSQ=?{dbm},", "The third command should have as collectable 'AT+CSQ=?{dbm},', but has %s" % commands[2].collectables[0])
    #Verify collectable for command 4
    self.assertEqual(len(commands[3].collectables), 1, "The third command should have 1 collectables, but has %d" % len(commands[3].collectables))
    self.assertEqual(commands[3].collectables[0], "?{IMEI::^[0-9]{15}$}", "The forth command should have as collectable '?{IMEI::^[0-9]{15}$}', but has %s" % commands[3].collectables[0])
    #Iterate over commands
    for command in commands:
      print("Command: %s; Response: %s; Delay %s; Timeout: %s; doppel_ganger %s; Collectables %s" % (command.command, command.expected_response, command.delay, command.timeout, command.doppel_ganger, command.collectables))

  def __test_parse_script4(self, script_parser):
    """
    Test script 1 (commands and ESKs)

    :param script_parser
    :type script_parser: ATScriptParser
    """
    #Start with basic commands
    print("Testing parse_file: %s" % SCRIPT_4)
    try:
      script = script_parser.parse_file("%s%s" % (self.script_dir, SCRIPT_4))
    except ATScriptNotFound as err:
      raise err
    except ATScriptSyntaxError as err:
      raise err
    #Let's check if returned script is correct
    commands = script[0]
    esks = script[1]
    #There mustn't be any ESK in response
    self.assertEqual(len(esks), 12, "There should be 12 ESKs in script %s, found %d" % (SCRIPT_4, len(esks)))
    #We expect 6 commands
    self.assertEqual(len(commands), 6, "There should be 6 commands; found %d in script %s" % (len(commands), SCRIPT_4))
    #Verify commands
    #Command 0
    self.assertEqual(commands[0].command, "+++", "The first command should be '+++' but is %s" % commands[0].command)
    #Command 3
    self.assertEqual(commands[3].command, "AT+CPIN?", "The fourth command should be AT+CPIN? but is %s" % commands[3].command)
    self.assertEqual(commands[3].delay, 0, "The fourth command should have 0 ms of delay but has %d" % commands[3].delay)
    self.assertEqual(commands[3].timeout, 5, "The fourth command should have 5 s of timeout but has %d" % commands[3].timeout)
    self.assertEqual(commands[3].doppel_ganger.command, "AT+CPIN=${SIM_PIN}", "The fourth command should have AT+CPIN=${SIM} as doppel_ganger, but has %s" % commands[3].doppel_ganger)
    #Command 4
    self.assertEqual(commands[4].command, "AT+CGDCONT=1,\"IP\",\"${APN}\"", "The fifth command should be AT+CPIN? but is %s" % commands[4].command)
    self.assertEqual(commands[4].expected_response, "OK", "The fifth command should have as response OK but has %s" % commands[4].expected_response)
    self.assertEqual(commands[4].delay, 1000, "The fifth command should have 1000 ms of delay but has %d" % commands[4].delay)
    #Iterate over commands
    for command in commands:
      print("Command: %s " % command.command)
    #Verify ESKs
    #device
    self.assertEqual(esks[0][0].keyword, ESK.DEVICE, "The first ESK should be DEVICE, but is %s" % esks[0][0].keyword)
    self.assertEqual(esks[0][0].value, "/dev/ttyUSB0", "The first ESK should have as value /dev/ttyUSB0, but has %s" % esks[0][0].value)
    self.assertEqual(esks[0][1], 0, "ESK 0 has wrong command index %d" % esks[0][1])
    #baud rate
    self.assertEqual(esks[1][0].keyword, ESK.BAUDRATE, "The first ESK should be BAUDRATE, but is %s" % esks[1][0].keyword)
    self.assertEqual(esks[1][0].value, 115200, "The first ESK should have as value 115200, but has %d" % esks[1][0].value)
    self.assertEqual(esks[1][1], 0, "ESK 1 has wrong command index %d" % esks[1][1])
    #Timeout
    self.assertEqual(esks[2][0].keyword, ESK.TIMEOUT, "The first ESK should be TIMEOUT, but is %s" % esks[2][0].keyword)
    self.assertEqual(esks[2][0].value, 10, "The first ESK should have as value 10, but has %d" % esks[2][0].value)
    self.assertEqual(esks[2][1], 0, "ESK 2 has wrong command index %d" % esks[2][1])
    #Break
    self.assertEqual(esks[3][0].keyword, ESK.BREAK, "The first ESK should be BREAK, but is %s" % esks[3][0].keyword)
    self.assertEqual(esks[3][0].value, "\r\n", "The first ESK should have as value CRLF, but has %s" % esks[3][0].value)
    self.assertEqual(esks[3][1], 0, "ESK 3 has wrong command index %d" % esks[3][1])
    #AOF
    self.assertEqual(esks[4][0].keyword, ESK.AOF, "The first ESK should be AOF, but is %s" % esks[4][0].keyword)
    self.assertEqual(esks[4][0].value, True, "The first ESK should have as value True, but has %s" % esks[4][0].value)
    self.assertEqual(esks[4][1], 0, "ESK 4 has wrong command index %d" % esks[4][1])
    #GETENV
    self.assertEqual(esks[5][0].keyword, ESK.GETENV, "The first ESK should be GETENV, but is %s" % esks[5][0].keyword)
    self.assertEqual(esks[5][0].value, "SIM_PIN", "The first ESK should have as value SIM_PIN, but has %s" % esks[5][0].value)
    self.assertEqual(esks[5][1], 0, "ESK 5 has wrong command index %d" % esks[5][1])
    #EXEC
    self.assertEqual(esks[6][0].keyword, ESK.EXEC, "The first ESK should be EXEC, but is %s" % esks[6][0].keyword)
    self.assertEqual(esks[6][0].value, "echo 0", "The first ESK should have as value echo 0, but has %s" % esks[6][0].value)
    self.assertEqual(esks[6][1], 0, "ESK 6 has wrong command index %d" % esks[6][1])
    #SET
    self.assertEqual(esks[7][0].keyword, ESK.SET, "The first ESK should be SET, but is %s" % esks[7][0].keyword)
    self.assertEqual(esks[7][0].value, ("APN", "apn.foo.bar"), "The first ESK should have as value (APN, apn.foo.bar)")
    self.assertEqual(esks[7][1], 0, "ESK 7 has wrong command index %d" % esks[7][1])
    #PRINT
    self.assertEqual(esks[8][0].keyword, ESK.PRINT, "The first ESK should be PRINT, but is %s" % esks[8][0].keyword)
    self.assertEqual(esks[8][0].value, "Dialing your ISP", "The first ESK should have as value 'Dialing your ISP', but has %s" % esks[8][0].value)
    self.assertEqual(esks[8][1], 0, "ESK 8 has wrong command index %d" % esks[8][1])
    #Last PRINT
    self.assertEqual(esks[11][1], 6, "ESK 11 has wrong command index %d" % esks[9][1])
    #Iterate over commands
    for esk in esks:
      eskpair = esk[0]
      cmd_index = esk[1]
      print("execution index: %d; Esk %s => %s" % (cmd_index, eskpair.keyword, eskpair.value))

  def test_syntax_errors(self):
    parser = ATScriptParser()
    with self.assertRaises(ATScriptSyntaxError): 
      parser.parse("BAUDRATE foobar") #Invalid ESK
    with self.assertRaises(ATScriptSyntaxError):
      parser.parse_file("%s/%s" % (self.script_dir, SCRIPT_ERR))
    with self.assertRaises(ATScriptSyntaxError): #Invalid delay
      parser.parse("AT;;OK;;foobar")
    with self.assertRaises(ATScriptSyntaxError): #Invalid timeout
      parser.parse("AT;;OK;;5000;;foobar")
    with self.assertRaises(ATScriptSyntaxError): #Invalid collectable syntax
      parser.parse("AT+CGSN;;OK;;5000;;5;;[\"?{IMEI::^[0-9]{15}$}\"")
    with self.assertRaises(ATScriptSyntaxError): #Invalid collectable syntax
      parser.parse("AT+CGSN;;OK;;5000;;5;;foobar")

if __name__ == "__main__":
  unittest.main()
