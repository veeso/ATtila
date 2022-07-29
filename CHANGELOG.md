# Changelog

- [Changelog](#changelog)
  - [1.2.1](#121)
  - [ATtila 1.2.0 (30/05/2020)](#attila-120-30052020)
  - [ATtila 1.1.6 (25/03/2020)](#attila-116-25032020)
  - [ATtila 1.1.5 (09/03/2020)](#attila-115-09032020)
  - [ATtila 1.1.4 (05/03/2020)](#attila-114-05032020)
  - [ATtila 1.1.3 (07/12/2019)](#attila-113-07122019)
  - [ATtila 1.1.2 (29/10/2019)](#attila-112-29102019)
  - [ATtila 1.1.1 (26/10/2019)](#attila-111-26102019)
  - [ATtila 1.1.0 (26/10/2019)](#attila-110-26102019)
  - [ATtila 1.0.4 (13/10/2019)](#attila-104-13102019)
  - [ATtila 1.0.3 (12/10/2019)](#attila-103-12102019)

## 1.2.1

Released on 29/07/2022

- [Fixed get_session_value returning None](https://github.com/veeso/ATtila/pull/4)
- Better typing definition
- Code improvements

## ATtila 1.2.0 (30/05/2020)

- New ESK
  - RTSCTS
  - DSRDTR
  - WRITE
- ATtila CLI
  - History
- Changed minimum Python version to 3.5
- Code
  - Type annotations
  - Indentation to 4 spaces

## ATtila 1.1.6 (25/03/2020)

- Fixed response collection

## ATtila 1.1.5 (09/03/2020)

- Fixed serial communication which didn't wait for all input
  - Serial is now slower, especially for lower baudrate

## ATtila 1.1.4 (05/03/2020)

- Fixed slow serial read when working with low baud rates
- Added ```rtscts=True, dsrdtr=True``` options to serial open
- Serial Write is no more blocking
- Fixed doppelganger and collectables

## ATtila 1.1.3 (07/12/2019)

- Fixed a typo in ATRE for ESK EXEC (commit ref: 8506523)

## ATtila 1.1.2 (29/10/2019)

- Fixed broken windows installation

## ATtila 1.1.1 (26/10/2019)

- Didn't deploy virtual.

## ATtila 1.1.0 (26/10/2019)

- Fixed device not None after serial close
- Fixed ATCommand response getter
- Added SyntaxError exception handler in ATScriptParser
- Fixed value getter in ESK
- Added Virtual Serial device
- Test improvements

## ATtila 1.0.4 (13/10/2019)

- Added codecov
- Added missing CR value in BREAK ESK
- Added ESK and ATRE tests

## ATtila 1.0.3 (12/10/2019)

- Fixed help in main
- Added Travis
