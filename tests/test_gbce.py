import unittest
from unittest.mock import patch

from super_simple_stocks import GBCE, CommonStock, PreferredStock, Stock

class GBCEInit(unittest.TestCase):

    def test_can_create_instance_with_empty_stocks(self):
        gbce = GBCE()
        self.assertEqual(gbce.stocks, [])

class TestAddStock(unittest.TestCase):

    def test_add_stock(self):
        gbce = GBCE()
        s = CommonStock('SYM', 100, 2)
        gbce.add_stock(s)
        self.assertEqual(len(gbce.stocks), 1)

    def test_raises_value_error_on_stock_not_stock_instance(self):
        with self.assertRaises(ValueError):
            gbce = GBCE()
            gbce.add_stock('s')

class TestTrade(unittest.TestCase):

    @patch('super_simple_stocks.Stock.buy')
    def test_trade(self, mock_api_call):
        gbce = GBCE()
        s = CommonStock('SYM', 100, 2)
        gbce.add_stock(s)
        gbce.trade(s, 1, 1, 'buy')
        mock_api_call.assert_called_with(1, 1)

    def test_raises_value_error_on_stock_not_stock_instance(self):
        with self.assertRaises(ValueError):
            gbce = GBCE()
            gbce.trade('s', 1, 1, 'buy')

class TestAllShareIndex(unittest.TestCase):

    def test_all_share_index(self):
        gbce = GBCE()
        sc = CommonStock('COM', 100, 2)
        sp = PreferredStock('PRE', 99, 1)
        gbce.add_stock(sc)
        gbce.add_stock(sp)
        gbce.trade(sc, 10, 10, 'buy')
        gbce.trade(sp, 11, 11, 'sell')
        self.assertEqual(gbce.all_share_index(), 10.488088481701515)

class TestToJson(unittest.TestCase):

    def test_to_json(self):
        gbce = GBCE()
        sc = CommonStock('COM', 100, 2)
        gbce.add_stock(sc)
        print(gbce.to_json())
        self.assertEqual(gbce.to_json(), [{
            'symbol': 'COM',
            'par': 100,
            'ticker_price': 1,
            'trades': [],
            'type': 'Common',
            'last_dividend': 2,
            'dividend_yield': 2.0,
            'pe_ratio': 0.5,
            'price': None
            }]
        )
