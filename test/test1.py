#!/usr/bin/env python3

import unittest
from helper import cheat_output
#from textreplacer import TextReplacer

# Test locally
import sys
sys.path.append('../textreplacer/')
from textreplacer import TextReplacer


class TestMarkCase1(unittest.TestCase):

    def setUp(self):
        self.tr = TextReplacer("test1.txt", "UTF-8", [r"^\d+$"])
        self.str_lst = self.tr.mark()

        # Setup up for replace - NO newline append to these in this list!
        replace_lst = [
            "REPLACED-0-A",
            "RB",
            "RC",
            "RD",
            "RE",
            "RF",
            "RG",
            "RH",
            "RI",
            "RJ",
            "RK",
            "RL"
        ]

        # Very simple case of replace - directly using lines in another list
        def r(source_line, new_line, state_for_replace, source_line_number, log_file):
            # logging is optional in this test case, still showing how to write log
            # Example of using log_file
            log_line = "[{}]: {} | {}".format(source_line_number, source_line, new_line)
            log_file.write(log_line + "\n")

            return (new_line, None)

        replace_checking_fnc = r

        self.tr.replace_and_output(replace_lst, replace_checking_fnc, "output/")


    def test_case1_01_marked_content(self):
        self.assertEqual(self.str_lst[0],"0")
        self.assertEqual(self.str_lst[1],"1")
        self.assertEqual(self.str_lst[2],"2")
        self.assertEqual(self.str_lst[3],"3")
        self.assertEqual(self.str_lst[4],"4")
        self.assertEqual(self.str_lst[5],"5")
        self.assertEqual(self.str_lst[6],"6")
        self.assertEqual(self.str_lst[7],"7")
        self.assertEqual(self.str_lst[8],"8")
        self.assertEqual(self.str_lst[9],"9")
        self.assertEqual(self.str_lst[10],"10")
        self.assertEqual(self.str_lst[11],"11")


    def test_case1_02_replace_content(self):
        with open("output/test1.txt", 'r') as dest_file:
            output_lines = dest_file.readlines()

            # Not sure if this is a good testing practice or not...
            # cheat_output(output_lines, "output_lines")

            # Anyone can teach me better way than this?
            # Note that in actual replaced file, each line ends with newline
            self.assertEqual(output_lines[0], "Test simple line matching (only line with digits only)" + "\n")
            self.assertEqual(output_lines[1], "REPLACED-0-A" + "\n")
            self.assertEqual(output_lines[2], "RB" + "\n")
            self.assertEqual(output_lines[3], "RC" + "\n")
            self.assertEqual(output_lines[4], "RD" + "\n")
            self.assertEqual(output_lines[5], "RE" + "\n")
            self.assertEqual(output_lines[6], "don't replace me" + "\n")
            self.assertEqual(output_lines[7], "Some blank lines following, they should be preserved." + "\n")
            self.assertEqual(output_lines[8], "" + "\n")
            self.assertEqual(output_lines[9], "" + "\n")
            self.assertEqual(output_lines[10], "" + "\n")
            self.assertEqual(output_lines[11], "RF" + "\n")
            self.assertEqual(output_lines[12], "RG" + "\n")
            self.assertEqual(output_lines[13], "RH" + "\n")
            self.assertEqual(output_lines[14], "" + "\n")
            self.assertEqual(output_lines[15], "The mark function for this test (file) should only mark pure number line" + "\n")
            self.assertEqual(output_lines[16], "Just stop at 11" + "\n")
            self.assertEqual(output_lines[17], "" + "\n")
            self.assertEqual(output_lines[18], "RI" + "\n")
            self.assertEqual(output_lines[19], "" + "\n")
            self.assertEqual(output_lines[20], "RJ" + "\n")
            self.assertEqual(output_lines[21], "RK" + "\n")
            self.assertEqual(output_lines[22], "" + "\n")
            self.assertEqual(output_lines[23], "RL" + "\n")
            self.assertEqual(output_lines[24], "   3 spaces before the character 3" + "\n")
            self.assertEqual(output_lines[25], "" + "\n")
            self.assertEqual(output_lines[26], "-- OK. Stop here 12 --" + "\n")


if __name__ == '__main__':
    unittest.main()
