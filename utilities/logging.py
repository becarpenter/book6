# Logging utilities
import os
import sys


class Logging:

    def __init__(self, log_path, printing=False, gui_instance=None):
        self.log_path = log_path
        self.printing = printing
        self.warnings = 0
        self.gui_instance = gui_instance
        # Deleting old log if present
        if os.path.isfile(log_path):
            os.remove(log_path)

    def logit(self, msg):
        """Add a message to the log file"""
        with open(self.log_path, "a",  encoding="utf-8") as f:
            f.write(msg + "\n")
        if self.printing:
            print(msg)
            if self.gui_instance is not None:
                self.gui_instance.print_info(msg)

    def logitw(self, msg):
        """Add a warning message to the log file"""
        self.logit("WARNING: " + msg)
        self.warnings += 1

    def dprint(self, *msg):
        """Diagnostic print"""
        if self.printing:
            print(*msg)

    def crash(self, msg):
        """Log and crash"""
        self.printing = True
        self.logit("CRASH " + msg)
        sys.exit(1)


