from enum import Enum
from typing import Optional, Any


class ESK(Enum):
    """
    This class represents an Environment Setup Keyword
    """

    DEVICE = 0
    BAUDRATE = 1
    TIMEOUT = 2
    BREAK = 3
    AOF = 4
    SET = 5
    GETENV = 6
    PRINT = 7
    EXEC = 8
    DSRDTR = 9
    RTSCTS = 10
    WRITE = 11

    @staticmethod
    def get_esk_from_string(esk_string: str) -> Optional[object]:
        """
        Get ESK enum value from its string representation

        :param esk_string
        :type esk_string: String
        :returns ESK or None if invalid
        """
        if esk_string == "DEVICE":
            return ESK.DEVICE
        elif esk_string == "BAUDRATE":
            return ESK.BAUDRATE
        elif esk_string == "TIMEOUT":
            return ESK.TIMEOUT
        elif esk_string == "BREAK":
            return ESK.BREAK
        elif esk_string == "AOF":
            return ESK.AOF
        elif esk_string == "SET":
            return ESK.SET
        elif esk_string == "GETENV":
            return ESK.GETENV
        elif esk_string == "PRINT":
            return ESK.PRINT
        elif esk_string == "EXEC":
            return ESK.EXEC
        elif esk_string == "DSRDTR":
            return ESK.DSRDTR
        elif esk_string == "RTSCTS":
            return ESK.RTSCTS
        elif esk_string == "WRITE":
            return ESK.WRITE
        else:
            return None

    @staticmethod
    def to_ESKValue(esk: Any, attr: str) -> Optional[object]:
        """
        Check if attributes for this esk have a valid syntax

        :param esk
        :param attr
        :type esk: ESK
        :type attr: String
        :returns ESKValue (None in case of errors)
        """
        if not esk:
            return None
        elif esk is ESK.DEVICE:
            if attr:
                return ESKValue(esk, attr)
            else:
                return None
        elif esk is ESK.BAUDRATE:
            try:
                baud = int(attr)
                return ESKValue(esk, baud)
            except ValueError:  # NaN
                return None
        elif esk is ESK.TIMEOUT:
            try:
                timeout = int(attr)
                return ESKValue(esk, timeout)
            except ValueError:  # NaN
                return None
        elif esk is ESK.BREAK:
            if attr == "LF":
                return ESKValue(esk, "\n")
            elif attr == "CRLF":
                return ESKValue(esk, "\r\n")
            elif attr == "CR":
                return ESKValue(esk, "\r")
            elif attr == "NONE":
                return ESKValue(esk, None)
            else:
                return None
        elif esk is ESK.AOF:
            if not attr:
                return None
            check = attr.lower()
            if check == "true":
                return ESKValue(esk, True)
            elif check == "false":
                return ESKValue(esk, False)
            else:
                return None
        elif esk is ESK.SET:
            key_val = attr.split("=")
            if len(key_val) == 2:
                # Tuple of key and value
                return ESKValue(esk, (key_val[0], key_val[1]))
            else:
                return None
        elif esk is ESK.GETENV:
            if attr:
                return ESKValue(esk, attr)
            else:
                return None
        elif esk is ESK.PRINT:
            if attr:
                return ESKValue(esk, attr)
            else:
                return None
        elif esk is ESK.EXEC:
            if attr:
                return ESKValue(esk, attr)
            else:
                return None
        elif esk is ESK.DSRDTR:
            if not attr:
                return None
            check = attr.lower()
            if check == "true":
                return ESKValue(esk, True)
            elif check == "false":
                return ESKValue(esk, False)
        elif esk is ESK.RTSCTS:
            if not attr:
                return None
            check = attr.lower()
            if check == "true":
                return ESKValue(esk, True)
            elif check == "false":
                return ESKValue(esk, False)
        elif esk is ESK.WRITE:
            if not attr:
                return None
            write_attr = attr.split(" ")
            if len(write_attr) < 2:
                return None
            # Tuple of file and file content
            file_path = write_attr[0]
            file_content = " ".join(write_attr[1:])
            return ESKValue(esk, (file_path, file_content))
        else:
            return None


class ESKValue(object):
    """
    This class represents an Environment Setup Keyword value
    """

    def __init__(self, keyword: ESK, value: Any):
        """
        Class constructor. Instantiates a new :class:`.ESKValue.` object with the provided paramters

        :param keyword: keyword type
        :param value associated
        :type keyword: ESK
        :type value: Any
        """
        self._keyword = keyword
        self._value = value

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, kw: ESK):
        self._keyword = kw

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: Any):
        self._value = val
