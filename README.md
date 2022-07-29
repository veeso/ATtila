# ATtila

<p align="center">
  <a href="CHANGELOG.md" target="_blank">Changelog</a>
  ·
  <a href="#get-started-" target="_blank">Get started</a>
  ·
  <a href="docs/atscript.md" target="_blank">Documentation</a>
</p>

<p align="center">~ Communicate easily with modems and RF modules using AT commands ~</p>

<p align="center">Developed by <a href="https://veeso.github.io/" target="_blank">@veeso</a></p>
<p align="center">Current version: 1.2.1 (29/07/2022)</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"
    ><img
      src="https://img.shields.io/badge/License-MIT-teal.svg"
      alt="License-MIT"
  /></a>
  <a href="https://github.com/veeso/ATtila/stargazers"
    ><img
      src="https://img.shields.io/github/stars/veeso/ATtila.svg"
      alt="Repo stars"
  /></a>
  <a href="https://pypi.org/project/attila/"
    ><img
      src="https://badge.fury.io/py/attila.svg"
      alt="latest version"
  /></a>
  <a href="https://pepy.tech/project/attila"
    ><img
      src="https://pepy.tech/badge/attila"
      alt="download counters"
  /></a>
  <a href="https://ko-fi.com/veeso">
    <img
      src="https://img.shields.io/badge/donate-ko--fi-red"
      alt="Ko-fi"
  /></a>
</p>
<p align="center">
  <a href="https://github.com/veeso/ATtila/actions"
    ><img
      src="https://github.com/veeso/ATtila/workflows/Build/badge.svg"
      alt="Build CI"
  /></a>
  <a href="https://codecov.io/gh/veeso/ATtila"
    ><img
      src="https://codecov.io/gh/veeso/ATtila/branch/main/graph/badge.svg"
      alt="Coveragg"
  /></a>
</p>

---

- [ATtila](#attila)
  - [About ATtila 📢](#about-attila-)
  - [Requirements 🛒](#requirements-)
  - [Get Started 🛠](#get-started-)
    - [Virtual Device ⌨](#virtual-device-)
  - [ATScripts 💻](#atscripts-)
  - [Contributions 🤝🏻](#contributions-)
  - [Known Issues 🧻](#known-issues-)
  - [Changelog 🕑](#changelog-)
  - [Branches 🌳](#branches-)
  - [Support the developer ☕](#support-the-developer-)
  - [License 📜](#license-)

---

```sh
pip3 install attila
```

## About ATtila 📢

ATtila is both a **Python3 🐍 module and a CLI utility**.
The module's purpose is to ease the communication with devices through serial port, automating the scripts execution workflow; in particular ATtila is designed for RF modules which use AT commands.

It is both possible to send single AT commands indicating what is the expected response, what information to store for each command and define an alternative behaviour in case of an unexpected responses.  
These are the main functionalities that ATtila provides:

- Façade to communicate with the serial devices
- Sending AT commands and define the expected response for it
- Collect values from response and store them in the session storage
- Define a command to execute in case the previously executed command fails
- Sending individual AT command to RF module/modem through serial port and get the response

ATtila comes, as said before, with a binary (which can be used instead of the classic `chat` binary) to pair with `pppd`, or for anything you want.
You can run ATtila binary with

```sh
python3 -m attila
#Or if installed, just
attila
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

## Requirements 🛒

- Python3.5 (>= 1.2.0)
  - Python3.4 (up to 1.1.x - switch to ```1.1.x``` branch)
- pyserial3

## Get Started 🛠

In order to build your own implementation using ATtila these are the steps you need to follow:

1. Import the AT Runtime Environment into your project

    The first thing you have to do is to import the AT Runtime Environment and the exceptions it can raise in your project

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

    Be careful, this function can return an `ATSerialPortError`

    ```py
    atrunenv.open_serial()
    ```

5. Choose how to parse commands:

    1. Parse an ATScript

        parse_ATScript can raise `ATScriptNotFound` or `ATScriptSyntaxError`

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

        if `abort_on_failure` is `True`, the ATRE will raise `ATRuntimeError` during execution  

        ```py
        response_list = atrunenv.run()
        ```

    2. Run one command a time (if `abort_on_failure` is True, the ATRE will raise `ATRuntimeError`):

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

### Virtual Device ⌨

Since version 1.1.0, it is possible to use a virtual serial device, instead of a real one. This has been introduced for test purposes, but can actually be used in case you need to emulate a serial device and you want to keep using ATtila.
In this case, in the ATRE, instead of using `configure_communicator` use:

```py
def configure_virtual_communicator(self, serial_port, baud_rate, timeout = None, line_break = "\r\n", read_callback = None, write_callback = None, in_waiting_callback = None)
```

The virtual communicator, in addition to the standard one, requires a `read`, a `write` and an `in_waiting` callback. These callbacks must replace the I/O operations of the serial device, with something else (e.g. a socket with an HTTP request)

## ATScripts 💻

ATtila uses its own syntax to communicate with the serial device, which is called **ATScript** (ATS).
The basic syntax for it, is:

```txt
COMMAND;;RESPONSE_EXPR;;DELAY;;TIMEOUT;;["COLLECTABLE1",...];;DOPPELGANGER;;DOPPELGANGER_RESPONSE
```

To know more about ATS see the [ATScript documentation](./docs/atscript.md)

---

## Contributions 🤝🏻

Contributions are welcome! 😉

If you think you can contribute to ATtila, please follow ATtila's [Contributions Guidelines](CONTRIBUTING.md)

---

## Known Issues 🧻

None, as far as I know at least.

---

## Changelog 🕑

View Changelog [HERE](CHANGELOG.md)

---

## Branches 🌳

- master: stable only with latest features
- 1.1.x: LTS with Python3.4 support; this version will receive only patch for major issues
- dev: main development branch
- other features

---

## Support the developer ☕

If you like ATtila and you're grateful for the work I've done, please consider a little donation 🥳

You can make a donation on the following platforms:

[![ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/veeso)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.me/chrisintin)

---

## License 📜

View [LICENSE HERE](LICENSE)
