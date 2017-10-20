# Welcome to CSC326!

### This is a python project that mimics google search
### The frontend handles all web requests, display, and parsing of the web interface
### The backend manages url database, page ranks, and interted indeces


## From lab2:
### Google authetication API is used in this lab

### To access the server or website:
The public IP Address of the live webserver is: **34.233.27.14**, the website server is running on port 80 (with IP 0.0.0.0)
you could also use DNS **http://ec2-34-233-27-14.compute-1.amazonaws.com/** to access the website


### To browse the website

There are two mods for the website:

For Anonymous Mode:
  1)Sign-In: Users can sign in by first clicking the sign-in button and selecting "Log In with Google" in the pop up window. Users in anonymous mode are not able to modify profile photo.
  2)Only word count table will be displayed after clicking the search button

For Signed-In Mode:
  
  1)Account:
  User Information will be displayed in the pop window triggered by clicking the username button on top-right
   
  a.Sign-Out: Users can sign out by first clicking username and selecting "Sign Out" in the pop up window.
  
  b.Profile Photo Modification: Users can modify his/her own profile photo by clicking the profile photo area in the account       pop up window.
  
  2)Search history count of the current user and Most recent searches of the current user will be displayed in the search         result page.

### Benchmarking

It is advised that you use two different machines to do the benchmarking. 

#### SSH in to the instance
First ssh in to the amazon instance with the permission, if you are the TA and do not have the permission, email nix.li@mail.utoronto.ca

Then make sure you have sysstat and dstat by typing

`sudo apt-get install sysstat dstat`

run your server in a different screen

`screen
cd /csc326/csc326Project/
sudo python srv.py &`

Use Control-A and Control-D to detach this screen, and you should be back in the previsou commandline

Type `dstat -c -m -d -n` to start monitoring system information

#### On test bench machine

you could follow the sample benchmarking code in the RESULT file, or refer to https://httpd.apache.org/docs/2.4/programs/ab.html

Test the server acpacity with your own options


## From lab1:
To run the project, first install bottle, beautifusoup, googleapiclient and bottle-beaker

for beautifulsoup:
`python2.7 -m pip install bottle beautifulsoup`

for googleapiclient:
`pip install --upgrade google-api-python-client`

for bottle-beaker:
`pip install bottle-beaker`

Then initialize the server with:
`sudo python srv.py`

after server is successfully run, open any browser at localhost:8080 to visit site


To test the functionality of the backend, run

`python2.7 test_backend.py`

options can be imposed on testing, to enable verbose, test with

`from test_backend import backend_test`

`backend_test('you-test-urls-txt', verbose=True)`

`review the messages to examin the test results`

