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

PROGRAM_NAME = "attila"

#Import ATtila
from attila.atre import ATRuntimeEnvironment
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError
#System imports
from sys import argv, exit, stdout
#Logging
import logging
#Getopt
from getopt import getopt, GetoptError
#Signals
from signal import signal, SIGTERM, SIGINT

USAGE = "Usage: %s [OPTION]... [FILE]\n\
  \n\
  With no FILE, run in interactive mode\n\
  \n\
  \t-p <device path>\tUse this device to communicate\n\
  \t-b <baud rate>\t\tUse the specified baudrate to communicate\n\
  \t-T <default timeout>\tUse the specified timeout as default to communicate\n\
  \t-B <break>\t\tUse the specified line break [CRLF, LF, CR, NONE] (Default: CRLF)\n\
  \t-A <True/False>\t\tAbort on failure (Default: True)\n\
  \t-L <logfile>\t\tEnable log and log to the specified log file (stdout is supported)\n\
  \t-l <loglevel>\t\tSpecify the log level (0: CRITICAL, 1: ERROR, 2: WARN, 3: INFO, 4: DEBUG) (Default: INFO\n\
  \t-v\t\t\tBe more verbose\n\
  \t-q\t\t\tBe quiet (print only PRINT ESKs and ERRORS)\n\
  \t-h\t\t\tShow this page\n\
  " % PROGRAM_NAME

LOG_LEVEL_DEBUG = 4
LOG_LEVEL_INFO = 3
LOG_LEVEL_WARN = 2
LOG_LEVEL_ERROR = 1
LOG_LEVEL_CRITICAL = 0

#Globals
sigterm_called = False
interactive_mode = True

def sigterm_handler(_signo, _stack_frame):
  """
  Handle sigterm (or sigint) setting sigterm_called to True
  """
  global interactive_mode
  global sigterm_called
  logging.warn("SIGTERM called")
  sigterm_called = True
  if interactive_mode:
    print("Press ENTER to QUIT")

def opt_error(message):
  """
  Function to call in case of an error while parsing options and terminates with exit code 1

  :param message
  :type message: String
  """
  print(message)
  print(USAGE)
  exit(1)

def get_log_level_from_option(log_level_int):
  """
  Get log level from attila option

  :param log_level_num
  :type int
  :returns logging level
  """
  if log_level_int == LOG_LEVEL_DEBUG:
    return logging.DEBUG
  elif log_level_int == LOG_LEVEL_INFO:
    return logging.INFO
  elif log_level_int == LOG_LEVEL_WARN:
    return logging.WARNING
  elif log_level_int == LOG_LEVEL_ERROR:
    return logging.ERROR
  elif log_level_int == LOG_LEVEL_CRITICAL:
    return logging.CRITICAL
  else:
    return logging.INFO


