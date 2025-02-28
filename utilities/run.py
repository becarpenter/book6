import os
import time
import sys

import utils
from bakeBook import bake_book_process


def pandoc_checks(log_instance):
    _out, _err = utils.execute_command("pandoc --version")
    if _err:
        # Pandoc not installed, we won't be able to do much...
        log_instance.crash("pandoc is not installed!")


def bake_book(book_dir, debug=True, gui_instance=None):
    script_location = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(script_location, "bakeBook.log")

    log_instance = utils.Logging(log_path,
                                 printing=debug,
                                 gui_instance=gui_instance)
    pandoc_checks(log_instance)

    utility_instance = utils.Utilities(log_instance, book_dir)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z", time.localtime())
    log_instance.logit("bakeBook run at " + timestamp)
    log_instance.logit("Book directory " + book_dir)

    bake_book_process(book_dir, log_instance, utility_instance)


if __name__ == "__main__":
    # Command line mode
    if len(sys.argv) <= 1:
        print("Please provide a path for the book dir or use run_gui.py")
    else:
        # user provided directory name?
        if os.path.isdir(sys.argv[1]):
            # assume user has provided directory
            # and set all options to defaults
            bake_book(sys.argv[1])
        else:
            print("Error : "
                "provided path is either inaccessible or innexistant")
