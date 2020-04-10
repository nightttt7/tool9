# how to do unittest
# python -m unittest test/test1
import unittest
from pathlib import Path
import pandas as pd

from tool9 import RRP, period, es, performance, portfolio_risk, period_4_plot


class TestMonthint(unittest.TestCase):

    def setUp(self):
        self.tmp_date1 = pd.to_datetime('2011-01-05')
        self.tmp_date2 = pd.to_datetime('2012-01-04')
        self.tmp_date3 = pd.to_datetime('2012-01-05')
        self.tmp_date4 = pd.to_datetime('2012-01-06')

    def test_0(self):
        with self.assertRaises(TypeError):
            RRP.month_interval(self.tmp_date1, 1)

    def test_1(self):
        interval = RRP.month_interval(self.tmp_date1, self.tmp_date2)
        self.assertEqual(interval, 11)

    def test_2(self):
        interval = RRP.month_interval(self.tmp_date1, self.tmp_date3)
        self.assertEqual(interval, 12)

    def test_3(self):
        interval = RRP.month_interval(self.tmp_date1, self.tmp_date4)
        self.assertEqual(interval, 12)

    def tearDown(self):
        return None


class TestInput(unittest.TestCase):

    def setUp(self):
        return None

    def test_0(self):
        return None

    def tearDown(self):
        return None
