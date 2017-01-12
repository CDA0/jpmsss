from super_simple_stocks import Stock

class GBCE(object):

    """ The Global Beveridge Corp. Exchange """

    def __init__(self):
        self.stocks = []

    def get_by_symbol(self, symbol):
        """
        :param symbol:  The symbol of the stock
        :return The Stock class
        """
        return next((stock for stock in self.stocks if stock.symbol == symbol), None)

    def add_stock(self, stock):
        """
        :param stock:  A Stock class
        """
        if isinstance(stock, Stock):
            self.stocks.append(stock)
        else:
            raise ValueError()

    def trade(self, stock, quantity, price, action):
        """
        :param stock:  A Stock class
        :param quantity: quantity of stocks
        :param price: price per share
        :param action:  buy or sell
        """
        if isinstance(stock, Stock):
            func = getattr(stock, action.lower())
            func(quantity, price)
        else:
            raise ValueError()

    def all_share_index(self):
        """
        :return: The all share index
        """
        stock_prices = [stock.price() for stock in self.stocks]
        product = 1
        for sp in stock_prices:
            product *= sp if sp is not None else 1
        return product**(1/len(self.stocks))

    def to_json(self):
        """
        :return all stocks as JSON
        """
        return [stock.as_dict() for stock in self.stocks]