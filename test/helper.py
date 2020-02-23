#!/usr/bin/env python3

def cheat_output(out_list, var_name):
    for idx, line in enumerate(out_list):
        print(r'self.assertEqual({}[{}], "{}" + "\n")'.format(var_name, idx, line.rstrip("\r\n")))
