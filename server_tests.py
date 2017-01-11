import json
import cherrypy
from cherrypy.test import helper
from server import Root, load_fixtures, gbce

headers = [
    ('Content-Type', 'application/json')
]

class ServerTests(helper.CPWebCase):

    def setup_server():
        load_fixtures()
        cherrypy.tree.mount(Root())
    setup_server = staticmethod(setup_server)

    # /api/stocks
    def test_api_stocks_returns_all_stocks(self):
        self.getPage('/api/stocks')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')
        self.assertBody(json.dumps(gbce.to_json()))

    def test_api_stocks_returns_requested_stock(self):
        self.getPage('/api/stocks/gin')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')
        self.assertBody(json.dumps(gbce.get_by_symbol('GIN').__dict__))

    def test_api_stocks_returns_400_on_symbol_length_too_long(self):
        self.getPage('/api/stocks/GINN', headers=headers)
        self.assertStatus('400 Bad Request')
        self.assertHeader('Content-Type', 'application/json')
        self.assertBody(b'{"status": 400, "message": "MalformedRequest"}')

    def test_api_stocks_returns_400_on_symbol_length_too_short(self):
        self.getPage('/api/stocks/GI', headers=headers)
        self.assertStatus('400 Bad Request')
        self.assertHeader('Content-Type', 'application/json')
        self.assertBody(b'{"status": 400, "message": "MalformedRequest"}')

    def test_api_stocks_returns_404_on_symbol_not_found(self):
        self.getPage('/api/stocks/GIT', headers=headers)
        self.assertStatus('404 Not Found')
        self.assertHeader('Content-Type', 'application/json')
        self.assertBody(b'{"status": 404, "message": "SymbolNotFound"}')


