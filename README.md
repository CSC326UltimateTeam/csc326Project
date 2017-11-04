# Welcome to CSC326!

### This is a python project that mimics google search
### The frontend handles all web requests, display, and parsing of the web interface
### The backend manages url database, page ranks, and interted indeces

## From lab3:

### Running the backend test program "run_backend_test.py"
In command line, run with `python run_backend_test.py [verbose(0 or1)] [depth]`

for example running `python run_backend_test.py 1 1` will test the crawler using the urls in urls.txt, at maximum depth 1, and the program will print all the database insertion messages.

It is advised to use depth level < 2 for testing, otherwise the crawler may take up too much time to traverse all the websites

You could add your test urls in urls.txt.

Many rank scores will be 0 since they are at the deepest depth, hence the program will prompt to you whether to still display them, type yes or no in commandline.


### If you want to use it in a script
`from run_backend_test import backend_test`

`test=backend_test("your-db-file", 'your-urls.txt', verbose=your_choice, depth=your_choice2)`

`test.test_all()`

### AWS setup will be uploaded to google docs once it is made available

### Please refer to the RESULT.docx for details of the benchmarking

### Attempt to multithread is done and is not yet complete

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

`ssh -i permission.pem ubuntu@34.233.27.14`

Then make sure you have sysstat and dstat by typing

`sudo apt-get install sysstat dstat`

run your server in a different screen

`screen`

`cd /csc326/csc326Project/`

`sudo python srv.py >output.txt 2>&1 &`

Use Control-A and Control-D to detach this screen, and you should be back in the previsou commandline

Type `dstat -c -m -d -n` to start monitoring system information

#### On test bench machine
get apache ab
`sudo apt-get apache-utils2`

you could follow the sample benchmarking code in the RESULT file, or refer to https://httpd.apache.org/docs/2.4/programs/ab.html

Test the server acpacity with your own options

Basically you just need to know the url or ip of the server location, and test it with apache benchmarking tool

example:
`ab -n 1000 -c 30  -r -S http://ec2-34-233-27-14.compute-1.amazonaws.com/?keywords=foo+bar+csc326`
This command sends 1000 get requests, and each time 30 request is sent simultaneously to the website under anonymous mode, searching for "foo bar csc326"

If you want get more instructions of how to use the `ab` command, type `man ab` to get more detailed description

Since people's requirements vary, the setup on the test machine is really up to you, as long as you have the server running on the other side


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

`test = backend_test('you-test-urls-txt', verbose=True)`

`test.test_all()`

`review the messages to examin the test results`

