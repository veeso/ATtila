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

class ATResponse(object):
  """
  This class represents an AT command response and provide access to the expected
  response format, the entire response and the command execution time (milliseconds)
  """

  def __init__(self, resp, fullresponse, command, executiontime = 0):
    """
    Class constructor. Instantiates a new :class:`.ATResponse.` object with the provided parameters.

    :param resp: main response from command (format/content as expected by the user)
    :param fullresponse: entire response received from command execution
    :param command: command associated to response
    :param executiontime: execution time of the command in milliseconds
    :type resp: string
    :type fullresponse: list of string
    :type command: ATCommand
    :type executiontime: int
    """
    self._response = resp
    self._full_response = fullresponse
    self._execution_time = executiontime
    self._command = command
    self._collectables = {}

  @property
  def response(self):
    return self._response

  @response.setter
  def response(self, response):
    self._response = response

  @property
  def full_response(self):
    return self._full_response

  @full_response.setter
  def full_response(self, full_response):
    self._full_response = full_response

  @property
  def command(self):
    return self._command

  @property
  def execution_time(self):
    return self._execution_time

  @execution_time.setter
  def execution_time(self, executiontime):
    if executiontime > 0:
      self._execution_time = executiontime
    else:
      self._execution_time = 0

  def add_collectable(self, key, value):
    """
    Add a collectable to the response collectables

    :param key: key of the collectable
    :param value: value of the collectable
    :type key: string
    :type value: any
    :returns void
    """

    self._collectables[key] = value
    return

  def get_collectable(self, key):
    """
    Returns the value associated to the collectable
    
    :param key: key of the collectable
    :type key: string
    :returns any
    """
    return self._collectables.get(key)
