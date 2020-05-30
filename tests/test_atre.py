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
#Tempfile
from tempfile import NamedTemporaryFile

SCRIPT = "commands_esk.ats"
SCRIPT_RUN = "atre.ats"
SCRIPT_ERR = "errors.ats"
SCRIPT_ATRE_ERR = "atre_error.ats"

response = None
response_ptr = 0

response_assoc = {
    "ATD*99***1#": "CONNECT\r\n",
    "AT+CGDATA=\"PPP\",1": "CONNECT\r\n",
    "AT+CSQ": "32,99\r\n\r\nOK\r\n",
    "AT+CPIN?": "+CPIN: READY\r\n",
    "AT+CGSN": "123456789\r\nOK\r\n",
    "AT+CGDCONT=1,\"IP\",\"apn.foo.bar\"": "OK\r\n",
    "AT": "OK\r\n"
}

def create_virtual_response(command):
    """
    Create a virtual response to return from command

    :param command
    :type command: String
    """
    global response
    global response_ptr
    #Remove newlines from command
    if command.endswith("\r\n"):
        command = command[:-2]
    response_str = response_assoc.get(command)
    response_ptr = 0
    if response_str:
        response = response_str
    else:
        response = "ERROR\r\n"

def in_waiting():
    global response
    global response_ptr
    return response_ptr < len(response)

def read_callback(nbytes):
    global response
    global response_ptr
    ret = response[response_ptr:response_ptr + nbytes]
    response_ptr += nbytes
    return ret

def write_callback(command):
    cmd = command.decode("utf-8")
    create_virtual_response(cmd)

