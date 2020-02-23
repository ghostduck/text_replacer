#!/usr/bin/env python3

import unittest
from helper import cheat_output
#from textreplacer import TextReplacer

# Test locally
import sys
sys.path.append('../textreplacer/')
from textreplacer import TextReplacer


# Example of using stateful function to loop + mark lines
def s(ln, state):
    # initial setup
    set_to_in_selection = None
    mark_current_line = False

    # Handle state from previous line first
    if state is None:  # First line
        state = {
            "mark_next_line" : False,
            "in_selection" : False
        }

    else:
        mark_current_line = bool(state["mark_next_line"])

        # cleanup, in case we forget to do so
        state["mark_next_line"] = False

    # Logic for checking current line
    # Set mark_current_line to True to mark current line
    # Set state["mark_next_line"] to True mark next line


    if ln == "Mark next":
        state["mark_next_line"] = True

    elif ln == "Mark me and next":
        mark_current_line = True
        state["mark_next_line"] = True

    elif ln == "Start":
        mark_current_line = True  # Comment out this line so "Start" won't be marked
        set_to_in_selection = True

    elif ln == "Stop":
        state["in_selection"] = False

    mark_current_line = mark_current_line or state["in_selection"]

    if set_to_in_selection:
        state["in_selection"] = True

    return (mark_current_line, state)


class TestMarkCase3(unittest.TestCase):

    def setUp(self):
        patterns = [
            r"^\d+$"
        ]

        special_rule = s

        self.tr = TextReplacer("test3.txt", "UTF-8", patterns, special_rule)
        self.str_lst = self.tr.mark()


    def test_case3_01_marked_content(self):
        self.assertEqual(self.str_lst[0], "99")
        self.assertEqual(self.str_lst[1], "100")
        self.assertEqual(self.str_lst[2], "nice")
        self.assertEqual(self.str_lst[3], "Mark me and next")
        self.assertEqual(self.str_lst[4], "gj")
        self.assertEqual(self.str_lst[5], "hohoho")
        self.assertEqual(self.str_lst[6], "Start")
        self.assertEqual(self.str_lst[7], "")
        self.assertEqual(self.str_lst[8], "300")
        self.assertEqual(self.str_lst[9], "Above 300 should not crash")
        self.assertEqual(self.str_lst[10], "")
        self.assertEqual(self.str_lst[11], "Blank line before")
        self.assertEqual(self.str_lst[12], "I am marked too")
        self.assertEqual(self.str_lst[13], "")
        self.assertEqual(self.str_lst[14], "101")

        # --- harder cases ---
        self.assertEqual(self.str_lst[15], "Mark next")  # second one
        self.assertEqual(self.str_lst[16], "This line should be marked and the last 'Mark next' above")

        self.assertEqual(self.str_lst[17], "Mark me and next")
        self.assertEqual(self.str_lst[18], "Mark me and next")
        self.assertEqual(self.str_lst[19], "This line and 2 lines above should be marked")

        self.assertEqual(self.str_lst[20], "Start")
        self.assertEqual(self.str_lst[21], "ok")
        self.assertEqual(self.str_lst[22], "Mark next")
        self.assertEqual(self.str_lst[23], "Stop")

        self.assertEqual(self.str_lst[24], "102")

        # Note that we have "Mark next" as last line
        # But it is not doing anything. And it should not crash
        self.assertEqual(len(self.str_lst), 25)


if __name__ == '__main__':
    unittest.main()
