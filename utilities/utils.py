import subprocess
import os
import shutil


def execute_command(command, cwd=None):
    if cwd is None:
        cwd = os.path.dirname(os.path.realpath(__file__))
    do_cmd = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
        )
    return do_cmd.communicate()


class Utilities:

    def __init__(self, log_instance, book_dir):
        self.log_instance = log_instance
        self.book_dir = book_dir
        self.base_dir = book_dir

    def set_new_working_dir(self, new_base_dir):
        self.base_dir = new_base_dir

    def read_file(self, target_file_path):
        """Return a file as a list of lower case strings"""
        complete_target_file_path = os.path.join(self.base_dir,
                                                 target_file_path)
        with open(complete_target_file_path,
                  "r", encoding="utf-8", errors="replace") as f:
            return f.readlines()

    def write_file(self, target_file_path, data):
        """Write list of strings to file"""
        complete_target_file_path = os.path.join(self.base_dir,
                                                 target_file_path)
        with open(complete_target_file_path,
                  "w", encoding="utf-8") as f:
            for line in data:
                f.write(line)
            self.log_instance.logit(f"{complete_target_file_path} written")
        return complete_target_file_path

    def cmd(self, command, cwd=None):
        """Execute system command"""
        _out, _err = execute_command(command, cwd)
        if _err:
            self.log_instance.logitw(_err.decode("utf-8").strip())
            pass

    def uncase(string_list):
        """Return lower case version of a list of strings"""
        uncased_string = []
        for string in string_list:
            uncased_string.append(string.lower())
        return uncased_string

    def imgcopy(self, dirname):
        """Duplicate any image files in the pdf directory"""
        target_dir = os.path.join(self.base_dir, dirname)
        for f in os.listdir(target_dir):
            ftype = os.path.splitext(f)[1]
            if ftype == ".svg":
                self.log_instance.logit("SVG image found, probable pandoc failure")
            if ftype in [".svg", ".jpg", ".jpeg", ".png", ".gif"]:
                shutil.copy(os.path.join(target_dir, f),
                            os.path.join(self.book_dir, "pdf", f))


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
