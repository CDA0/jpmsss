import unittest

from super_simple_stocks import Trade

class TestInit(unittest.TestCase):

    def test_raises_value_error_on_qty_lt_1(self):
        with self.assertRaises(ValueError):
            Trade(0, 5, 'BUY')

    def test_raises_value_error_on_price_lt_1(self):
        with self.assertRaises(ValueError):
            Trade(5, 0, 'BUY')

    def test_raises_value_error_on_action_not_buy_sell(self):
        with self.assertRaises(ValueError):
            Trade(5, 5, 'TEST')

class TestTotalPrice(unittest.TestCase):

    def test_total_price(self):

        trade = Trade(5, 5, 'BUY')
        self.assertEqual(trade.total_price, 25)