class TestATRE(unittest.TestCase):
    """
      Test ATRuntime Environment commands preparation and evaluation
      NOTE: this tests doesn't test communicator!
    """

    def __init__(self, methodName):
        super().__init__(methodName)
        self.atre = ATRuntimeEnvironment()
        self.script_dir = "%s/scripts/" % dirname(__file__)
        #Verify constructor
        self.assertEqual(self.atre.aof, True)

    def test_session_reset(self):
        # Try to reset session
        cmd = ATCommand("AT", "OK")
        cmds = [cmd]
        self.atre.init_session(cmds)

    def test_set_esks(self):
        # Try to set ESK
        esks = []
        esk = ESK.to_ESKValue(ESK.get_esk_from_string("AOF"), "True")
        self.assertIsNotNone(esk, "Could not parse ESK AOF")
        esks.append((esk, 0))
        self.atre.set_ESKs(esks)
        #Test ESKs
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.AOF, "True")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.BAUDRATE, "9600")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.BREAK, "CRLF")))
        #Use a different ATRE for device
        new_atre = ATRuntimeEnvironment()
        self.assertTrue(new_atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.DEVICE, "/dev/ttyS1")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.DSRDTR, "True")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.EXEC, "echo foo")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.GETENV, "PATH")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.PRINT, "foobar")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.RTSCTS, "True")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.SET, "PIN=1522")))
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.TIMEOUT, "5")))
        tempfile = NamedTemporaryFile()
        self.assertTrue(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.WRITE, "%s HELLO WORLD!" % tempfile.name)))
        #Bad cases
        self.assertFalse(self.atre._ATRuntimeEnvironment__process_ESK(ESK.to_ESKValue(ESK.DEVICE, "/dev/ttyS1")))

    def test_write(self):
        #Test write
        tempfile = NamedTemporaryFile()
        self.assertTrue(self.atre._ATRuntimeEnvironment__write_file(tempfile.name, "HELLO WORLD!"))
        #Try bad write
        self.assertFalse(self.atre._ATRuntimeEnvironment__write_file("/", "HELLO WORLD!"))

    def test_reconfigure_communicator(self):
        self.assertTrue(self.atre._ATRuntimeEnvironment__reconfigure_communicator())

    def test_parse_script(self):
        # Try to parse script
        try:
            self.atre.parse_ATScript("%s%s" % (self.script_dir, SCRIPT))
        except ATScriptNotFound as err:
            raise err
        except ATScriptSyntaxError as err:
            raise err

    def test_configure_communicator(self):
        self.atre.configure_communicator("/dev/ttyS0", 115200, 5, "\r\n", False, False)
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.serial_port, "/dev/ttyS0")
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.baud_rate, 115200)
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.default_timeout, 5)
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.line_break, "\r\n")
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.rtscts, False)
        self.assertEqual(self.atre._ATRuntimeEnvironment__communicator.dsrdtr, False)

    def test_session_key(self):
        # Try to get unexisting key
        with self.assertRaises(KeyError):
            self.atre.get_session_value("foobar")

    def test_run(self):
        self.atre = ATRuntimeEnvironment(True)
        # Configure virtual communicator
        # Parse script
        try:
            self.atre.parse_ATScript("%s%s" % (self.script_dir, SCRIPT_RUN))
        except (ATScriptNotFound, ATScriptSyntaxError) as err:
            self.assertTrue(False, "Could not parse AT script: %s" % err)
        # Assert uninitialized atre
        with self.assertRaises(ATREUninitializedError):
            self.atre.run()
        # Initialize communicator and then run
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r", read_callback, write_callback, in_waiting)
        try:
            self.atre.run()
        except (ATRuntimeError, ATSerialPortError, ATREUninitializedError) as err:
            self.assertTrue(False, "Runtime error: %s" % err)

    def test_exec(self):
        self.atre = ATRuntimeEnvironment(True)
        # Exec single command string
        with self.assertRaises(ATREUninitializedError):
            self.atre.exec("AT;;OK")
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r\n", read_callback, write_callback, in_waiting)
        self.atre.open_serial()
        self.atre.exec("AT;;OK;;100")  # Tests delay too
        # Test bad response
        with self.assertRaises(ATRuntimeError):
            self.atre.exec("AT;;NOK")
        # Test ESK
        self.atre.exec("PRINT Foobar")
        with self.assertRaises(ATRuntimeError):
            self.atre.exec("GETENV aaaaaaaaaaa")
        self.assertIsNone(self.atre.exec(""))
        self.atre.close_serial()

    def test_exec_step(self):
        self.atre = ATRuntimeEnvironment(True)
        # Configure virtual communicator
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r", read_callback, write_callback, in_waiting)
        # Parse script
        try:
            self.atre.parse_ATScript("%s%s" % (self.script_dir, SCRIPT_RUN))
        except (ATScriptNotFound, ATScriptSyntaxError) as err:
            self.assertTrue(False, "Could not parse AT script: %s" % err)
        # Open serial
        self.atre.open_serial()
        res = True
        while res:
            try:
                res = self.atre.exec_next()
            except (ATRuntimeError, ATSerialPortError, ATREUninitializedError) as err:
                self.assertTrue(False, "Runtime error: %s" % err)
        self.atre.close_serial()
        # With errors
        self.atre.init_session([])
        # Parse script
        try:
            self.atre.parse_ATScript(
                "%s%s" % (self.script_dir, SCRIPT_ATRE_ERR))
        except (ATScriptNotFound, ATScriptSyntaxError) as err:
            self.assertTrue(False, "Could not parse AT script: %s" % err)
        # Open serial
        self.atre.open_serial()
        with self.assertRaises(ATRuntimeError):
            self.atre.exec_next()
        self.atre.close_serial()

    def test_fail_parse(self):
        self.atre = ATRuntimeEnvironment(True)
        # Configure virtual communicator
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r", read_callback, write_callback, in_waiting)
        # Parse script
        with self.assertRaises(ATScriptNotFound):
            self.atre.parse_ATScript("/tmp/unexisting_script.ats")
        with self.assertRaises(ATScriptSyntaxError):
            self.atre.parse_ATScript("%s%s" % (self.script_dir, SCRIPT_ERR))

    def test_add_command(self):
        self.atre = ATRuntimeEnvironment(True)
        # Configure virtual communicator
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r", read_callback, write_callback, in_waiting)
        cmd = ATCommand("AT", "OK")
        self.assertTrue(self.atre.add_command(cmd), "ATRE add_command failed")

    def test_serial(self):
        self.atre = ATRuntimeEnvironment(True)
        # Open before init
        with self.assertRaises(ATREUninitializedError):
            self.atre.open_serial()
        # Close before init
        with self.assertRaises(ATREUninitializedError):
            self.atre.close_serial()
        # Configure virtual communicator
        self.atre.configure_virtual_communicator(
            "virtualAdapter", 115200, 10, "\r", read_callback, write_callback, in_waiting)
        self.atre.open_serial()
        self.atre.open_serial()  # Re-open, nothing strange should happen
        self.atre.close_serial()
        self.atre.close_serial()  # Re-close, nothing strange should happen

    def test_exceptions(self):
        # AtSerialPortError
        msg = "Could not open Serial Device"
        exc = ATSerialPortError(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)
        # ATScriptNotFound
        msg = "Could not open file /tmp/foobar.ats"
        exc = ATScriptNotFound(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)
        # ATScriptSyntaxError
        msg = "Error while parsing AT script"
        exc = ATScriptSyntaxError(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)
        # ATREUninitializedError
        msg = "Uninitialized AT Runtime Environment"
        exc = ATREUninitializedError(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)
        # ATRuntimeError
        msg = "Runtime Error"
        exc = ATRuntimeError(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)


if __name__ == "__main__":
    unittest.main()
