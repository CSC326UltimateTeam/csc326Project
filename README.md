#Welcome to CSC326!

##This is a python project that mimics google search

##The frontend handles all web requests, display, and parsing of the web interface

##The backend manages url database, page ranks, and interted indeces











#From lab1:
To run the project, first install bottle, beautifusoup, googleapiclient and bottle-beaker

for beautifulsoup:
python2.7 -m pip install bottle beautifulsoup

for googleapiclient:
pip install --upgrade google-api-python-client

for bottle-beaker:
pip install bottle-beaker

Then initialize the server with:
python srv.py

after server is successfully run, open any browser at localhost:8080 to visit site


To test the functionality of the backend, run

python2.7 test_backend.py

options can be imposed on testing, to enable verbose, test with

from test_backend import backend_test

backend_test('you-test-urls-txt', verbose=True)

review the messages to examin the test results

