#!/usr/bin/env python3

import unittest
from helper import cheat_output
#from textreplacer import TextReplacer

# Test locally
import sys
sys.path.append('../textreplacer/')
from textreplacer import TextReplacer


class TestMarkCase2(unittest.TestCase):

    def setUp(self):
        patterns = [
            r"^\d+$",
            r"^<.*>$",
            r"^\[YEP"
        ]
        self.tr = TextReplacer("test2.txt", "UTF-8", patterns)
        self.str_lst = self.tr.mark()

    def test_case2_01_marked_content(self):
        self.assertEqual(self.str_lst[0], "1")
        self.assertEqual(self.str_lst[1], "2")
        self.assertEqual(self.str_lst[2], "[YEP thaths good - hey]")
        self.assertEqual(self.str_lst[3], "<likehtml>")
        self.assertEqual(self.str_lst[4], "100")
        self.assertEqual(self.str_lst[5], "<<<<<<ok too>>>>>>")
        self.assertEqual(self.str_lst[6], "[YEP this counts too")


if __name__ == '__main__':
    unittest.main()
