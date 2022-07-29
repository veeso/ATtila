from .atcommand import ATCommand
from .atresponse import ATResponse

import re
from typing import List, Dict, Optional, Union, Tuple


class ATSession(object):
    """
    This class represents an AT sessions, which is a set of commands to execute - "a script".
    It takes care of preparing the next command to execute based on the response of the previous one
    and of validating the response of the last command.
    """

    def __init__(self, commands: Optional[List[ATCommand]]):
        """
        Class constructor. Instantiates a new :class:`.ATSession.` object with the provided parameters.

        :param commands: list of ATCommand which will become the set of instructions for this session.
        :type commands: list
        """
        if commands is None:
            commands = []
        self._commands: List[ATCommand] = commands
        self._session_storage: Dict[str, Union[str, int]] = {}
        self._current_command_index = 0
        self._last_command_failed = False

    @property
    def last_command_failed(self):
        return self._last_command_failed

    def reset(self):
        """
        Reset the AT session. It clears the command list and the session values
        """
        self._session_storage = {}
        self.clear_commands()
        self.reset_execution()

    def clear_commands(self):
        """
        Removes all commands from AT session an restores command index to 0
        """
        self._commands = []
        self.reset_execution()

    def reset_execution(self):
        """
        Reset only execution parameters (last command failed and command index)
        """
        self._current_command_index = 0
        self._last_command_failed = False

    def add_command(self, command: ATCommand) -> bool:
        """
        Add a command at the end of the command list

        :param command: command to add
        :type command: ATCommand
        :returns boolean
        """
        self._commands.append(command)
        return True

    def add_new_command(
        self,
        command: str,
        exp_response: str,
        tout: int = None,
        delay: int = 0,
        collectables: Optional[List[str]] = None,
        dganger: Optional[ATCommand] = None,
    ) -> bool:
        """
        Add a new command at the end of the command list

        :param command: command to add
        :param exp_response: expected response from command execution. a literal or a generic response can be provided
        :param tout (optional): command execution timeout in seconds.
        :param delay (optional): delay in milliseconds before command execution
        :param collectables (optional): values to store from response. Follow collectables syntax as specified in ATtila documentation
        :param dganger (optional): doppelganger command associated to this command (command to execute in case of this command fails)
        :type command: string
        :type ATResponse: string
        :type exp_respose: string
        :type tout: int
        :type delay: int
        :type collectables: list of string
        :type dganger: ATCommand
        :returns boolean
        """
        if not command:
            return False
        new_command = ATCommand(
            command, exp_response, tout, delay, collectables, dganger
        )
        self._commands.append(new_command)
        return True

    def rem_command(self, index: int) -> bool:
        """
        Remove a command from the session command list

        :param index: index of the command to remove
        :type index: int
        :returns boolean
        """
        if index >= len(self._commands):
            return False
        self._commands.remove(self._commands[index])
        return True

    def get_next_command(self) -> Optional[ATCommand]:
        """
        Get the next command in the AT session to execute

        :returns ATCommand (or None)
        """
        # Prepare command
        try:
            next_command = self._commands[self._current_command_index]
        except IndexError:
            return None
        self.prepare(next_command)
        # Return command
        return next_command

    def get_command(self, index: int) -> Optional[ATCommand]:
        """
        Get the command with the provided index

        :param index: index of the command to get
        :type index: int
        :returns ATCommand (or None)
        """
        if index >= len(self._commands):
            return None
        return self._commands[index]

    def validate_response(self, response: List[str], execution_time: int) -> ATResponse:
        """
        Validate a response of a command. The response is associated to the current command.
        Based on the response and the command associated to it,
        the ATResponse will have collectables based on expected response,
        also the next command, in case of a wrong response will be the doppelganger (if set)
        :param response
        :param execution_time
        :type response: list of string
        :type execution_time: int
        :returns ATResponse
        """
        # Get current command expected response
        current_command = self._commands[self._current_command_index]
        # Increment current command
        self._current_command_index += 1
        # Prepare variables for looking for response
        expected_response = current_command.expected_response
        vars_to_collect = current_command.collectables
        # Variables for response object
        response_str = None
        # If expected response is set, look for it
        if expected_response:
            # Search for response
            for line in response:
                # Search for expected response in line
                regresult = re.search(expected_response, line)
                if regresult:
                    response_str = regresult.group()
                    self._last_command_failed = False
                    break
            # If response hasn't been found => last command failed
            if not response_str:
                self._last_command_failed = True
        # Instance ATResponse
        atresponse = ATResponse(response_str, response, current_command, execution_time)
        # If last command failed => set doppelganger as next command
        if self._last_command_failed:
            # @! Response NOK
            doppelganger = current_command.doppel_ganger
            if doppelganger:
                # Add command to command list
                self._commands.insert(self._current_command_index, doppelganger)
        else:
            # @! Response OK
            # Try to get collectables
            if vars_to_collect:
                for to_collect in vars_to_collect:  # String
                    collected = self.__get_value_from_response(
                        to_collect, response
                    )  # collected => tuple(key, value)
                    if collected is not None:
                        self._session_storage[collected[0]] = collected[1]
                        atresponse.add_collectable(collected[0], collected[1])
        # Instance response object
        current_command.response = atresponse
        return atresponse

    def replace_session_keys(self, haystack: str) -> str:
        """
        Replace all the session keys with session values
        :param haystack: string where keys have to be replaced with their values
        :type haystack: string
        :returns string
        """
        # Get session variable
        while True:
            reg_result = re.search("\\${(.*?)}", haystack)
            if reg_result is None:
                break
            key_group = reg_result.group(0)
            key_name = key_group[2:-1]
            # @! Okay, there is a session variable to replace
            # Search for session variable
            session_value = self._session_storage.get(key_name)
            if session_value is None:
                # If not found set to empty
                session_value = ""
            # Replace session variable
            haystack = haystack.replace(key_group, str(session_value))
        return haystack

    def prepare(self, command: ATCommand) -> None:
        """
        Prepare command to execute, replacing session variable with values in session;
        if value is not in session, it will be replaced with an empty string

        :param command
        :type command: ATCommand
        """

        command_str = command.command
        # Get session variable
        command_str = self.replace_session_keys(command_str)
        # @!All sessions variables have been replaced
        # Other stuff???
        # Reassign command to ATCommand
        command.command = command_str
        return

    def set_session_value(self, key: str, value: Union[str, int]) -> None:
        """
        Set a new key to session storage

        :param key
        :param value
        :type key: String
        :type value: Union[str, int]
        """
        self._session_storage[key] = value

    def get_session_value(self, key: str) -> Union[str, int]:
        """
        Try to get a value from the current session storage
        If key doesn't exist, KeyError is raised

        :param key
        :type key: String
        :returns Union[str, int]
        :raises KeyError
        """
        try:
            return self._session_storage[key]
        except KeyError:
            raise KeyError("Could not find %s in current session storage" % key)

    def __get_value_from_response(
        self, to_collect: str, response: List[str]
    ) -> Optional[Tuple[str, Union[str, int]]]:
        """
        Get a value from response.
        The collectable syntax is '...?{KEY_NAME}...'
        The ?{} part is replaced by (.*) in a regex

        :param to_collect: collectable syntax to match
        :param response: list of string gained in the response
        :type to_collect: string
        :type response: list of string
        :returns tuple(string, string/int); None if not found
        """
        # Replace session keys in response first
        reg_result = re.search("\\?{(.*)}", to_collect)
        if reg_result:
            key_group = reg_result.group()
        else:
            return None
        # Remove ?{} from key group and split by regex specifier
        key_parts = key_group[2:-1].split("::")
        key_regex = None
        if len(key_parts) > 1:
            key_regex = key_parts[1]
        key_name = key_parts[0]
        # part_to_remove = to_collect.replace(key_group, "")
        key_value = None
        # compose regex with to_collect[0] + (.*) + to_collect[1]
        regex = to_collect.replace(key_group, "")
        # Escape regex
        if to_collect == key_group:
            collect_expr_parts = []
        else:
            collect_expr_parts = to_collect.split(key_group)
        # Collect regex part to build regex; excape parts
        part_to_remove: List[str] = []
        if len(collect_expr_parts) > 0:
            for i in range(len(collect_expr_parts)):
                if not collect_expr_parts[i]:  # Skip empty tokens
                    continue
                collect_expr_parts[i] = self.replace_session_keys(collect_expr_parts[i])
                # First collect this part in parts to remove
                part_to_remove.append(collect_expr_parts[i])
                # Then escape regex
                collect_expr_parts[i] = re.escape(collect_expr_parts[i])
            # Eventually compose regex
            collect_expr_parts.insert(1, "(.*)")
            regex = ""
            for expr_part in collect_expr_parts:
                regex += expr_part
        else:  # If there are no collect parts, just get everything
            regex = "(.*)"
        # Iterate over lines
        for line in response:
            search = re.search(regex, line)
            if search is not None:
                # If a key regex is set, check if line complies
                if key_regex:
                    key_regex_match = re.search(key_regex, line)
                    if key_regex_match:
                        key_value = key_regex_match.group()
                    else:
                        # Line doesn't comply
                        continue
                key_value = search.group()
                for part in part_to_remove:
                    key_value = key_value.replace(part, "")
                try:
                    key_value = int(key_value)
                except ValueError:
                    break
                break
        # Return values
        if key_value is not None:
            return (key_name, key_value)
        else:
            return None
