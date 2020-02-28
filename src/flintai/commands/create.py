from src.flintai.cli.base_command import Command
import numpy as np
import datetime
import classes.Neuron_Network as nn
import classes.Grid as g


class CreateCommand(Command):
    """
    Create a new world to run simulations on.
    """

    usage = """flintai create [options] ..."""

    def __init__(self, *args, **kwargs):
        super(CreateCommand, self).__init__(*args, **kwargs)

        cmd_opts = self.cmd_opts

        cmd_opts.add_option(
            '--width',
            action='store',
            dest='item_width',
            help="Set the width of the world. "
                 "Currently in matrix width. ",
        )

        cmd_opts.add_option(
            '--height',
            action='store',
            dest='item_height',
            help="Set the height of the world. "
                 "Currently in matrix height. ",
        )

        cmd_opts.add_option(
            '--name',
            action='store',
            dest='item_name',
            help="Set the name for your new net.",
        )

        cmd_opts.add_option(
            '--path',
            action='store',
            dest='file_path',
            default='..'
        )

        print("Int Create")

    def run(self, options, args):
        print("Running create. Your string is {}".format(args))

        if args[0].lower() == "net":
            # ----------------------------
            # ----Configuration------------------
            # --------------------------
            test = nn.Neuron_Network()

            best = 15

            self.height = 3 if int(options.item_height) is None else int(options.item_height)
            self.width = 3 if int(options.item_width) is None else int(options.item_width)
            self.name = int(options.item_name)

            grid_options = 2  # goal, flint, (empty is granted)

            inputs = grid_x * grid_y * grid_options
            outputs = 4  # up, down, left, right
            iterations = 1000000
            second_iterations = 2000
            file_name = "self.name"

            np.save(self.name, a)

            neurons = test.complex_light_setup(inputs,outputs,3,inputs*3)
            #neurons = test.load(file_name)
            #neurons = test.load("best.txt")



            a = np.arange(self.width * self.height).reshape(self.width, self.height)


            print(a)
        elif args[0].lower() == "net":

            self.height = 3 if int(options.item_height) is None else int(options.item_height)
            self.width = 3 if int(options.item_width) is None else int(options.item_width)

            default_grid_name = " ".join(self.height, "x", self.width, "grid")
            self.name = default_grid_name if int(options.item_name) is None else int(options.item_width)

            grid = g.Grid(self.height, self.width)

        else:
            print("{} is not an option for create".format(args[0]))
