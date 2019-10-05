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

from .exceptions import ATSerialPortError

from serial import Serial, SerialException
import re

class ATCommunicator(object):
  """
  ATCommunicator class provides an interface to communicate with an 
  RF module using AT commands through a serial port
  """

  def __init__(self, serial_port, baud_rate, default_timeout = 10, line_break = "\r\n"):
    """
    Class constructor. Instantiates a new :class:`.ATCommunicator.` object with the provided parameters.

    :param serial_port: serial port to use in order to communicate with the RF module
    :param baud_rate: baud rate to set
    :param default_timeout (optional): the default timeout for command response read in seconds; it will be used if a timeout is not provided when executing a command
    :param line_break (optional): specify line break to use when sending command; most of RF modules use CRLF
    :type serial_port: string
    :type baud_rate: int
    :type default_timeout: int > 0
    :type line_break: string
    """
    self._device = None
    self._serial_port = serial_port
    self._baud_rate = baud_rate
    if default_timeout > 0:
      self._default_timeout = default_timeout
    else:
      self._default_timeout = 10
    self._line_break = line_break

  @property
  def serial_port(self):
    return self._serial_port

  @serial_port.setter
  def serial_port(self, serial_port):
    self._serial_port = serial_port

  @property
  def baud_rate(self):
    return self._baud_rate

  @baud_rate.setter
  def baud_rate(self, baud_rate):
    self._baud_rate = baud_rate

  def open(self):
    """
    Open serial port

    :raises ATSerialPortError
    """
    if not self._serial_port:
      raise ATSerialPortError("Serial port is not set")
    try:
      self._device = Serial(self._serial_port, self._baud_rate, timeout = self._default_timeout)
    except (OSError, SerialException) as error:
      raise ATSerialPortError(error)
    return

  def close(self):
    """
    Close serial port

    :raises ATSerialPortError
    """
    if not self._device:
      raise ATSerialPortError("Serial port device is closed")
    try:
      self._device.close()
    except (OSError, SerialException) as error:
      raise ATSerialPortError(error)
    return

  def is_open(self):
    """
    Returns whether the serial port is open

    :returns bool
    """
    return self._device != None

  def exec(self, command, timeout = None):
    """
    Execute AT command
    
    :param command: command to execute
    :param timeout: timeout for command, if not set default will be used
    :type command: str
    :type timeout: int
    :returns list of string: command response without line break; empty lines are ignored
    :raises ATSerialPortError
    """
    if not self._device:
      raise ATSerialPortError("Serial port device is closed")
    self._device.timeout = timeout
    self._device.write(b"%s%s" % (command, self._line_break))
    lines = self._device.readlines()
    for line in lines:
      line = line.decode('utf-8')
      #Remove newline
      if re.search("(\\r|)\\n$", line):
        line = re.sub("(\\r|)\\n$", "", line)
    return lines
