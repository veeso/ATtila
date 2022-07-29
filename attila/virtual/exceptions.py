class VirtualSerialException(Exception):
    """
    VirtualSerialError class provides an exception in case of an error on the virtual serial port
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return str(self.message)
