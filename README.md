# ATtila

[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT) [![Stars](https://img.shields.io/github/stars/ChristianVisintin/ATtila.svg)](https://github.com/ChristianVisintin/ATtila) [![Issues](https://img.shields.io/github/issues/ChristianVisintin/ATtila.svg)](https://github.com/ChristianVisintin/ATtila/) [![PyPI version](https://badge.fury.io/py/attila.svg)](https://pypi.org/project/attila/) [![Build](https://api.travis-ci.org/ChristianVisintin/ATtila.svg?branch=master)](https://travis-ci.org/ChristianVisintin/ATtila) [![codecov](https://codecov.io/gh/ChristianVisintin/ATtila/branch/master/graph/badge.svg)](https://codecov.io/gh/ChristianVisintin/ATtila)

Developed by *Christian Visintin*

Current Version: **1.1.6 (25/03/2020)**

- [ATtila](#attila)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Get Started](#get-started)
    - [Virtual Device](#virtual-device)
  - [ATScript](#atscript)
  - [Known Issues](#known-issues)
  - [Changelog](#changelog)
    - [ATtila 1.1.6 (25/03/2020)](#attila-116-25032020)
    - [ATtila 1.1.5 (09/03/2020)](#attila-115-09032020)
    - [ATtila 1.1.4 (05/03/2020)](#attila-114-05032020)
    - [ATtila 1.1.3 (07/12/2019)](#attila-113-07122019)
    - [ATtila 1.1.2 (29/10/2019)](#attila-112-29102019)
    - [ATtila 1.1.1 (26/10/2019)](#attila-111-26102019)
    - [ATtila 1.1.0 (26/10/2019)](#attila-110-26102019)
    - [ATtila 1.0.4 (13/10/2019)](#attila-104-13102019)
    - [ATtila 1.0.3 (12/10/2019)](#attila-103-12102019)
  - [Branches](#branches)
  - [License](#license)

---

```sh
pip3 install attila
```

## Introduction

ATtila is a Python module which purpose is to ease the communication with an RF module which uses AT commands. It is both possible to send single AT commands indicating what response is expected and AT scritps which indicate all the commands to send, the expected response for each command, what information to store for each command and define an alternative behaviour in case of unexpected responses.  
These are the main functionalities that ATtila provides:

- Sending individual AT command to RF module/modem through serial port and get the response for them
- Sending of multiple AT commands using “ATScripts”. ATScripts in particular allows you to:
  - Define a set of commands to execute on the RF module
  - Get the response and choose what information to store for each commands
  - Use the response of a certain command in a command which will be executed later
  - Define alternative behaviour in case of error

ATtila comes with a binary (which should be used instead of chat in my opinion) or for anything you want.
You can run ATtila binary with

```sh
python3 -m attila
```

```txt
Usage: attila [OPTION]... [FILE]

  With no FILE, run in interactive mode

  -p  <device path>     Use this device to communicate
  -b  <baud rate>       Use the specified baudrate to communicate
  -T  <default timeout> Use the specified timeout as default to communicate
  -B  <break>           Use the specified line break [CRLF, LF, CR, NONE] (Default: CRLF)
  -A  <True/False>      Abort on failure (Default: True)
  -L  <logfile>         Enable log and log to the specified log file (stdout is supported)
  -l  <loglevel>        Specify the log level (0: CRITICAL, 1: ERROR, 2: WARN, 3: INFO, 4: DEBUG) (Default: INFO)
  -v                    Be more verbose
  -q                    Be quiet (print only PRINT ESKs and ERRORS)
  -h                    Show this page
```

## Requirements

- Python3.5 (>= 1.2.0)
  - Python3.4 (up to 1.1.x)
- pyserial3

## Get Started

In order to build your own implementation using ATtila these are the steps you'll need to follow:

1. Import the AT Runtime Environment into your project

    The first thing you have to do is import the AT Runtime Environment and the exceptions it can raise in your project

    ```py
    from attila.atre import ATRuntimeEnvironment
    from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError
    ```  

2. Instantiate an ATRuntimeEnvironment object

    ```py
    atrunenv = ATRuntimeEnvironment(abort_on_failure)
    ```

3. Configure the communicator

    This is the component which will communicate with your device

    ```py
    atrunenv.configure_communicator(device, baud_rate, default_timeout, line_break)
    ```

4. Open the serial port

    Be careful, this function can return a ATSerialPortError

    ```py
    atrunenv.open_serial()
    ```

5. Choose how to parse commands:

    1. Parse an ATScript

        parse_ATScript can raise ATScriptNotFound or ATScriptSyntaxError

        ```py
        atrunenv.parse_ATScript(script_file)
        ```

    2. Execute directly a command (or an ESK)

        ```py
        response = atrunenv.exec(command_str)
        ```

    3. Add an ATCommand to the session

        ```py
        atrunenv.add_command(command_str)
        ```

6. Execute commands:
    1. Run everything at once and then get a list of ATResponse

        if abort_on_failure is True, the ATRE will raise ATRuntimeError during execution  

        ```py
        response_list = atrunenv.run()
        ```

    2. Run one command a time (if abort_on_failure is True, the ATRE will raise ATRuntimeError):

        ```py
        response = atrunenv.exec_next()
        ```

7. Collect the values you need

    ```py
    rssi = atrunenv.get_session_value("rssi")
    ```

8. Close serial

    ```py
    atrunenv.close_serial()
    ```

### Virtual Device

Since version 1.1.0, it is possible to use a virtual serial device, instead of a real one. This has been introduced for tests purpose, but can actually used in cases where you need to emulate a serial device and you want to keep using ATtila.
In this case, in the ATRE, instead of using configure_communicator use:

```py
def configure_virtual_communicator(self, serial_port, baud_rate, timeout = None, line_break = "\r\n", read_callback = None, write_callback = None, in_waiting_callback = None)
```

The virtual communicator, in addition to the standard one, requires a read, a write and an in waiting callback. These callbacks must replace the I/O operations of the serial device, with something else (e.g. a socket with an HTTP request)

## ATScript

ATtila uses its own syntax to communicate with the serial device, which is called **ATScript** (ATS).
The basic syntax for it is:

```txt
COMMAND;;RESPONSE_EXPR;;DELAY;;TIMEOUT;;["COLLECTABLE1",...];;DOPPELGANGER;;DOPPELGANGER_RESPONSE
```

To know more about ATS see the [ATScript documentation](./docs/atscript.md)

## Known Issues

None, as far as I know at least.

## Changelog

### ATtila 1.1.6 (25/03/2020)

- Fixed response collection

### ATtila 1.1.5 (09/03/2020)

- Fixed serial communication which didn't wait for all input
  - Serial is now slower, especially for lower baudrate

### ATtila 1.1.4 (05/03/2020)

- Fixed slow serial read when working with low baud rates
- Added ```rtscts=True, dsrdtr=True``` options to serial open
- Serial Write is no more blocking
- Fixed doppelganger and collectables

### ATtila 1.1.3 (07/12/2019)

- Fixed a typo in ATRE for ESK EXEC (commit ref: 8506523)

### ATtila 1.1.2 (29/10/2019)

- Fixed broken windows installation

### ATtila 1.1.1 (26/10/2019)

- Didn't deploy virtual.

### ATtila 1.1.0 (26/10/2019)

- Fixed device not None after serial close
- Fixed ATCommand response getter
- Added SyntaxError exception handler in ATScriptParser
- Fixed value getter in ESK
- Added Virtual Serial device
- Test improvements

### ATtila 1.0.4 (13/10/2019)

- Added codecov
- Added missing CR value in BREAK ESK
- Added ESK and ATRE tests

### ATtila 1.0.3 (12/10/2019)

- Fixed help in main
- Added Travis

## Branches

- master: stable only
- dev: main development branch
- other features

---

## License

View [LICENSE HERE](LICENSE)
