import time

class Trade(object):

    """ A Trade class"""

    def __init__(self, quantity, price, action):
        """
        :param symbol: The symbol that identifies this stock
        :param quantity  Number of stocks bought or sold
        :param buysell   BuySellIndicator
        """
        if quantity < 1:
            raise ValueError('quantity must be > 0')
        if price < 1:
            raise ValueError('price must be > 0')
        if action not in ['BUY', 'SELL']:
            raise ValueError('action must be either "BUY" or "SELL"')
        self.timestamp = int(time.time())
        self.quantity = quantity
        self.price = price
        self.action = action
        self.total_price = self.quantity * self.price