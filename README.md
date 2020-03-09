# ATtila

[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT) [![Stars](https://img.shields.io/github/stars/ChristianVisintin/ATtila.svg)](https://github.com/ChristianVisintin/ATtila) [![Issues](https://img.shields.io/github/issues/ChristianVisintin/ATtila.svg)](https://github.com/ChristianVisintin/ATtila/) [![PyPI version](https://badge.fury.io/py/attila.svg)](https://pypi.org/project/attila/) [![Build](https://api.travis-ci.org/ChristianVisintin/ATtila.svg?branch=master)](https://travis-ci.org/ChristianVisintin/ATtila) [![codecov](https://codecov.io/gh/ChristianVisintin/ATtila/branch/master/graph/badge.svg)](https://codecov.io/gh/ChristianVisintin/ATtila)

Developed by *Christian Visintin*

Current Version: **1.1.5 (09/03/2020)**

- [ATtila](#attila)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Implementation](#implementation)
    - [Virtual Device](#virtual-device)
  - [ATScript](#atscript)
    - [ATScript Introduction](#atscript-introduction)
    - [ATScript Commands](#atscript-commands)
      - [Examples](#examples)
        - [Basic command](#basic-command)
        - [Command and expected response](#command-and-expected-response)
        - [Delay and timeout](#delay-and-timeout)
      - [Doppelgangers](#doppelgangers)
      - [Collectables](#collectables)
      - [Session Values](#session-values)
    - [Environment Setup Keywords](#environment-setup-keywords)
    - [Let's put it all together](#lets-put-it-all-together)
  - [Known Issues](#known-issues)
  - [Tests Units](#tests-units)
  - [Changelog](#changelog)
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
  - Python3.4 (up to 1.1.4)
- pyserial3

## Implementation

In order to build your own implementation using ATtila these are the steps you'll need to follow:

1. The first thing you have to do is import the AT Runtime Environment and the exceptions it can raise in your project:  
  ```from attila.atre import ATRuntimeEnvironment```  
  ```from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError```
2. Instance an ATRuntimeEnvironment object:  
  ```atrunenv = ATRuntimeEnvironment(abort_on_failure)```
3. Configure the communicator, the component which will communicate with your device:  
  ```atrunenv.configure_communicator(device, baud_rate, default_timeout, line_break)```
4. Open the serial port (Be careful, this function can return a ATSerialPortError):  
  ```atrunenv.open_serial()```
5. Choose how to parse commands:
   1. Parse an ATScript (parse_ATScript can raise ATScriptNotFound or ATScriptSyntaxError):  
    ```atrunenv.parse_ATScript(script_file)```
   2. Execute directly a command (or an ESK):
    ```response = atrunenv.exec(command_str)```
   3. Add an ATCommand to the session:
    ```atrunenv.add_command(command_str)```
6. Execute commands:
   1. Run everything at once and then get a list of ATResponse (if abort_on_failure is True, the ATRE will raise ATRuntimeError during execution):  
    ```response_list = atrunenv.run()```
   2. Run one command a time (if abort_on_failure is True, the ATRE will raise ATRuntimeError):
    ```response = atrunenv.exec_next()```
7. Collect the values you need:  
  ```rssi = atrunenv.get_session_value("rssi")```
8. Close serial: ```atrunenv.close_serial()```

### Virtual Device

Since version 1.1.0, it is possible to use a virtual serial device, instead of a real one. This has been introduced for tests purpose, but can actually used in cases where you need to emulate a serial device and you want to keep using ATtila.
In this case, in the ATRE, instead of using configure_communicator use:

```py
def configure_virtual_communicator(self, serial_port, baud_rate, timeout = None, line_break = "\r\n", read_callback = None, write_callback = None, in_waiting_callback = None)
```

The virtual communicator, in addition to the standard one, requires a read, a write and an in waiting callback. These callbacks must replace the I/O operations of the serial device, with something else (e.g. a socket with an HTTP request)

## ATScript

### ATScript Introduction

ATScript is the most important feature of ATtila, since it allows to execute a set of AT commands (*well, not only AT based to be honest...*) sequentially and evaluate, store and combine their output.

Basically in an AT scripts there are three things:

- **Commands**: describe what you want to send to the device and how to treat its response.
- **Environment Setup Keywords**: describes how to establish and manage the communication.
- **Comments**: you can obviously put comments in the ATScripts, the ATScriptParser will just ignore them. A comment statement must start with '#' character.

### ATScript Commands

Obviously the most important feature of ATScripts is the possibility to execute AT Commands.
As far as we’ve learned up to now, we know that a command has the following parameters:

- the **command** itself
- the **response** we expect
- the **doppelganger** and it's expected response
- **collectables**
- a **delay** (milliseconds to wait before its execution)
- a **timeout**

So basically, to think it easy, the syntax for commands will be a combination of them:

```txt
COMMAND;;RESPONSE_EXPR;;DELAY;;TIMEOUT;;["COLLECTABLE1","...","COLLECTABLEn"];;DOPPELGANGER;;DOPPELGANGER_RESPONSE
```

To see practical applications of them, let's see a few examples.

#### Examples

We’ll start with a simple one: the "AT" command

The most basic usable syntax is just:

##### Basic command

```txt
AT
```

##### Command and expected response

but you probably want at least to verify if its response is what you expect:

```txt
AT;;OK
```

We told ATtila that we expect to find “OK” in the command response.
We can also use a regex in the expected response, for example if a command returns 16 hex digits, we can use

```txt
AT+GSN;;^[0-9,A-F]{16}$
```

##### Delay and timeout

Then we can also add a delay before command execution (in milliseconds) and a timeout (in seconds)

```txt
AT;;OK;;1000;;5
```

These commands don’t have all the available parameters, we still need to go deep and the see **doppelgangers and collectables** concepts.

#### Doppelgangers

In the previous example we’ve seen the basic parameters associated to a command, but now I want to introduce you the doppelganger feature included in ATScripts. Imagine for instance that we want to set the SIM pin, but only if it requires to be unlocked (This is a situation I’ve encountered many times at job where there could be devices with locked and unlocked PIN, but the chat script was the same).
We’ll use AT+CPIN?, in case the SIM is unlocked it will return “+CPIN:READY”; we want to set the PIN only if returns something else. (If locked, returns “CPIN:SIM PIN”)
The command we’ll use is:

```txt
AT+CPIN?;;READY;;0;;5;;;;AT+CPIN=7782;;OK
```

What does this command mean?
It tells ATtila to send AT+CPIN? and that we expect to find "READY" string in the response. If READY is found in the response it will proceed with the next command, but what happens for example if the device answers with “+CPIN: SIM PIN”? The ATSession will set as next command its doppelganger, which is AT+CPIN=7782, which will be executed as the next command.

#### Collectables

The last, but not least important parameter you can set in a command is collectables.
Collectables are values that you can collect from a command response and transform into a **session value** (we’ll talk about session values in the next chapter).
Imagine for example you want to collect the current signal quality and store it into a variable you want for example to save on Redis, you can do it just by specifying what you’re looking for and the session value name and the job is done: ATila will do the job for you!

```txt
AT+CSQ:;;+CSQ;;0;;5;;["AT+CSQ=?{rssi},","AT+CSQ=${rssi},?{ber}"]
```

This command has two collectables, which are the rssi and the Ber. We know that AT+CSQ, in case of a positive response (+CSQ:...), will return the **rssi and the ber** after “AT+CSQ=” separated by a comma. Imagine that we want to get both. The first value we want is located after “AT+CSQ=” and terminates with the ',' comma before the ber. So we tell ATtila to get a value between these two strings and to store it into a session value called “rssi”. The other value will be located after the other part of the string; we can as you can see, reuse the rssi value in the second collectable (since rssi is already set).
The syntax which describes the start of a collectable is **?{SESSION_KEY}**.

This was a simple case, where we knew the value where between 'AT+CSQ=...,' and after 'AT+CSQ=rssi,...'. But sometimes we have to get a value which hasn't anything around. An example of this case is AT+CGSN, which returns the IMEI. The IMEI is returned on a line, with nothing around:

```txt
AT+CGSN
123456789012345
OK
```

How can we get this value using collectables? Well, we can, but making a collectable a little more bit complex. We need to use a key regex:

```txt
AT+CGSN;;OK;;;;;;["?{IMEI::^[0-9]{15}$}"]
```

This means we're looking for a value between nothing, but which has to respect the regex we provided which is ```^[0-9]{15}$```. If a number of 15 digits is found in the response, this value will be stored into the session storage into a key named "IMEI".
The separator between the **key name** and the **key regex** is ```::```
This mechanism can also be used to solve ambiguity in the response to get the value that we really want.

For example we can make a more severe check on the CSQ using:

```txt
AT+CSQ;;OK;;;;;;["AT+CSQ=?{rssi::[0-9]{1,2}},","AT+CSQ=${rssi},?{ber::[0-9]{1,2}}"]
```

#### Session Values

We’ve seen that session values are values we can store using collectables and also setting environment variables and through Environment Setup Keywords, but we’ll see that in the next chapter.
A session value **is just a key associated to a value**, stored in the **session storage**. The session storage is a dictionary made up of all the session values, it lives only for the current command set, when a new session is instanced, the session storage is empty again.
*It’s not that complicated.*

We can rethink the previous example of CPIN using session values.
The script which set the SIM PIN only if locked, could be a part of an image installed on plenty of devices, but we can’t have a different script for each device and using a script which replace runtime the text with the configured PIN is not such a good way to do things.
Here is where the power of session values comes in help!
The SIM pin could be for instance, written example in a configuration file and we want to set it as a session value.
If before the execution of our script, we execute “export SIM_PIN=7782” and then we execute this row in ATila using GETENV (we'll see what GETENV is in the next chapter) somewhere in the script before its execution.

```txt
GETENV SIM_PIN
AT+CPIN;;READY;;0;;5;;;;AT+CPIN=${SIM_PIN};;OK
```

SIM_PIN will be replaced by 7782.

But as we seen in the previous chapter, Session values can also be used to get collectables (if we already know a value that will be for sure in the response).

### Environment Setup Keywords

As said before, ATScripts are not made only up of commands, but also of another thing called **Environment Setup Keywords (ESKs)**.
Let’s start from talking briefly about how ATtila works. ATtila has two main components: the **AT Runtime Environment (ATRE)** and the **ATSession**. The AT Runtime Environment instances a session and executes it following its commands, when the session execution ends, a new session can be instanced and the previous one gets destroyed, while the runtime environment persists. While **commands describe the ATSession execution path**, the **ESKs describe the setup for the AT Runtime Environment**, not only at the initial setup, but also at any time during runtime. ESKs can also be used to invoke the ATRE to execute some commands as we'll see..
So, to summarize, **ESKs are commands you can put (but are not mandatory) in your scripts and tell the Runtime Environment how to configure its components or extra instructions to be executed**.
Let’s see then which ESKs are supported.

| ESK      | Value                         | Description                                                                                              |
|----------|-------------------------------|----------------------------------------------------------------------------------------------------------|
| DEVICE   | String                        | Indicates the target device used to communicate (e.g. /dev/ttyUSB0)                                      |
| BAUDRATE | Int                           | Describes the baud rate used to communicate (e.g. 9600)                                                  |
| TIMEOUT  | Int                           | Describes the default command timeout (e.g. 5)                                                           |
| BREAK    | "LF" / "CRLF" / "CR" / "NONE" | Describes the line break used for commands between LF and CRLF                                           |
| AOF      | True / False                  | Abort on failure: describes whether the runtime environment shut abort on command failure                |
| SET      | String=String                 | Tells ATRE to set a session value with a certain key and value: (e.g. SET SIM=7789)                      |
| GETENV   | String                        | Tells ATRE to store in session storage a certain environmental variable. (e.g. GETENV SIM_PIN)           |
| PRINT    | String                        | Tells ATRE to print to stdout a string (e.g. PRINT SIM PIN: ${SIM_PIN})                                  |
| EXEC     | String                        | Tells ATRE to execute a shell process (e.g. EXEC “export SIM_PIN=`cat /tmp/config.json | jq .modem.pin`” |

### Let's put it all together

Now that we know everything about ATScripts, let's build a Modem dial script :D

```txt
#Set up communication parameters
DEVICE /dev/ttyUSB0
BAUDRATE 115200
TIMEOUT 10
BREAK CRLF
#Abort on failure
AOF True
#Get the SIM PIN and the APN
GETENV SIM_PIN
GETENV APN
#Let's start with modem setup
PRINT Configuring modem parameters
#+++ doesn't want a break
BREAK NONE
+++
BREAK CRLF
ATH0;;;;5000
ATE0;;OK
ATZ;;OK
ATE0;;OK
#I'm going to verify signal etc, we don't need to aof
AOF False
AT+CSQ;;OK;;;;;;["AT+CSQ=?{rssi::[0-9]{1,2}},","AT+CSQ=${rssi},?{ber::[0-9]{1,2}}"]
AT+CGSN;;OK;;;;;;["?{IMEI::^[0-9]{15}$}"]
AT+CREG?;;OK
#Now I'm configuring modem for dialup, so AOF it's important
AOF True
AT+CPIN?;;READY;;0;;5;;;;AT+CPIN=${SIM_PIN};;OK
AT+CGDCONT=1,"IP","${APN}";;OK;;1000
#Dial APN
PRINT Dialing your ISP...
AT+CGDATA="PPP",1;;CONNECT
```

## Known Issues

None, as far as I know at least.

## Tests Units

ATtila is provided with tests units, which can be found under tests/ directory.
These tests units tests the three most important parts of ATtila which are the ATScriptParser, the ATSession and the ATRuntimeEnvironment.
To launch test unit just type:

```sh
nosetests -v --with-coverage --cover-tests --cover-package=attila --nocapture tests/
```

## Changelog

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

```txt
MIT License

Copyright (c) 2019 Christian Visintin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
