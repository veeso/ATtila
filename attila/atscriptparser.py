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

from .exceptions import ATScriptNotFound, ATScriptSyntaxError
from .atcommand import ATCommand
from .esk import ESK, ESKValue

class ATScriptParser(object):
  """
  This class represents an AT script parser, which is the component which purpose is to parse an ATScript.
  """

  def parse(self, script):
    """
    Parse an ATScript

    :param script: lines of at script
    :type script: String
    :returns Tuple of array of ATCommand and array of tuple of (ESKValue, execution index)
    :raises ATScriptSyntaxError
    """
    result = ([], [])
    commands = result[0]
    esks = result[1]
    execution_index = 0
    line_no = 0
    #Split script into rows
    for row in script.splitlines():
      #Increment line number
      line_no += 1
      if not row: #Empty row
        continue
      if row.startswith("#"): #Is comment
        continue
      eks, error = self.__parse_esk(row)
      if eks:
        esks.append((eks, execution_index))
      elif error: #If error is set, it means line is EKS, but has invalid syntax
        raise ATScriptSyntaxError("Syntax error at line %d: %s (%s)" % (line_no, error, row))
      else: #Otherwise, if both are None, it is a command
        #Try as ommand
        command, error = self.__parse_command(row)
        if command:
          commands.append(command)
          #Increment execution_index
          execution_index += 1
        elif error:
          raise ATScriptSyntaxError("Syntax error at line %d: %s (%s)" % (line_no, error, row))
        else:
          raise ATScriptSyntaxError("Syntax error at line %d: %s -- Don't know how to interpret this line, sorry..." % (line_no, row))
    return result

  def parse_file(self, file_path):
    """
    Parse an ATScript file

    :param file_path: path of the ATScript file
    :type file_path: String
    :returns Tuple of array of ATCommand and array of tuple of (ESKValue, execution index)
    :raises ATScriptNotFound, ATScriptSyntaxError
    """
    try:
      hnd = open(file_path)
      script = hnd.read()
      hnd.close()
      return self.parse(script)
    except IOError as err:
      raise ATScriptNotFound(err)
    except ATScriptSyntaxError as err:
      raise err

  def __parse_esk(self, row):
    """
    Parse a row, which is possibly an ESK

    :param row: ESK row
    :type row: String
    :returns (ESKValue, String): A tuple of ESKValue and an error string. Error is different from None only if ESK is valid. Both are None if it's not an ESK.
    """
    esk_value = None
    error = None
    line_tokens = row.split()
    if len(line_tokens) == 0:
      error = "Empty row"
      return (esk_value, error)
    esk_str = line_tokens[0]
    if len(line_tokens) > 1:
      esk_attr = " ".join(line_tokens[1:])
    else:
      esk_attr = None
    esk = ESK.get_esk_from_string(esk_str)
    if not esk:
      #Not an ESK
      return (esk_value, error) #None, None
    #Eval attributes
    esk_value = ESK.to_ESKValue(esk, esk_attr)
    if not esk_value:
      error = "Invalid attributes"
    return (esk_value, error)

  def __parse_command(self, row):
    """
    Parse a row, which is possibly an AT command

    :param row: command row
    :type row: String
    :returns (ATCommand, String): A tuple of ATCommand and an error string. Error is different from None only if command syntax is wrong. Both are None if it's not an AT command.
    """
    command = None
    error = None
    command_tokens = row.split(";;")
    if len(command_tokens) == 0:
      error = "Empty row"
      return (command, error)
    atcommand = command_tokens[0]
    expected_response = None
    delay = 0
    timeout = None
    collectables = None
    doppelganger = None
    doppelganger_response = None
    has_doppelganger = False
    if len(command_tokens) > 1: #Expected response
      if command_tokens[1]:
        expected_response = command_tokens[1]
    if len(command_tokens) > 2: #Delay
      if command_tokens[2]:
        try:
          delay = int(command_tokens[2])
        except ValueError:
          error = "Delay is not a number"
          return (command, error)
    if len(command_tokens) > 3: #Timeout
      if command_tokens[3]:
        try:
          timeout = int(command_tokens[3])
        except ValueError:
          error = "Timeout is not a number"
          return (command, error)
    if len(command_tokens) > 4: #Collectables
      if command_tokens[4]:
        try:
          collectables = eval(command_tokens[4])
        except NameError as err:
          error = "Collectables has invalid syntax (%s)" % err
          return (command, error)
        except SyntaxError as err:
          error = "Collectables has invalid syntax (%s)" % err
          return (command, error)
    if len(command_tokens) > 5: #Doppelganger
      if command_tokens[5]:
        has_doppelganger = True
    if len(command_tokens) > 6: #Doppelganger response
      if command_tokens[6]:
        doppelganger_response = command_tokens[6]
    if has_doppelganger:
      #Instance doppelganger
      doppelganger = ATCommand(command_tokens[5], doppelganger_response, timeout, delay, collectables, None)
    #Instance new AT command
    command = ATCommand(atcommand, expected_response, timeout, delay, collectables, doppelganger)
    return (command, error)
