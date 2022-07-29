class ATSerialPortError(Exception):
    """
    ATSerialPortError class provides an exception in case of an error on the serial port
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)


class ATScriptNotFound(Exception):
    """
    ATScriptNotFound class provides an exception in case of an at script not found
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)


class ATScriptSyntaxError(Exception):
    """
    ATScriptSyntaxError class provides an exception in case of a syntax error in an ATScript
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)


class ATREUninitializedError(Exception):
    """
    ATREUninitializedError class provides an exception in case of uninitialized ATRE
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)


class ATRuntimeError(Exception):
    """
    ATRuntimeError class provides an exception in case of a Runtime Error
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)
