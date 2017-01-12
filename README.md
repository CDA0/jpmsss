# Super Simple Stocks

## Server Setup

This project was built with python3 and cherrypy.

[CherryPy](http://cherrypy.org) is a self contained webserver allowing simple setup.
For the purpose of this excerise it is suitable and is being run for a development setting.
```
python3 -m venv cda0
cd cda0
. ./bin/activate
git clone https://github.com/CDA0/jpmsss.git
cd jpmsss
pip install -r requirements.txt
```

You can then run the cherrypy server by:

`python server.py`

The server will be running on port 9090.

## Client setup

The client was built with [Ember](http://emberjs.com).

To build and test the client application Node.js is required.
I reccommend using nvm to install the latest stable version of node, though I wont cover this here.

From the jpmsss directory:
```
cd client
npm install
./node_modules/.bin/bower install
./node_modules/.bin/ember server
```

This will start a development server serving the client application.

Open a browser and head to [http://localhost:4200](http://localhost:4200).

## Testing

Some light testing has been added, and while by no means bulletproof covers most key areas.

From the jspmsss directory:
```
python -m unittest -v
```

Some simple integration tests can be run:
```
py.test -s tests/server_test.py -v
```

client tests are run in the client directory:
```
./node_modules/.bin/ember test
```