from .exceptions import ATSerialPortError

from serial import Serial, SerialException, SerialTimeoutException
import re
from time import time
from time import sleep
from typing import List, Optional, Tuple


class ATCommunicator(object):
    """
    ATCommunicator class provides an interface to communicate with an
    RF module using AT commands through a serial port
    """

    def __init__(
        self,
        serial_port: str,
        baud_rate: int,
        default_timeout: int = 10,
        line_break: str = "\r\n",
        rtscts: Optional[bool] = True,
        dsrdtr: Optional[bool] = True,
    ):
        """
        Class constructor. Instantiates a new :class:`.ATCommunicator.` object with the provided parameters.

        :param serial_port: serial port to use in order to communicate with the RF module
        :param baud_rate: baud rate to set
        :param default_timeout (optional): the default timeout for command response read in seconds; it will be used if a timeout is not provided when executing a command         :param line_break (optional): specify line break to use when sending command; most of RF modules use CRLF
        :param line_break: line break to send with commands
        :param rtscts: use rtscts
        :param dsrdtr: use dsrdtr
        :type serial_port: string
        :type baud_rate: int
        :type default_timeout: int > 0
        :type line_break: string
        :type rtscts: bool
        :type dsrdtr: bool
        """
        self._device: Optional[Serial] = None
        self._serial_port: str = serial_port
        self._baud_rate: int = baud_rate
        self.default_timeout: Optional[int] = default_timeout
        self._line_break: str = line_break
        self._rtscts: Optional[bool] = rtscts
        self._dsrdtr: Optional[bool] = dsrdtr

    @property
    def serial_port(self):
        return self._serial_port

    @serial_port.setter
    def serial_port(self, serial_port: str):
        self._serial_port = serial_port

    @property
    def baud_rate(self):
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, baud_rate: int):
        self._baud_rate = baud_rate

    @property
    def default_timeout(self):
        return self._default_timeout

    @default_timeout.setter
    def default_timeout(self, timeout: int):
        if timeout:
            if timeout > 0:
                self._default_timeout = timeout
            else:
                self._default_timeout = 10
        else:
            self._default_timeout = 10

    @property
    def line_break(self):
        return self._line_break

    @line_break.setter
    def line_break(self, brk: str):
        self._line_break = brk

    @property
    def rtscts(self):
        return self._rtscts

    @rtscts.setter
    def rtscts(self, opt: bool):
        self._rtscts = opt

    @property
    def dsrdtr(self):
        return self._dsrdtr

    @dsrdtr.setter
    def dsrdtr(self, opt: bool):
        self._dsrdtr = opt

    def open(self) -> None:
        """
        Open serial port

        :raises ATSerialPortError
        """
        if not self._serial_port:
            raise ATSerialPortError("Serial port is not set")
        if self._device:
            self.close()
        try:
            self._device = Serial(
                self._serial_port,
                self._baud_rate,
                timeout=0.1,
                write_timeout=self._default_timeout,
                rtscts=self._rtscts,
                dsrdtr=self._dsrdtr,
            )
        except (OSError, SerialException) as error:
            raise ATSerialPortError(str(error))
        except Exception as error:  # Catch other exceptions too
            raise ATSerialPortError(str(error))
        # Flush port
        self.__flush()

    def close(self) -> None:
        """
        Close serial port

        :raises ATSerialPortError
        """
        if not self._device:
            raise ATSerialPortError("Serial port device is closed")
        try:
            self._device.close()
        except (OSError, SerialException) as error:
            raise ATSerialPortError(error)
        self._device = None

    def is_open(self) -> bool:
        """
        Returns whether the serial port is open

        :returns bool
        """
        return self._device is not None

    def exec(self, command: str, timeout: int = None) -> Tuple[List[str], int]:
        """
        Execute AT command

        :param command: command to execute
        :param timeout: timeout for command, if not set default will be used
        :type command: str
        :type timeout: int
        :returns tuple of (list of string, execution time ms); list: command response without line break; empty lines are ignored
        :raises ATSerialPortError
        """
        if not self._device:
            raise ATSerialPortError("Serial port device is closed")
        # Flush before write
        self.__flush()
        if not timeout:
            timeout = self.default_timeout
            self._device.write_timeout = self.default_timeout
        else:  # Set write timeout to timeout
            self._device.write_timeout = timeout
        # Get start time
        t_start = int(time() * 1000)
        try:
            if self._line_break:
                self._device.write(
                    b"%s%s"
                    % (
                        command.encode("utf-8"),
                        self._line_break.encode("utf-8"),
                    )
                )
            else:
                self._device.write(b"%s" % command.encode("utf-8"))
        except SerialTimeoutException as err:
            raise ATSerialPortError(str(err))
        data = bytearray()
        # Set timeout to t_start + timeout seconds
        t_timeout = t_start + (timeout * 1000)
        t_now = t_start
        data_still_available = True
        sleep_time_based_on_baud = 100 / self.baud_rate  # Milliseconds

        # Try to read until there are data available and t_now < t_timeout
        while t_now < t_timeout and data_still_available:
            t_now = int(time() * 1000)
            # Read available bytes
            read_bytes = self._device.read(self._device.in_waiting)
            if not read_bytes:
                continue
            # Mini sleep to wait for incoming data
            t_waiting_elapsed = 0
            mini_sleep_time = 0.001
            # Wait until in waiting is 0 and waiting elapsed millis is < of sleep time based on baud
            while (
                self._device.in_waiting == 0
                and sleep_time_based_on_baud > t_waiting_elapsed
            ):
                sleep(mini_sleep_time)  # 1ms
                t_waiting_elapsed += mini_sleep_time
            # Check if there are still data available
            if self._device.in_waiting > 0:
                data_still_available = True
            else:
                data_still_available = False
            data += read_bytes
            # End of read

        data = data.decode("utf-8")
        lines: List[str] = data.splitlines()
        t_end = int(time() * 1000)
        for i in range(len(lines)):
            # Remove newline
            if re.search("(\\r|)\\n$", lines[i]):
                lines[i] = re.sub("(\\r|)\\n$", "", lines[i])
        # Flush input buffer
        self._device.reset_input_buffer()
        return (lines, t_end - t_start)

    def __flush(self) -> None:
        """
        Flush serial port
        """
        if self._device:
            self._device.reset_input_buffer()
