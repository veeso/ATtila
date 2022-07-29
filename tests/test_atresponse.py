import unittest

from attila.atresponse import ATResponse
from attila.atcommand import ATCommand


class TestATResponse(unittest.TestCase):
    """
    Test ATResponse instance, setters and getters
    """

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_at_commands(self):
        cmd = ATCommand("AT+CSQ", "OK", 5, 1000, ["AT+CSQ=?{rssi},"])
        resp = ATResponse("OK", ["+CSQ: 32,2", "", "OK"], cmd, 632)
        # Test response
        self.assertEqual(
            resp.response,
            "OK",
            "Expected response 'OK', got %s" % resp.response,
        )
        self.assertEqual(
            len(resp.full_response),
            3,
            "Expected full response length: 3, got %d" % len(resp.full_response),
        )
        self.assertEqual(
            resp.execution_time,
            632,
            "Expected execution time 632, got %d" % resp.execution_time,
        )
        # Add collectable
        resp.add_collectable("rssi", 32)
        self.assertEqual(
            resp.get_collectable("rssi"),
            32,
            "Expected rssi value 32, got %s" % resp.get_collectable("rssi"),
        )
        # Setters / Getters
        resp.response = "OK"
        self.assertEqual(
            resp.response,
            "OK",
            "Response should be OK but is %s" % resp.response,
        )
        resp.full_response = ["+CSQ: 99,99", "", "OK"]
        self.assertEqual(
            resp.full_response[0],
            "+CSQ: 99,99",
            "First element in full response should be +CSQ: 99,99, but is %s"
            % resp.full_response[0],
        )
        self.assertEqual(
            len(resp.full_response),
            3,
            "Length of full response should be 3 but is %d" % len(resp.full_response),
        )
        self.assertEqual(
            resp.command,
            cmd,
            "Associated command is not the command previously set",
        )
        resp.execution_time = 5000
        self.assertEqual(
            resp.execution_time,
            5000,
            "Execution time should be 5000, but is %d" % resp.execution_time,
        )
        # Test bad cases
        resp.execution_time = -1
        self.assertEqual(
            resp.execution_time,
            0,
            "Execution time should be 0, but is %d" % resp.execution_time,
        )


if __name__ == "__main__":
    unittest.main()
