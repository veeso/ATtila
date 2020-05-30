# Developers Guide

- [Developers Guide](#developers-guide)
  - [Introduction](#introduction)
  - [SubModules and Classes](#submodules-and-classes)
    - [Modules](#modules)
      - [ATRE](#atre)
      - [ATCommunicator](#atcommunicator)
      - [ATSession](#atsession)
      - [ATScriptParser](#atscriptparser)
    - [Classes](#classes)
      - [ATCommand](#atcommand)
      - [ATResponse](#atresponse)
      - [ESK](#esk)

## Introduction

This is the ATtila's developers guide. This document describes how ATtila works to ease the developer to contribute to the project.

Consider that each function is documented following the **reStructuredText** standard. The documentation for each function can directly be read in the source code.

## SubModules and Classes

ATtila is made up of 4 main modules, in addition there are different entities.
The main modules of ATtila are:

- [ATRE](#atre) (AT Runtime Environment)
- [ATCommunicator](#atcommunicator)
- [ATSession](#atsession)
- [ATScriptParser](#atscriptparser)

### Modules

#### ATRE

The AT runtime environment is the main component, and the only module that should be used to interface with the library by the user.
It instantiates an ATCommunicator to create a communication channel with the AT module, an ATSession to store the session values and to evaluate the responses and an ATScriptParser to parse the user's input.

#### ATCommunicator

The ATCommunicator is the module which takes care of creating a communication channel with the AT module through a serial port. It provides function to open/close the channel and to send and receive data from it.

#### ATSession

The ATSession is the module which takes care of parsing the response and to store in the session storage the values collected from the response. It also takes care of providing the next command to perform (based also on the last command's doppelganger and result).

#### ATScriptParser

The ATScriptParser is the module which takes care of parsing the ATS statements. Given a file or a stream of rows, it returns the ESKs and the ATCommands parsed from the source content.

---

### Classes

#### ATCommand

This class represents an AT command.  
An ATCommand is represented by the raw string command, the expected response, the timeout for its execution, the execution delay, the collectables, the response and an optional the doppelganger.

#### ATResponse

This class represents a response for an ATCommand.
It provides access to the expected response format, the entire response and the command execution time (milliseconds)

#### ESK

This class represents an Environment Setup Keyword value
