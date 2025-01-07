import sys

#
class Arguments:
    def __init__(self, argv):
        self.model_flag = False
        self.chart_flag = False
        self.diagram_flag = False

        i = 1  # Start from the first argument after the program name
        while i < len(argv):
            if argv[i] in ("-M", "--model"):
                self.model_flag = True
            elif argv[i] in ("-C", "--chart"):
                self.chart_flag = True
            elif argv[i] in ("-D", "--diagram"):
                self.diagram_flag = True
            else:
                print(f"Error: Invalid argument: {argv[i]}")
                sys.exit(2)
            i += 1  # Move to the next argument

    def print_help_message(self):
        print("Usage: strikerPython [options]")
        print("Options:")
        print("  --help                                   Show this help message")
        print("  --version                                Display the program version")
        print("  -M, --model                              Build models")
        print("  -C, --chart                              Build the player strategy charts")
        print("  -D, --diagram                            Build the diagrams")

