from typing import List, Optional, Any

from .atresponse import ATResponse


class ATCommand(object):
    """
    This class represents an AT command
    """

    def __init__(
        self,
        cmd: str,
        exp_response: Optional[str] = None,
        tout: Optional[int] = None,
        delay: Optional[int] = 0,
        collectables: Optional[List[str]] = None,
        dganger: Optional[Any] = None,
    ):
        """
        Class constructor. Instantiates a new :class:`.ATCommand.` object with the provided parameters.

        :param cmd: command to execute
        :param exp_response: expected response from command execution. a literal or a generic response can be provided
        :param tout (optional): command timeout execution in seconds.
        :param delay (optional): delay in milliseconds before command execution
        :param collectables (optional): values to store from response. Follow collectables syntax as specified in ATtila documentation
        :param dganger (optional): doppelganger command associated to this command (command to execute in case of this command fails)
        :type cmd: string
        :type exp_respose: string
        :type tout: int
        :type delay: int
        :type collectables: list of string
        :type dganger: ATCommand
        """
        self._command: str = cmd
        self._expected_response = exp_response
        self._timeout = tout
        self._delay = delay
        if type(collectables) != list:
            self._collectables: Optional[List[str]] = None
        else:
            self._collectables: List[str] = collectables
        if isinstance(dganger, ATCommand):
            self._doppel_ganger = dganger
        else:
            self._doppel_ganger = None
        self._response = None

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, cmd: str):
        self._command = cmd

    @property
    def expected_response(self):
        return self._expected_response

    @expected_response.setter
    def expected_response(self, exp_response: str):
        self._expected_response = exp_response

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: ATResponse):
        self._response = response

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, tout: int):
        if tout > 1:
            self._timeout = tout
        else:
            self._timeout = 1

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay: int):
        if delay > 0:
            self._delay = delay
        else:
            self._delay = 0

    @property
    def collectables(self):
        return self._collectables

    @collectables.setter
    def collectables(self, collectables: Optional[List[str]]):
        self._collectables = collectables

    @property
    def doppel_ganger(self):
        return self._doppel_ganger

    @doppel_ganger.setter
    def doppel_ganger(self, dganger: Any):
        if isinstance(dganger, ATCommand):
            self._doppel_ganger = dganger
        else:
            self._doppel_ganger = None