def main():
  global sigterm_called
  global interactive_mode
  #Options
  script_file = None
  device = None
  baud_rate = None
  default_timeout = 0
  line_break = None
  logfile = None
  log_level = LOG_LEVEL_INFO
  verbose = False
  quiet = False
  abort_on_failure = True
  to_stdout = False

  try:
    optlist, args = getopt(argv[1:], "p::b::T::B::L::l::Avqh")
    if args:
      interactive_mode = False
      script_file = args[0]
    for opt, arg in optlist:
      if opt == "-p":
        device = arg
      elif opt == "-b":
        try:
          baud_rate = int(arg)
        except ValueError:
          opt_error("Specified baud rate is not a number!")
      elif opt == "-T":
        try:
          default_timeout = int(arg)
        except ValueError:
          opt_error("Specified default timeout is not a number!")
      elif opt == "-B":
        line_break = arg
        #Verify line break
        if line_break == "CRLF":
          line_break = "\r\n"
        elif line_break == "LF":
          line_break = "\n"
        elif line_break == "CR":
          line_break = "\r"
        elif line_break == "NONE":
          line_break = None
        else:
          opt_error("Invalid line break '%s'" % line_break)
      elif opt == "-L":
        logfile = arg
      elif opt == "-l":
        try:
          log_level = int(arg)
          if log_level < LOG_LEVEL_CRITICAL or log_level > LOG_LEVEL_DEBUG:
            opt_error("Log level is out of range")
          else:
            log_level = get_log_level_from_option(log_level)
        except ValueError:
          opt_error("Log level is not a number")
      elif opt == "-A":
        try:
          abort_on_failure = eval(arg)
          if abort_on_failure != True and abort_on_failure != False:
            opt_error("Abort on failure has a bad value: '%s', but should be True or False" % abort_on_failure)
        except NameError:
          opt_error("Abort on failure has a bad value")
      elif opt == "-v":
        verbose = True
      elif opt == "-q":
        quiet = True
      elif opt == "-h":
        print(USAGE)
        exit(0)
      else:
        opt_error("Unkown option '%s'" % opt)
  except GetoptError as err:
    opt_error(err)

  #Set signal handlers listener
  signal(SIGTERM, sigterm_handler)
  signal(SIGINT, sigterm_handler)

  #Prepare logger if requested
  if logfile:
    if logfile == "stdout":
      to_stdout = True
      stdout_handler = logging.StreamHandler(stdout)
      stdout_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"))
      logging.getLogger().addHandler(stdout_handler)
    else:
      logging.basicConfig(filename=logfile, level=log_level, format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
  else:
    logging.getLogger().disabled = True
  #Instance ATRuntime environment
  atrunenv = ATRuntimeEnvironment(abort_on_failure)
  #Configure serial
  if device and baud_rate:
    atrunenv.configure_communicator(device, baud_rate, default_timeout, line_break)
    logging.info("Setup communicator (device: %s, baud_rate: %d)" % (device, baud_rate))
    if verbose and not to_stdout:
      print("Setup communicator (device: %s, baud_rate: %d)" % (device, baud_rate))
    #Open serial
    try:
      atrunenv.open_serial()
      logging.info("Serial port opened (%s)" % device)
      if verbose and not to_stdout:
        print("Serial port opened")
    except ATSerialPortError as err:
      logging.error("Could not open serial port: %s" % err)
      if not to_stdout and not quiet:
        print("Could not open serial port: %s" % err)
    except ATREUninitializedError as err:
      logging.error("Uninitialized runtime environment: %s " % err)
      if not to_stdout and not quiet:
        print("Uninitialized runtime environment: %s" % err)
      exit(1)
  #Parse file if set
  if script_file:
    logging.debug("Trying to parse file %s..." % script_file)
    try:
      atrunenv.parse_ATScript(script_file)
    except ATScriptNotFound as err:
      logging.error("Could not find script file %s: %s" % (script_file, err))
      if not to_stdout:
        print("Could not find script file %s: %s" % (script_file, err))
      exit(1)
    except ATScriptSyntaxError as err:
      logging.error("Script Syntax error: %s" % err)
      if not to_stdout:
        print("Script syntax error: %s" % err)
      exit(1)
    #Execute script
    response = 1
    while response and not sigterm_called:
      try:
        response = atrunenv.exec_next()
        if not response:
          continue
        #Handle response
        if response.response and response.command:
          logging.info("%s (%d ms) >> %s" % (response.command.command, response.execution_time, response.response))
          if not to_stdout and not quiet:
            print("%s (%d ms) >> %s" % (response.command.command, response.execution_time, response.response))
        else: #Command failed (this snippet gets executed only if aof is false)
          logging.error("%s (%d ms) >> %s" % (response.command.command, response.execution_time, "\n".join(response.full_response)))
          if not to_stdout and not quiet:
            print("%s (%d ms) >> %s" % (response.command.command, response.execution_time, "\n".join(response.full_response)))
      except ATSerialPortError as err:
        logging.error("Serial Port error: %s" % err)
        if not to_stdout:
          print("Serial Port error: %s" % err)
        if atrunenv.aof:
          break
      except ATRuntimeError as err:
        logging.error("Runtime error: %s" % err)
        if not to_stdout:
          print("Runtime error: %s" % err)
        if atrunenv.aof:
          break
      except ATREUninitializedError as err:
        logging.error("Uninitialized runtime environment: %s " % err)
  else: #Interactive mode
    while not sigterm_called:
      command_line = input(">> ")
      if not command_line:
        continue
      #Parse and execute command
      try:
        response = atrunenv.exec(command_line)
        if response: #Was a command (otherwise was probably ESK)
          if response.response: #Command was successful
            logging.info("%s (%d ms) >> %s" % (response.command.command, response.execution_time, response.response))
            if not to_stdout and not quiet:
              print("<< %s (%d ms) >> %s" % (response.command.command, response.execution_time, response.response))
          else: #Command error
            logging.error("%s (%d ms) >> %s" % (response.command.command, response.execution_time, "\n".join(response.full_response)))
            if not to_stdout and not quiet:
              print("<< %s (%d ms) >> %s" % (response.command.command, response.execution_time, "\n".join(response.full_response)))
        else:
          logging.info("%s >> OK" % command_line)
          if not to_stdout and not quiet:
            print("%s >> OK" % command_line)
      except ATScriptSyntaxError as err:
        logging.error("Syntax error: %s" % err)
        if not to_stdout:
          print("Syntax error: %s" % err)
        continue
      except ATSerialPortError as err:
        logging.error("Serial Port error: %s" % err)
        if not to_stdout:
          print("Serial Port error: %s" % err)
      except ATRuntimeError as err:
        logging.error("Runtime error: %s" % err)
        if not to_stdout:
          print("Runtime error: %s" % err)
  #Close serial
  try:
    atrunenv.close_serial()
  except ATSerialPortError as err:
    logging.error("Could not close serial port: %s" % err)
    if not to_stdout and not quiet:
      print("Could not close serial port: %s" % err)
    exit(1)
  except ATREUninitializedError as err:
    logging.error("Couldn't close serial port, since device was not initialized")
    if verbose and not to_stdout:
      print("Couldn't close serial port, since device was not initialized")
  #Execution terminated
  logging.info("attila terminated with exit code 0")
  if not to_stdout and verbose:
    print("attila terminated with exit code 0")

if __name__ == "__main__":
  main()
