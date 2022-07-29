from .atsession import ATSession
from .atcommand import ATCommand, ATResponse
from .esk import ESKValue, ESK
from .atscriptparser import ATScriptParser
from .exceptions import (
    ATScriptNotFound,
    ATScriptSyntaxError,
    ATSerialPortError,
    ATREUninitializedError,
    ATRuntimeError,
)
from .atcommunicator import ATCommunicator
from .virtual.atvirtualcommunicator import ATVirtualCommunicator

from os import environ, system
from time import sleep

from typing import Callable, List, Optional, Tuple, Union


class ATRuntimeEnvironment(object):
    """
    This class represents the AT Runtime Environment which is the main component of
    ATtila, and the only one that should be instanced by the final user.
    The ATRE takes care of handling the communication between the session and the device and
    of the command execution flow
    """

    def __init__(self, abort_on_failure: bool = True):
        """
        Class constructor. Instantiates a new :class:`.ATRuntimeEnvironment.` object with the provided parameters.

        :param abort_on_failure
        :type abort_on_failure bool
        """
        self.__session = ATSession([])
        self.__communicator = ATCommunicator(None, None)
        self.__script_parser = ATScriptParser()
        self.__esks = []
        self.__virtual_communicator = False
        # ES Params
        self.__aof: bool = abort_on_failure
        self.__current_command = 0

    @property
    def aof(self):
        return self.__aof

    def configure_communicator(
        self,
        serial_port: str,
        baud_rate: int,
        timeout: int = None,
        line_break: str = "\r\n",
        rtscts: Optional[bool] = True,
        dsrdtr: Optional[bool] = True,
    ) -> None:
        """
        Configure ATRE communicator

        :param serial_port: Serial port for the communicator
        :param baud_rate: Baud rate used
        :param timeout: default timeout for commands
        :param line_break: line break used by the device
        :param rtscts: use rtscts
        :param dsrdtr: use dsrdtr
        :type serial_port: String
        :type baud_rate: int
        :type timeout: int
        :type line_break: String
        :type rtscts: bool
        :type dsrdtr: bool
        """
        if self.__communicator:  # If device is open, close device
            if self.__communicator.is_open():
                self.__communicator.close()
        if self.__virtual_communicator:
            self.__communicator = ATCommunicator(serial_port, baud_rate)
        self.__virtual_communicator = False
        self.__communicator.serial_port = serial_port
        self.__communicator.baud_rate = baud_rate
        self.__communicator.default_timeout = timeout
        self.__communicator.line_break = line_break
        self.__communicator.dsrdtr = dsrdtr
        self.__communicator.rtscts = rtscts

    def configure_virtual_communicator(
        self,
        serial_port: str,
        baud_rate: int,
        timeout: int = None,
        line_break: str = "\r\n",
        read_callback: Optional[Callable[[], str]] = None,
        write_callback: Optional[Callable[[str], None]] = None,
        in_waiting_callback: Optional[Callable[[], int]] = None,
    ) -> None:
        """
        Configure ATRE Virtual communicator

        :param serial_port: Serial port for the communicator
        :param baud_rate: Baud rate used
        :param timeout: default timeout for commands
        :param line_break: line break used by the device
        :param read_callback (optional): Specify a read function to call to read using the virtual communicator
        :param write_callback (optional): Specifiy a write funtion to call to write using the virtual communicator
        :param in_waiting_callback (optional): Specify a in waiting function to call
        :type serial_port: String
        :type baud_rate: int
        :type timeout: int
        :type line_break: String
        :type read_callback: function which returns string and takes nbytes as argument, if nbytes is -1 returns all lines
        :type write_callback: function which takes string and raises VirtualSerialException
        :type in_waiting_callback: function which returns True if there are data available to read
        """
        if self.__communicator:  # If device is open, close device
            if self.__communicator.is_open():
                self.__communicator.close()
        self.__virtual_communicator = True
        self.__communicator = ATVirtualCommunicator(
            serial_port,
            baud_rate,
            timeout,
            line_break,
            read_callback,
            write_callback,
            in_waiting_callback,
        )

    def init_session(self, commands: List[ATCommand]) -> None:
        """
        Initialize a new ATSession

        :param commands
        :type commands: Array of ATCommands
        """
        self.__session.reset()
        for command in commands:
            self.__session.add_command(command)

    def set_ESKs(self, esks: Tuple[ESKValue, int]) -> None:
        """
        Set ATRE Environment Setup Keywords
        The previous ESKs will be overwritten, the newer will be associated to the current session

        :param esks
        :type esks: tuple of (ESKValue, execution_index)
        """
        self.__esks = esks

    def parse_ATScript(self, script_file: str) -> None:
        """
        Parse an AT Script file

        :param script: Script content
        :type script_file: String
        :raises ATScriptSyntaxError, ATScriptNotFound
        """
        try:
            parse_result = self.__script_parser.parse_file(script_file)
        except ATScriptNotFound as err:
            raise err
        except ATScriptSyntaxError as err:
            raise err
        commands = parse_result[0]
        esks = parse_result[1]
        self.init_session(commands)
        self.set_ESKs(esks)

    def add_command(self, command: ATCommand) -> bool:
        """
        Add an ATCommand to the ATSession

        :param command: at command to add
        :type command: ATCommand
        :returns bool
        """
        return self.__session.add_command(command)

    def run(self) -> List[ATResponse]:
        """
        Starts and run current ATSession

        :returns List of ATResponse
        :raises ATSerialPortError, ATRuntimeError, ATREUninitializedError
        """
        # Open serial port to initialize communication with device
        if not self.__communicator or not self.__session:
            raise ATREUninitializedError("AT Runtime Environment is not initialized")
        try:
            self.open_serial()
        except ATSerialPortError as err:
            raise err
        response_list = []
        while self.__session.get_next_command():  # For each command execute it
            response = self.exec_next()
            response_list.append(response)
            # Proceed with the next command (or its doppelganger maybe...)
        # Close serial
        try:
            self.close_serial()
        except ATSerialPortError as err:
            raise err
        return response_list

    def exec(self, command: str) -> Optional[ATResponse]:
        """
        Execute in the current session a command or a ESK.
        The command has to be parsed by th eATScriptParser before being executed.
        An ATResponse is returned if was a command, otherwise None
        This method doesn't open or close the serial

        :param command
        :type command String
        :returns ATResponse or None
        :raises ATScriptSyntaxError, ATSerialPortError, ATREUninitializedError, ATRuntimeError
        """
        # Try to parse command
        try:
            parse_result = self.__script_parser.parse(command)
        except ATScriptSyntaxError as err:
            raise err
        commands = parse_result[0]
        esks = parse_result[1]
        if len(commands) > 0:
            command = commands[0]
            if not self.__session:
                raise ATREUninitializedError("Session is not initialized")
            if not self.__communicator.serial_port:
                raise ATREUninitializedError("Communicator is not initialized")
            # Clear commands in order to prevent conflicts
            self.__session.clear_commands()
            # Add command to session
            self.__session.add_command(command)
            atcmd = self.__session.get_next_command()
            # Delay
            if atcmd is None:
                return None
            if atcmd.delay:
                sleep(atcmd.delay / 1000)
            # Execute command on device
            response, execution_time = self.__communicator.exec(
                atcmd.command, atcmd.timeout
            )
            # Validate response
            response = self.__session.validate_response(response, execution_time)
            if (
                self.__session.last_command_failed
                and not atcmd.doppel_ganger
                and self.__aof
            ):
                raise ATRuntimeError(
                    "Command '%s' got a bad response: '%s' (and hasn't any doppelganger)!"
                    % (atcmd.command, response.full_response)
                )
            return response
        elif len(esks) > 0:
            # Process ESK
            esk = esks[0]
            if not self.__process_ESK(esk[0]):
                raise ATRuntimeError("ESK %s failed" % esk[0].keyword)
            return None
        else:
            return None

    def exec_next(self) -> Optional[ATResponse]:
        """
        Execute next command (It doesn't open/close the serial port)

        :returns ATResponse (None if there's no command to execute)
        :raises ATSerialPortError, ATRuntimeError
        """
        # Before executing command, check if an ESK has to be executed
        esks: List[ESKValue] = [
            i[0] for i in self.__esks if i[1] == self.__current_command
        ]
        for esk in esks:
            if not self.__process_ESK(esk) and self.__aof:
                raise ATRuntimeError(
                    "Runtime Error while processing ESK (%s %s)"
                    % (esk.keyword, esk.value)
                )
        # Then remove already executed esks esks
        self.__esks = [i for i in self.__esks if i[1] != self.__current_command]
        # Get next command
        next_command = self.__session.get_next_command()
        if not next_command:
            return None
        # Delay
        if next_command.delay:
            sleep(next_command.delay / 1000)
        # Send command to communicator
        try:
            response, execution_time = self.__communicator.exec(
                next_command.command, next_command.timeout
            )
        except ATSerialPortError as err:
            raise err
        # Validate response
        response = self.__session.validate_response(response, execution_time)
        # Check if last command failed; if it hasn't a doppelganger and abort on failure is True, then raise RuntimeError
        if (
            self.__session.last_command_failed
            and not next_command.doppel_ganger
            and self.__aof
        ):
            raise ATRuntimeError(
                "Command '%s' got a bad response: '%s' (and hasn't any doppelganger)!"
                % (next_command.command, response.full_response)
            )
        if not self.__session.last_command_failed:
            self.__current_command += 1
        return response

    def open_serial(self) -> None:
        """
        Open Serial port

        :raises ATSerialError, ATREUninitializedError
        """
        if not self.__communicator.serial_port:
            raise ATREUninitializedError("Communicator is not initialized")
        if self.__communicator.is_open():
            return
        try:
            self.__communicator.open()
        except ATSerialPortError as err:
            raise err

    def close_serial(self) -> None:
        """
        Close Serial Port

        :raises ATSerialError, ATREUninitializedError
        """
        if not self.__communicator.serial_port:
            raise ATREUninitializedError("Communicator is not initialized")
        if not self.__communicator.is_open():
            return
        try:
            self.__communicator.close()
        except ATSerialPortError as err:
            raise err

    def get_session_value(self, key: str) -> Union[str, int]:
        """
        Try to get a value from the current session storage
        If key doesn't exist, KeyError is raised

        :param key
        :type key: str
        :returns any
        :raises KeyError
        """
        try:
            return self.__session.get_session_value(key)
        except KeyError as err:
            raise err

    def __process_ESK(self, esk: ESKValue) -> bool:
        """
        Process an environment setup keyword

        :param esk
        :type esk: ESKValue
        :returns bool
        """
        if not esk:
            return False
        elif esk.keyword is ESK.DEVICE:
            # Check if serial is opened
            self.__communicator.serial_port = esk.value
            return self.__reconfigure_communicator()
        elif esk.keyword is ESK.BAUDRATE:
            self.__communicator.baud_rate = esk.value
            return self.__reconfigure_communicator()
        elif esk.keyword is ESK.DSRDTR:
            self.__communicator.dsrdtr = esk.value
            return self.__reconfigure_communicator()
        elif esk.keyword is ESK.RTSCTS:
            self.__communicator.rtscts = esk.value
            return self.__reconfigure_communicator()
        elif esk.keyword is ESK.TIMEOUT:
            self.__communicator.default_timeout = esk.value
        elif esk.keyword is ESK.BREAK:
            self.__communicator.line_break = esk.value
        elif esk.keyword is ESK.AOF:
            self.__aof = esk.value
        elif esk.keyword is ESK.SET:
            # Set a session value
            if self.__session:
                self.__session.set_session_value(esk.value[0], esk.value[1])
        elif esk.keyword is ESK.GETENV:
            # Try to get key from environment
            try:
                env_value = environ[esk.value]
                self.__session.set_session_value(esk.value, env_value)
            except KeyError:
                return False
        elif esk.keyword is ESK.PRINT:
            # Replace session values
            to_out = self.__session.replace_session_keys(esk.value)
            print(to_out)
        elif esk.keyword is ESK.EXEC:
            rc = system(esk.value)
            if rc != 0:
                return False
        elif esk.keyword is ESK.WRITE:
            file_path = esk.value[0]
            write_cnt = esk.value[1]
            return self.__write_file(file_path, write_cnt)
        else:
            return False
        return True

    def __reconfigure_communicator(self) -> bool:
        """
        Reconfigure communicator on related ESK
        """
        # Check if serial is opened
        if self.__communicator:
            if self.__communicator.is_open():
                self.__communicator.close()
        self.configure_communicator(
            self.__communicator.serial_port,
            self.__communicator.baud_rate,
            self.__communicator.default_timeout,
            self.__communicator.line_break,
            self.__communicator.rtscts,
            self.__communicator.dsrdtr,
        )
        if self.__communicator.serial_port and self.__communicator.baud_rate:
            try:
                self.__communicator.open()
                return True
            except ATSerialPortError:
                return False
        else:
            return True

    def __write_file(self, file_path: str, content: str) -> bool:
        """
        Write file from ESK.
        Content ${} variables are evaluated

        :param file
        :param content
        :type file: str
        :type content: str
        :returns bool
        """
        content = self.__session.replace_session_keys(content)
        try:
            hnd = open(file_path, "w")
            hnd.write(content)
            hnd.close()
        except IOError:
            return False
        return True
