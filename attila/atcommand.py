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

from .atresponse import ATResponse

class ATCommand(object):
  """
  This class represents an AT command
  """
  
  def __init__(self, cmd, exp_response = None, tout = None, delay = 0, collectables = None, dganger = None):
    """
    Class constructor. Instantiates a new :class:`.ATCommand.` object with the provided parameters.
    
    :param cmd: command to execute
    :param exp_response: expected response from command execution. a literal or a generic response can be provided
    :param tout (optional): command timeout execution in seconds.
    :param delay (optional): delay in milliseconds before command execution
    :param collectables (optional): values to store from response. Follow collectables syntax as specified in ATtila documentation
    :param dganger (optional): doppelganger command associated to this command (command to execute in case of this command fails)
    :type cmd: string
    :type ATResponse: string
    :type exp_respose: string
    :type tout: int
    :type delay: int
    :type collectables: list of string
    :type dganger: ATCommand
    """
    self._command = cmd
    self._expected_response = exp_response
    self._timeout = tout
    self._delay = delay
    self.collectables = collectables
    self.doppel_ganger = dganger
    self._response = None

  @property
  def command(self):
    return self._command

  @command.setter
  def command(self, cmd):
    self._command = cmd

  @property
  def expected_response(self):
    return self._expected_response

  @expected_response.setter
  def expected_response(self, exp_response):
    self._expected_response = exp_response

  @property
  def response(self):
    return self._response

  @response.setter
  def response(self, response):
    if isinstance(response, ATResponse):
      self._response = response
    else:
      self._response = None

  @property
  def timeout(self):
    return self._timeout

  @timeout.setter
  def timeout(self, tout):
    if tout > 1:
      self._timeout = tout
    else:
      self._timeout = 1

  @property
  def delay(self):
    return self._delay

  @delay.setter
  def delay(self, delay):
    if delay > 0:
      self._delay = delay
    else:
      self._delay = 0

  @property
  def collectables(self):
    return self._collectables

  @collectables.setter
  def collectables(self, collectables):
    if type(collectables) == list:
      self._collectables = collectables
    else:
      self._collectables = None

  @property
  def doppel_ganger(self):
    return self._doppel_ganger

  @doppel_ganger.setter
  def doppel_ganger(self, dganger):
    if isinstance(dganger, ATCommand):
      self._doppel_ganger = dganger
    else:
      self._doppel_ganger = None
