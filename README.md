Welcome to CSC326!

This is a python project that mimics google search

The frontend handles all web requests, display, and parsing of the web interface

The backend manages url database, page ranks, and interted indeces


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



The public IP Address of the live webserver is: http://ec2-34-233-27-14.compute-1.amazonaws.com/

There are two mods for the website:
For Anonymous Mode:
1)Sign-In: Users can sign in by first clicking the sign-in button and selecting "Log In with Google" in the pop up window. Users in anonymous mode are not able to modify profile photo.
2)Only word count table will be displayed after clicking the search button

For Signed-In Mode:
1)Account:
User Information will be displayed in the pop window triggered by clicking the username button on top-right
a.Sign-Out: Users can sign out by first clicking username and selecting "Sign Out" in the pop up window.
b.Profile Photo Modification: Users can modify his/her own profile photo by clicking the profile photo area in the account pop up window.
2)Search history count of the current user and Most recent searches of the current user will be displayed in the search result page.
