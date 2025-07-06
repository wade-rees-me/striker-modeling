import sys


class Arguments:
    """
    Parses command-line arguments for the striker-modeling application.
    Sets flags for model, chart, and diagram generation.
    """

    def __init__(self, argv):
        # Default flags
        self.model_flag = False
        self.chart_flag = False
        self.diagram_flag = False

        # Start parsing arguments after script name
        i = 1
        while i < len(argv):
            arg = argv[i]
            if arg in ("-M", "--model"):
                self.model_flag = True
            elif arg in ("-C", "--chart"):
                self.chart_flag = True
            elif arg in ("-D", "--diagram"):
                self.diagram_flag = True
            elif arg in ("--help", "-h"):
                self.print_help_message()
                sys.exit(0)
            elif arg == "--version":
                print("striker-modeling version 1.0.0")  # Update version as needed
                sys.exit(0)
            else:
                print(f"Error: Invalid argument: {arg}")
                self.print_help_message()
                sys.exit(2)
            i += 1

    def print_help_message(self):
        """
        Prints a usage message to help the user.
        """
        print("Usage: striker-modeling [options]")
        print("Options:")
        print("  -M, --model           Build models")
        print("  -C, --chart           Build the player strategy charts")
        print("  -D, --diagram         Build the diagrams")
        print("  --help, -h            Show this help message")
        print("  --version             Display the program version")
