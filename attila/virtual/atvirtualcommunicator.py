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

from attila.exceptions import ATSerialPortError
from attila.virtual.virtualserial import VirtualSerial, VirtualSerialException
from attila.atcommunicator import ATCommunicator
import re
from time import time
from time import sleep

class ATVirtualCommunicator(ATCommunicator):
  """
  ATVirtualCommunicator class provides a virtual interface to communicate with an 
  RF module using AT commands through a serial port 
  This module should be used in test environment only
  """

  def __init__(self, serial_port, baud_rate, default_timeout = 10, line_break = "\r\n", read_callback = None, write_callback = None, in_waiting_callback = None):
    """
    Class constructor. Instantiates a new :class:`.ATCommunicator.` object with the provided parameters.

    :param serial_port: serial port to use in order to communicate with the RF module
    :param baud_rate: baud rate to set
    :param default_timeout (optional): the default timeout for command response read in seconds; it will be used if a timeout is not provided when executing a command
    :param line_break (optional): specify line break to use when sending command; most of RF modules use CRLF
    :param read_callback (optional): Specify a read function to call to read using the virtual communicator
    :param write_callback (optional): Specifiy a write funtion to call to write using the virtual communicator
    :param in_waiting_callback (optional): Specify a in waiting function to call
    :type serial_port: string
    :type baud_rate: int
    :type default_timeout: int > 0
    :type line_break: string
    :type read_callback: function which returns string and takes nbytes as argument, if nbytes is -1 returns all lines
    :type write_callback: function which takes string and raises VirtualSerialException
    :type in_waiting_callback: function which returns True if there are data available to read
    """
    self._device = None
    self._serial_port = serial_port
    self._baud_rate = baud_rate
    self.default_timeout = default_timeout
    self._line_break = line_break
    self.__writeCB = write_callback
    self.__readCB = read_callback
    self.__inwaitingCB = in_waiting_callback

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

  @property
  def default_timeout(self):
    return self._default_timeout

  @default_timeout.setter
  def default_timeout(self, timeout):
    if timeout:
      if timeout > 0:
        self._default_timeout = timeout
      else:
        self._default_timeout = 10
    else:
      self._default_timeout = 10

  @property
  def line_break(self):
    return self._line_break

  @line_break.setter
  def line_break(self, brk):
    self._line_break = brk

  def open(self):
    """
    Open serial port

    :raises ATSerialPortError
    """
    if not self._serial_port:
      raise ATSerialPortError("Serial port is not set")
    try:
      self._device = VirtualSerial(self._serial_port, self._baud_rate, timeout = 0.5, read_callback = self.__readCB, write_callback = self.__writeCB, in_waiting_callback = self.__inwaitingCB)
    except (OSError, VirtualSerialException) as error:
      raise ATSerialPortError(error)

  def close(self):
    """
    Close serial port

    :raises ATSerialPortError
    """
    if not self._device:
      raise ATSerialPortError("Serial port device is closed")
    try:
      self._device.close()
    except (OSError, VirtualSerialException) as error:
      raise ATSerialPortError(error)
    self._device = None

  def is_open(self):
    """
    Returns whether the serial port is open

    :returns bool
    """
    return super().is_open()

  def exec(self, command, timeout = None):
    """
    Execute AT command
    
    :param command: command to execute
    :param timeout: timeout for command, if not set default will be used
    :type command: str
    :type timeout: int
    :returns tuple of (list of string, execution time ms); list: command response without line break; empty lines are ignored
    :raises ATSerialPortError
    """
    try:
      return super().exec(command, timeout)
    except ATSerialPortError as err:
      raise err
