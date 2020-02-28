
from src.flintai.cli.base_command import Command
from src.flintai.cli.status_codes import SUCCESS
from src.flintai.exceptions import CommandError


class HelpCommand(Command):
    """
    Show help for commands
    """

    usage: """
    """

    def run(self, options, args):
        from src.flintai.commands import(
            commands_dict, create_command,
        ) #also get_similar_commands

        try:
            #'flintai help' with no args is handled by flintai.__init__.parseopt() ?
            cmd_name = args[0]
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            #guess = get_similar_commands(cmd_name)

            msg = ['unkown command "{}"'.format(cmd_name)]
            #if guess:
                #msg.append('maybe you meant "{}"'.format(guess)
            raise CommandError(' - '.join(msg))

        command = create_command(cmd_name)
        command.parser.print_help()

        return SUCCESS