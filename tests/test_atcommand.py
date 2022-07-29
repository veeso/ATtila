import unittest

from attila.atcommand import ATCommand, ATResponse


class TestATCommands(unittest.TestCase):
    """
    Test ATcommands instance, setters and getters
    """

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_at_commands(self):
        cmd = ATCommand("AT+CSQ", "OK", 5, 1000, ["AT+CSQ=?{dbm},"], None)
        self.assertEqual(
            cmd.command,
            "AT+CSQ",
            "Expected command AT+CSQ, got %s" % cmd.command,
        )
        self.assertEqual(
            cmd.expected_response,
            "OK",
            "Expected response OK, got %s" % cmd.expected_response,
        )
        self.assertEqual(cmd.timeout, 5, "Expected timeout 5, got %d" % cmd.timeout)
        self.assertEqual(cmd.delay, 1000, "Expected delay 1000, got %d" % cmd.delay)
        self.assertEqual(
            len(cmd.collectables),
            1,
            "Expected collectables length 1, got %d" % len(cmd.collectables),
        )
        self.assertEqual(
            cmd.collectables[0],
            "AT+CSQ=?{dbm},",
            "Expected collectable 'AT+CSQ=?{dbm},', got %s" % cmd.collectables[0],
        )
        # Constructor bad case
        cmd2 = ATCommand("AT+CSQ", "OK", 5, 1000, "AT+CSQ=?{dbm},", None)
        self.assertIsNone(
            cmd2.collectables,
            "Collectables should be None, since a string has been provided",
        )
        cmd3 = ATCommand(
            "AT+CSQ", "OK", 5, 1000, "AT+CSQ=?{dbm},", ATCommand("AT+CSQ?")
        )
        self.assertIsNone(
            cmd3.collectables,
            "Collectables should be None, since a string has been provided",
        )
        self.assertIsNotNone(cmd3.doppel_ganger)
        cmd4 = ATCommand("AT+CSQ", "OK", 5, 1000, "AT+CSQ=?{dbm},", "foobar")
        self.assertIsNone(
            cmd4.doppel_ganger,
            "Doppelganger should be None, since a string has been provided",
        )
        # Test setters getters
        cmd = ATCommand("AT")
        # Command
        cmd.command = "ATE0"
        self.assertEqual(
            cmd.command,
            "ATE0",
            "Expected ATE0 as command, got %s" % cmd.command,
        )
        # Expected response
        cmd.expected_response = "OK"
        self.assertEqual(
            cmd.expected_response,
            "OK",
            "Expected OK as expected response, got %s" % cmd.expected_response,
        )
        # Timeout
        cmd.timeout = 10
        self.assertEqual(
            cmd.timeout, 10, "Expected 10 as timeout, got %d" % cmd.timeout
        )
        cmd.timeout = 0  # Test bad case
        self.assertEqual(cmd.timeout, 1, "Expected 1 as timeout, got %d" % cmd.timeout)
        # Delay
        cmd.delay = 5000
        self.assertEqual(cmd.delay, 5000, "Expected 5000 as delay, got %d" % cmd.delay)
        cmd.delay = -1  # Test bad case
        self.assertEqual(cmd.delay, 0, "Expected 0 as delay, got %d" % cmd.delay)
        # Collectables
        cmd.collectables = [
            "AT+CSQ=?{rssi::[0-9]{1,2}},",
            "AT+CSQ=${rssi},?{ber::[0-9]{1,2}}",
        ]
        self.assertEqual(
            len(cmd.collectables),
            len(
                [
                    "AT+CSQ=?{rssi::[0-9]{1,2}},",
                    "AT+CSQ=${rssi},?{ber::[0-9]{1,2}}",
                ]
            ),
            "Bad collectables",
        )
        # Doppelganger
        cmd.doppel_ganger = cmd3
        self.assertEqual(cmd.doppel_ganger, cmd3)
        bad_doppelganger = "foobar"
        cmd.doppel_ganger = bad_doppelganger
        self.assertIsNone(
            cmd.doppel_ganger,
            "Doppelganger should be None, since a string has been provided, but it's not",
        )
        # Response
        response_ok = ATResponse("OK", ["+CSQ=32,99", "", "OK"], cmd, 5000)
        cmd.response = response_ok
        self.assertEqual(
            cmd.response,
            response_ok,
            "Response should be an ATResponse instance",
        )


if __name__ == "__main__":
    unittest.main()
