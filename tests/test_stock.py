import unittest

from super_simple_stocks import Stock

class TestInit(unittest.TestCase):

    def test_not_instantiable(self):

        with self.assertRaises(TypeError):
            stock = Stock('TEA', 100)