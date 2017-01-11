from abc import ABC, abstractmethod

DEFAULT_TICKER_PRICE = 1
DEFAULT_TIME_PERIOD = 60 * 15

class Stock(ABC):
    """ A Base Stock class

    """

    def __init__(self, symbol, par):
        """
        :param symbol: The symbol that identifies this stock
        :param par: The par value for this stock
        """
        self.symbol = symbol
        self.par = par
        self.ticker_price = DEFAULT_TICKER_PRICE
        self.trades = []

    @property
    @abstractmethod
    def dividend(self):
        """
        :return the calculated dividend
        """
        pass

    @property
    def dividend_yield(self):
        return self.dividend / self.ticker_price

    @property
    def pe_ratio(self):
        """
        :return: The P/E ratio for this stock
        """
        if self.dividend != 0:
            return self.ticker_price / self.dividend
        else:
            return None

    def buy(self, quantity, price):
        """
        :param symbol: The symbol that identifies this stock
        :param quantity  Number of stocks bought

        :note: updating ticker price here
        """
        self.trades.append(Trade(quantity, price, 'BUY'))
        self.ticker_price = price

    def sell(self, quantity, price):
        """
        :param symbol: The symbol that identifies this stock
        :param quantity  Number of stocks sold

        :note: updating ticker price here
        """
        self.trades.append(Trade(quantity, price, 'SELL'))
        self.ticker_price = price

    def price(self):
        """  Get the stock price from historical trades
        """
        trades = [t for t in self.trades if t.timestamp >= int(time.time()) - DEFAULT_TIME_PERIOD]

        if len(trades) > 0:
            return sum(t.total_price for t in trades) / sum(t.quantity for t in trades)
        else:
            return None

    def as_dict(self):
        """
        :return: Stock as dict
        """
        d = self.__dict__.copy()
        d['dividend_yield'] =  self.dividend_yield
        d['pe_ratio'] = self.pe_ratio
        d['trades'] = list([trade.__dict__ for trade in self.trades])
        d['price'] = self.price()
        return d


class CommonStock(Stock):
    """ A Common Stock class

    """

    def __init__(self, symbol, par, last_dividend):
        """
        :param symbol: The symbol that identifies this stock
        :param par: The par value for this stock
        """
        super().__init__(symbol, par)
        self.last_dividend = last_dividend

    @property
    def dividend(self):
        return self.last_dividend


class PreferredStock(Stock):
    """ A Preferred Stock class

    """

    def __init__(self, symbol, par, fixed_dividend):
        """
        :param symbol: The symbol that identifies this stock
        :param par: The par value for this stock
        """
        super().__init__(symbol, par)
        self.fixed_dividend = fixed_dividend

    @property
    def dividend(self):
        return self.fixed_dividend