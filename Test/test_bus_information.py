#!/usr/bin/env python3
# coding:utf-8
import unittest

from Main.Module import bus_information


class BusInfo(unittest.TestCase):
   def test_get_title(self):
       bus_info = bus_information.BusInfo()
       self.assertTrue(bus_info.send_info())
       self.assertRaises(bus_info.send_info())


if __name__ == '__main__':
    # unittestを実行
    unittest.main()