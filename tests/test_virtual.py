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
from attila.virtual.atvirtualcommunicator import (
    ATVirtualCommunicator,
    ATSerialPortError,
)
from attila.virtual.virtualserial import VirtualSerial, VirtualSerialException

response = None
response_ptr = 0


def create_virtual_response(command):
    """
    Create a virtual response to return from command

    :param command
    :type command: String
    """
    global response
    global response_ptr
    response_assoc = {
        "ATD*99***1#": "CONNECT\r\n",
        'AT+CGDATA="PPP",1': "CONNECT\r\n",
        "AT+CSQ": "+CSQ: 32,99\r\n\r\nOK\r\n",
        "AT+CPIN?": "+CPIN: READY\r\n",
        "AT+CGSN": "123456789\r\nOK\r\n",
    }
    response_str = response_assoc.get(command)
    response_ptr = 0
    if response_str:
        response = response_str
    else:
        response = "OK\r\n"


def in_waiting():
    global response
    global response_ptr
    return response_ptr < len(response)


def read_callback(nbytes):
    global response
    global response_ptr
    if nbytes > 0:
        ret = response[response_ptr : response_ptr + nbytes]
        response_ptr += nbytes
    elif nbytes == 0:
        lines = response.splitlines()
        if len(lines) > response_ptr:
            ret = lines[response_ptr]
            response_ptr += 1
            return ret
        else:
            return None
    elif nbytes == -1:
        return response
    return ret


def write_callback(command):
    cmd = command.decode("utf-8")
    create_virtual_response(cmd)


class TestATCommunicator(unittest.TestCase):
    """
    Test ATCommunicator instance, setters and getters
    """

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_communicator(self):
        # Test setters / getters
        com = ATVirtualCommunicator(
            "/dev/ttyS0", 9600, 10, "\r\n", read_callback, write_callback, in_waiting
        )
        self.assertEqual(com.serial_port, "/dev/ttyS0")
        self.assertEqual(com.baud_rate, 9600)
        self.assertEqual(com.default_timeout, 10)
        self.assertEqual(com.line_break, "\r\n")
        com.serial_port = "/dev/ttyV0"
        self.assertEqual(com.serial_port, "/dev/ttyV0")
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
        # Open port
        com.open()
        self.assertTrue(com.is_open())
        # Execute
        resp = com.exec("AT")
        print("AT Response: %s" % resp[0])
        self.assertNotEqual(len(resp), 0, "Response should not have 0 as length")
        com.close()
        # Bad cases
        com.serial_port = None
        with self.assertRaises(ATSerialPortError):
            com.open()
        with self.assertRaises(ATSerialPortError):
            com.close()
        self.assertFalse(com.is_open())

    def test_virtual_serial(self):
        device = VirtualSerial(
            "/dev/virtual", 115200, 1, read_callback, write_callback, in_waiting
        )
        self.assertEqual(device.serial_port, "/dev/virtual")
        self.assertEqual(device.baudrate, 115200)
        self.assertEqual(device.timeout, 1)
        # Test open
        device.open()
        # Test write
        device.write(b"AT")
        # Test read
        self.assertEqual(device.read(4).decode("utf-8"), "OK\r\n")
        device.reset_input_buffer()
        # Test read line
        device.write(b"AT+CSQ")
        self.assertEqual(device.read_line().decode("utf-8"), "+CSQ: 32,99")
        self.assertEqual(device.read_line().decode("utf-8"), "")
        self.assertEqual(device.read_line().decode("utf-8"), "OK")
        # Test read lines
        device.write(b"AT+CSQ")
        self.assertEqual(len(device.read_lines()), 3)

    def test_exceptions(self):
        msg = "Virtual Serial error"
        exc = VirtualSerialException(msg)
        self.assertIsNotNone(str(exc))
        self.assertEqual(repr(exc), msg)
        # Open / Close exceptions
        com = ATVirtualCommunicator(
            "/dev/virtual", None, 1, read_callback, write_callback, in_waiting
        )
        com.open()
        with self.assertRaises(ATSerialPortError):
            com.close()


if __name__ == "__main__":
    unittest.main()
