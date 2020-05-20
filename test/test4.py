#!/usr/bin/env python3

import unittest
from helper import cheat_output
#from textreplacer import TextReplacer

# Test locally
import sys
sys.path.append('../textreplacer/')
from textreplacer import TextReplacer


class TestMarkCase4(unittest.TestCase):

    def setUp(self):
        patterns = [
            r"long\d+$",
        ]
        self.tr = TextReplacer("test4.txt", "UTF-8", patterns)
        self.str_lst = self.tr.mark()

        replace_lst = [
            "short1",
            "short2",
            "",
            "short4",
            "",
            "short6",
            "",
            "",
            ""
        ]

        def r(source_line, new_line, state_for_replace, source_line_number, log_file):
            if new_line == "":
                replace_log_line = "(nil)"
            else:
                replace_log_line = new_line

            log_line = "[{}]: {} | {}".format(source_line_number, source_line, replace_log_line)
            log_file.write(log_line + "\n")

            return (new_line, None)

        replace_checking_fnc = r

        # Aim: Test skip_blank_line flag
        self.tr.replace_and_output(replace_lst, replace_checking_fnc, "output/", skip_blank_line=True)

    def test_case4_01_marked_content(self):
        self.assertEqual(self.str_lst[0], "long1")
        self.assertEqual(self.str_lst[1], "long2")
        self.assertEqual(self.str_lst[2], "long3")
        self.assertEqual(self.str_lst[3], "long4")
        self.assertEqual(self.str_lst[4], "long5")
        self.assertEqual(self.str_lst[5], "long6")
        self.assertEqual(self.str_lst[6], "long7")
        self.assertEqual(self.str_lst[7], "long8")
        self.assertEqual(self.str_lst[8], "something before long9")

    def test_case4_02_replace_content(self):
        with open("output/test4.txt", 'r') as dest_file:
            output_lines = dest_file.readlines()

            self.assertEqual(output_lines[0], "Simple replace test - replace longX with shortX, will delete some long lines" + "\n")
            self.assertEqual(output_lines[1], "This tests feature of skip_blank_line" + "\n")
            self.assertEqual(output_lines[2], "" + "\n")
            self.assertEqual(output_lines[3], "Start1" + "\n")
            self.assertEqual(output_lines[4], "short1" + "\n")
            self.assertEqual(output_lines[5], "short2" + "\n")
            self.assertEqual(output_lines[6], "kekw" + "\n")
            self.assertEqual(output_lines[7], "End1" + "\n")
            self.assertEqual(output_lines[8], "" + "\n")
            self.assertEqual(output_lines[9], "Start2" + "\n")
            self.assertEqual(output_lines[10], "short4" + "\n")
            self.assertEqual(output_lines[11], "kekw" + "\n")
            self.assertEqual(output_lines[12], "" + "\n")
            self.assertEqual(output_lines[13], "short6" + "\n")
            self.assertEqual(output_lines[14], "kekw" + "\n")
            self.assertEqual(output_lines[15], "" + "\n")
            self.assertEqual(output_lines[16], "kekw" + "\n")
            self.assertEqual(output_lines[17], "End2" + "\n")


if __name__ == '__main__':
    unittest.main()
