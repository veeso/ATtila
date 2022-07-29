import unittest
from attila.atcommunicator import ATCommunicator, ATSerialPortError


class TestATCommunicator(unittest.TestCase):
    """
    Test ATCommunicator instance, setters and getters
    """

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_communicator(self):
        # Test setters / getters
        com = ATCommunicator("/dev/ttyS0", 9600, 10, "\r\n", True, True)
        self.assertEqual(com.serial_port, "/dev/ttyS0")
        self.assertEqual(com.baud_rate, 9600)
        self.assertEqual(com.default_timeout, 10)
        self.assertEqual(com.line_break, "\r\n")
        self.assertEqual(com.rtscts, True)
        self.assertEqual(com.dsrdtr, True)
        com.serial_port = "/dev/ttyfoobar"
        self.assertEqual(com.serial_port, "/dev/ttyfoobar")
        com.baud_rate = 115200
        self.assertEqual(com.baud_rate, 115200)
        com.default_timeout = 15
        self.assertEqual(com.default_timeout, 15)
        com.default_timeout = -5
        self.assertEqual(com.default_timeout, 10)
        com.default_timeout = None
        self.assertEqual(com.default_timeout, 10)
        com.line_break = "\r"
        self.assertEqual(com.line_break, "\r")
        com.rtscts = False
        self.assertEqual(com.rtscts, False)
        com.dsrdtr = False
        self.assertEqual(com.dsrdtr, False)
        with self.assertRaises(ATSerialPortError):
            com.open()
        com.serial_port = None
        with self.assertRaises(ATSerialPortError):
            com.open()
        with self.assertRaises(ATSerialPortError):
            com.close()
        self.assertFalse(com.is_open())
        with self.assertRaises(ATSerialPortError):
            com.exec("AT")


if __name__ == "__main__":
    unittest.main()
