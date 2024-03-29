""" Primary application entrypoint
"""

import sys
import os

from src.flintai.exceptions import FlintaiError
from src.flintai.cli import parse_command
from src.flintai.commands import create_command

def main(args=None):

    if args is None:
        args = sys.argv[1:]

#      insert autocompeletion

    try:
        cmd_name, cmd_args = parse_command(args)
    except FlintaiError as exc:
        sys.stderr.write("ERROR: {}".format(exc))
        sys.stderr.write(os.linesep)
        sys.exit(1)

    command = create_command(cmd_name)

    return command.main(cmd_args)