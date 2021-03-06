from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import input

import sys
import importlib
import inspect

from datmo.core.util.i18n import get as __
from datmo.core.util.exceptions import ArgumentException


class Helper():
    def __init__(self):
        pass

    def echo(self, message):
        print(message)

    def prompt(self, msg, default=None):
        try:
            if default:
                msg = msg + "[" + str(default) + "]"
            msg = msg + ": "
            return input(msg)
        except EOFError:
            pass

    def prompt_bool(self, msg):
        val = input(msg).lower()
        return val in [
            'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh'
        ]

    def prompt_validator(self,
                         msg,
                         validate_function,
                         tries=5,
                         error_message="Invalid input"):
        if not callable(validate_function):
            raise ArgumentException(
                'validate_function argument must be function')
        val = input(msg).lower()
        if not validate_function(val) and tries >= 0:
            tries -= 1
            return self.prompt_validator(msg, validate_function, tries,
                                         error_message)
        if tries == 0:
            self.echo(error_message)
        return val

    def get_command_class(self, command_name):
        command_path = "datmo.cli.command." + command_name

        try:
            command_class = importlib.import_module(command_path)
        except ImportError as ex:
            self.echo(__("error", "cli.general", ex.message))
            sys.exit()

        all_members = inspect.getmembers(command_class)

        # find class module based on first param passed into command line
        for member in all_members:
            if command_path in member[1].__module__:
                command_class = member
                break

        # command_class[1] == concrete class constructor
        return command_class[1]

    def get_command_choices(self):
        return ["init", "snapshot", "task"]
