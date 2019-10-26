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

from attila.virtual.exceptions import VirtualSerialException

class VirtualSerial(object):
  def __init__(self, serial_port, baudrate, timeout = 0, read_callback = None, write_callback = None, in_waiting_callback = None):
    """
    Class constructor. Instantiates a new :class:`.virtual.VirtualSerial` object with the provided parameters.

    :param serial_port: serial port to use in order to communicate with the RF module
    :param baud_rate: baud rate to set
    :param timeout (optional): the default timeout for command response read in seconds; it will be used if a timeout is not provided when executing a command
    :param read_callback (optional): Specify a read function to call to read using the virtual communicator
    :param write_callback (optional): Specifiy a write funtion to call to write using the virtual communicator
    :type serial_port: string
    :type baud_rate: int
    :type timeout: int > 0
    :type read_callback: function which returns string and takes nbytes as argument, if nbytes is -1 returns all lines, if 0 returns line
    :type write_callback: function which takes string and raises VirtualSerialException
    """
    self.serial_port = serial_port
    self.baudrate = baudrate
    self.timeout = timeout
    self.__writeCB = write_callback
    self.__readCB = read_callback
    self.__in_waiting_callback = in_waiting_callback

  @property
  def serial_port(self):
    return self._serial_port

  @serial_port.setter
  def serial_port(self, serial_port):
    self._serial_port = serial_port

  @property
  def baudrate(self):
    return self._baudrate

  @baudrate.setter
  def baudrate(self, baud_rate):
    self._baudrate = baud_rate

  @property
  def timeout(self):
    return self._timeout

  @timeout.setter
  def timeout(self, timeout):
    if timeout:
      if timeout > 0:
        self._timeout = timeout
      else:
        self._timeout = 10
    else:
      self._timeout = 10

  @property
  def in_waiting(self):
    if self.__in_waiting_callback:
      return self.__in_waiting_callback()
    else:
      return False

  def open(self):
    """
    Open virtual serial
    """
    if not self.serial_port or not self.baudrate:
      raise VirtualSerialException("Could not open %s" % self.serial_port)
    return True

  def close(self):
    """
    Open virtual serial
    """
    if not self.serial_port or not self.baudrate:
      raise VirtualSerialException("Could not close %s" % self.serial_port)
    return True

  def write(self, data):
    """
    Virtual write function

    :param data
    :type data bytes
    :returns True
    """
    #Prepare virtual response
    if self.__writeCB:
      self.__writeCB(data)
    return True

  def read(self, nbytes = 1):
    """
    Read a virtual byte

    :param nbytes
    :type nbytes: int
    :returns bytes
    """
    if self.__readCB:
      response = self.__readCB(nbytes)
      return response.encode("utf-8")

  def read_lines(self):
    """
    Read lines

    :returns array of bytes
    """
    response = []
    str_tokens = self.__readCB(-1).splitlines()
    for token in str_tokens:
      response.append(token.encode("utf-8"))
    return response

  def read_line(self):
    """
    Read line

    :returns bytes
    """
    return self.__readCB(0).encode("utf-8")

  def reset_input_buffer(self):
    """
    Reset Input buffer
    Virtually, reset response and pointer
    """
    pass
