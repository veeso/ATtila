import unittest

from os.path import dirname

from attila.esk import ESK, ESKValue


class TestEsk(unittest.TestCase):
    """
    Test ATRuntime Environment commands preparation and evaluation
    NOTE: this tests doesn't test communicator!
    """

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_esks_to_string(self):
        self.assertIsNotNone(ESK.get_esk_from_string("DEVICE"))
        self.assertIsNotNone(ESK.get_esk_from_string("BAUDRATE"))
        self.assertIsNotNone(ESK.get_esk_from_string("TIMEOUT"))
        self.assertIsNotNone(ESK.get_esk_from_string("BREAK"))
        self.assertIsNotNone(ESK.get_esk_from_string("AOF"))
        self.assertIsNotNone(ESK.get_esk_from_string("SET"))
        self.assertIsNotNone(ESK.get_esk_from_string("GETENV"))
        self.assertIsNotNone(ESK.get_esk_from_string("PRINT"))
        self.assertIsNotNone(ESK.get_esk_from_string("EXEC"))
        self.assertIsNotNone(ESK.get_esk_from_string("RTSCTS"))
        self.assertIsNotNone(ESK.get_esk_from_string("DSRDTR"))
        self.assertIsNotNone(ESK.get_esk_from_string("WRITE"))
        # Try to fail
        self.assertIsNone(ESK.get_esk_from_string("FOOBAR"))

    def tests_esks_to_eskvalue(self):
        self.assertIsNotNone(ESK.to_ESKValue(ESK.DEVICE, "/dev/ttyUSB0"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.BAUDRATE, 9600))
        self.assertIsNone(ESK.to_ESKValue(ESK.BAUDRATE, "ABC"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.TIMEOUT, 5))
        self.assertIsNone(ESK.to_ESKValue(ESK.TIMEOUT, "ABC"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "CRLF"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "LF"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "CR"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.BREAK, "NONE"))
        self.assertIsNone(ESK.to_ESKValue(ESK.BREAK, "ABC"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.AOF, "True"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.AOF, "False"))
        self.assertIsNone(ESK.to_ESKValue(ESK.AOF, "ABC"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.SET, "foo=bar"))
        self.assertIsNone(ESK.to_ESKValue(ESK.SET, "ABC"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.GETENV, "CSQ"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.PRINT, "SAMPLE TEXT"))
        self.assertIsNotNone(ESK.to_ESKValue(ESK.EXEC, "echo foobar"))
        self.assertEqual(ESK.to_ESKValue(ESK.RTSCTS, "True").value, True)
        self.assertEqual(ESK.to_ESKValue(ESK.RTSCTS, "false").value, False)
        self.assertEqual(ESK.to_ESKValue(ESK.DSRDTR, "True").value, True)
        self.assertEqual(ESK.to_ESKValue(ESK.DSRDTR, "false").value, False)
        self.assertEqual(
            ESK.to_ESKValue(ESK.WRITE, '/tmp/foo.txt {"csq":${CSQ} }').value,
            ("/tmp/foo.txt", '{"csq":${CSQ} }'),
        )
        # Bad cases
        self.assertFalse(ESK.to_ESKValue(None, "FOOBAR"))
        self.assertIsNone(ESK.to_ESKValue(ESK.DEVICE, None))
        self.assertIsNone(ESK.to_ESKValue(ESK.EXEC, None))
        self.assertIsNone(ESK.to_ESKValue(6000, "foobar"))
        self.assertIsNone(ESK.to_ESKValue(ESK.AOF, None))
        self.assertIsNone(ESK.to_ESKValue(ESK.AOF, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.GETENV, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.PRINT, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.RTSCTS, None))
        self.assertIsNone(ESK.to_ESKValue(ESK.RTSCTS, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.DSRDTR, None))
        self.assertIsNone(ESK.to_ESKValue(ESK.DSRDTR, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.WRITE, None))
        self.assertIsNone(ESK.to_ESKValue(ESK.WRITE, ""))
        self.assertIsNone(ESK.to_ESKValue(ESK.WRITE, "/tmp/foo.txt"))  # No string

    def tests_setters_getters(self):
        esk = ESKValue("DEVICE", "/dev/ttyS0")
        self.assertEqual(
            esk.keyword,
            "DEVICE",
            "Keyword should be DEVICE, but is %s" % esk.keyword,
        )
        self.assertEqual(
            esk.value,
            "/dev/ttyS0",
            "Value should be /dev/ttyS0, but is %s" % esk.value,
        )
        esk.keyword = "BAUDRATE"
        esk.value = 9600
        self.assertEqual(
            esk.keyword,
            "BAUDRATE",
            "Keyword should be BAUDRATEss, but is %s" % esk.keyword,
        )
        self.assertEqual(esk.value, 9600, "Value should be 9600, but is %d" % esk.value)


if __name__ == "__main__":
    unittest.main()
