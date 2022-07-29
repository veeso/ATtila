from typing import List, Union, Any


class ATResponse(object):
    """
    This class represents an AT command response and provide access to the expected
    response format, the entire response and the command execution time (milliseconds)
    """

    def __init__(
        self,
        resp: str,
        fullresponse: List[str],
        command: Any,
        executiontime: int = 0,
    ):
        """
        Class constructor. Instantiates a new :class:`.ATResponse.` object with the provided parameters.

        :param resp: main response from command (format/content as expected by the user)
        :param fullresponse: entire response received from command execution
        :param command: command associated to response
        :param executiontime: execution time of the command in milliseconds
        :type resp: string
        :type fullresponse: list of string
        :type command: ATCommand
        :type executiontime: int
        """
        self._response = resp
        self._full_response = fullresponse
        self._execution_time = executiontime
        self._command = command
        self._collectables = {}

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: str):
        self._response = response

    @property
    def full_response(self):
        return self._full_response

    @full_response.setter
    def full_response(self, full_response: List[str]):
        self._full_response = full_response

    @property
    def command(self):
        return self._command

    @property
    def execution_time(self):
        return self._execution_time

    @execution_time.setter
    def execution_time(self, executiontime: int):
        if executiontime > 0:
            self._execution_time = executiontime
        else:
            self._execution_time = 0

    def add_collectable(self, key: str, value: Union[str, int]) -> None:
        """
        Add a collectable to the response collectables

        :param key: key of the collectable
        :param value: value of the collectable
        :type key: string
        :type value: any
        :returns None
        """

        self._collectables[key] = value
        return

    def get_collectable(self, key: str) -> Union[str, int]:
        """
        Returns the value associated to the collectable

        :param key: key of the collectable
        :type key: string
        :returns Union[str, int]
        """
        return self._collectables.get(key)
