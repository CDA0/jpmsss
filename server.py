import cherrypy

from super_simple_stocks import GBCE, CommonStock, PreferredStock

FIXTURES = [
    { 'symbol': 'TEA', 'type': 'common', 'last_dividend': 0, 'fixed_dividend': None, 'par': 100 },
    { 'symbol': 'POP', 'type': 'common', 'last_dividend': 8, 'fixed_dividend': None, 'par': 100 },
    { 'symbol': 'ALE', 'type': 'common', 'last_dividend': 23, 'fixed_dividend': None, 'par': 60 },
    { 'symbol': 'GIN', 'type': 'preferred', 'last_dividend': 8, 'fixed_dividend': 2, 'par': 100 },
    { 'symbol': 'JOE', 'type': 'common', 'last_dividend': 13, 'fixed_dividend': None, 'par': 250 },
]

class Api(object):

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def validate_sym(self, symbol):
        return isinstance(symbol, str) and len(symbol) == 3

    def validate_trade(self, data):
        return ((set(data.keys()) & set(['quantity', 'price', 'symbol', 'action'])) and
            self.RepresentsInt(data['price']) and
            self.RepresentsInt(data['quantity']) and
            isinstance(data['symbol'], str) and len(data['symbol']) == 3 and
            data['action'].upper() in ['BUY', 'SELL'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.popargs('symbol')
    def stocks(self, symbol=None):
        """ return a stock or stocks
        :param symbol:  A stock symbol
        """

        if (symbol):
            # validate
            if not self.validate_sym(symbol):
                cherrypy.response.status = 400
                return {'status': 400, 'message': 'MalformedRequest'}

            # Get stock from storage, return 404 if not found
            stock = gbce.get_by_symbol(symbol.upper())
            if not stock:
                cherrypy.response.status = 404
                return {'status': 404, 'message': 'SymbolNotFound'}

            return stock.as_dict()

        return gbce.to_json()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def trade(self):
        data = cherrypy.request.json

        if not self.validate_trade(data):
            cherrypy.response.status = 400
            return {'status': 400, 'message': 'MalformedRequest'}

        # Get stock from storage, return 404 if not found
        stock = gbce.get_by_symbol(data['symbol'].upper())
        if not stock:
            cherrypy.response.status = 404
            return {'status': 404, 'message': 'SymbolNotFound'}

        try:
            gbce.trade(stock, data['quantity'], data['price'], data['action'])
            cherrypy.response.status = 204
        except:
            cherrypy.response.status = 400
            return {'status': 400, 'message': 'ValueError'}
        return

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def asi(self):
        return {'all_share_index': gbce.all_share_index()}


class Root(object):

    def __init__(self):
        self.api = Api()

def load_fixtures():
    # Load default stocks into store
    for item in FIXTURES:
        if item['type'] == 'common':
            s = CommonStock(item['symbol'], item['par'], item['last_dividend'])
        if item['type'] == 'preferred':
            s = PreferredStock(item['symbol'], item['par'], item['fixed_dividend'])
        gbce.add_stock(s)


gbce = GBCE()

load_fixtures()

if __name__ == '__main__':
    def cors():
        if cherrypy.request.method == 'OPTIONS':
            # preflight request
            # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
            cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
            # tell CherryPy no avoid normal handler
            return True
        else:
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
    cherrypy.quickstart(Root(), '/', config={ '/': { 'tools.cors.on': True }})
