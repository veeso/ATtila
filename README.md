# ATtila

Developed by *Christian Visintin*

Current Version: **currently under development**

---

## Introduction

ATtila is a Python module which purpose is to ease the communication with an RF module which uses AT commands. It is both possible to send single AT commands indicating what response is expected and AT scritps which indicate all the commands to send, the expected response for each command, what information to store for each command and define an alternative behaviour in case of unexpected responses.
These are the main functionalities that ATtila provides:

- Send of a single AT command to RF module/modem through serial port and get the response for them
- Send of multiple AT commands using “ATScripts”. ATScripts in particular allows you to:
  - Define a set of commands to execute on the RF module
  - Get the response and choose what information to store for each commands
  - Use the response of a certain command in a command which will be executed later
  - Define alternative behaviour in case of error

## Implementation

TBD

## ATScript

TBD

## Known Issues

## Changelog

---

## License

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
