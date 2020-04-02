#!/usr/bin/env python3

import logging
import re
import os


DEFAULT_OUTPUT_LOG_ENCODING = "UTF8"
DEFAULT_OUTPUT_LOG_DIRECTORY_NAME = "log"
DEFAULT_OUTPUT_FILE_ENCODING = "UTF8"
DEFAULT_OUTPUT_NEWLINE = "\n"


class TextReplacer():
    r"""

    Mark and replace text in a text file.

    Normal logic:
        Loop through whole file, copy "matching" lines to a list in order. (marking)
        Then we can replace the marked lines.

    Note that marked_lines should NOT be changed at all. It belongs to the original source file + patterns/special rule pair.

    In other words, let mark() set it up and never manually change it.

    ---------------

    Purpose in high level:
        Marking:
        - mark multiple patterns (simple regex match), return as a list of strings
        - allow to use special rule (provided by user) on marking too

        Replace and output:
        - Read a list with same length, then replace, and output updated content
        - Needs to provide a function (replace_checking_fnc) to replace

    ---------------

    Attributes:
        # Note that they should NOT be modified manually

        marked_lines - list of marked lines (without \n)
        normal_pattern - list of strings for regex
        special_rule - custom stateless function to mark lines

    Methods:
        mark - mark lines
        replace_and_output - as its name

    """

    def __init__(self, path, encoding, pattern, special_rule=lambda ln, state: (False, None), log_dirname=DEFAULT_OUTPUT_LOG_DIRECTORY_NAME):
        self.path = path
        self.encoding = encoding
        # log directory: log files will be generated in /pathto/output/${log_dirname}/
        self.output_log_dirname = log_dirname

        # Normal pattern: mark whole line as long as any of the patterns match
        # Expect list of strings (patterns to create regex)
        self.normal_pattern = pattern

        # only one special rule (method)
        # This method consume one line, return True to mark the line as match
        # special_rule(ln, state)
        self.special_rule = special_rule

        self.__marked = False
        self.marked_lines = None
        self.marked_lines_info = None  # just put source line number for now

        self.__create_regex()

    def mark(self):
        self.marked_lines = []
        self.marked_lines_info = []

        state = None

        with open(self.path, encoding=self.encoding) as file:
            for line_number, ln in enumerate(file, start=1):
                ln = ln.rstrip("\r\n")

                # Every line will be passed to special_rule()
                # special_rule is like a stateless loop function
                # updated state needs to be returned for the next call
                # if state is None, it means it is the first iteration (or not using state at all)
                match_special_rule, state = self.special_rule(ln, state)

                # Current design does not allow unmark marked lines.
                # This can be changed but will break many codes in use (compatability issue)

                if any(r.match(ln) for r in self.__matched_patterns) or match_special_rule:
                    # Each ln should end with newline. I don't think I want it in list of strings
                    # I would rather add a "\n" myself when I need to use the list
                    self.marked_lines.append(ln)
                    self.marked_lines_info.append(line_number)

        self.__marked = True
        return self.marked_lines

    # Most kwargs are for file arguments, others are for special options
    def replace_and_output(self, replace_lst, replace_checking_fnc, output_dir, **kwargs):
        # --- Sanity check ---
        if not self.__marked:
            raise ValueError("Lines not marked yet")

        if len(replace_lst) != len(self.marked_lines):
            raise ValueError("Numbers of line to replace not the same as marked lines")

        # --- Setup ---
        self.__output_dir_setup(output_dir)

        pairs = iter(zip(self.marked_lines, replace_lst))

        state_for_readline = None
        state_for_replace = None

        original_script_base = os.path.basename(self.path)

        # --- Setup for the output file ---
        # Flags
        # Use default option if nothing is provided
        # Same as normal file arguments
        encoding = kwargs.get("encoding") or DEFAULT_OUTPUT_FILE_ENCODING
        output_newline = kwargs.get("newline") or DEFAULT_OUTPUT_NEWLINE

        # Customized flags
        output_log_file_encoding = kwargs.get("output_log_file_encoding") or DEFAULT_OUTPUT_LOG_ENCODING

        # if True, blank line in replace_lst will not output anything to output file (not even \n)
        # Default option is False
        skip_blank_line = bool(kwargs.get("skip_blank_line"))  # User should specify to skip, None -> False (Won't skip)

        # Paths
        output_log_path = output_dir + "/" + self.output_log_dirname + "/" + original_script_base + ".log"
        output_file_path = output_dir + "/" + original_script_base

        # --- read source file and start replacing marked lines
        with open(self.path, encoding=self.encoding) as source_file, \
                open(output_log_path, 'w', encoding=output_log_file_encoding) as log_file, \
                open(output_file_path, 'w', encoding=encoding, newline=output_newline) as dest_file:

            for source_line_number, ln in enumerate(source_file, start=1):

                # Same loop logic as mark()
                match_special_rule, state_for_readline = self.special_rule(ln, state_for_readline)

                if any(r.match(ln) for r in self.__matched_patterns) or match_special_rule:
                    source_line, new_line = next(pairs)
                    # replace_checking_fnc needs to return the actual line for output
                    # Also, it should do the logging as well

                    # output_line does not need to append newline
                    output_line, state_for_replace = replace_checking_fnc(source_line, new_line, state_for_replace, source_line_number, log_file)

                    if output_line or not skip_blank_line:
                        # WARNING: INTENDED - Will crash if output_line is None. Why would you pass None anyway?
                        dest_file.write(output_line + "\n")
                else:
                    # unmarked lines (original lines) ends with newline
                    dest_file.write(ln)

    def __output_dir_setup(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(output_dir + "/" + self.output_log_dirname, exist_ok=True)

    def __create_regex(self):
        self.__matched_patterns = [re.compile(r) for r in self.normal_pattern]
