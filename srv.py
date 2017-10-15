from bottle import route, run, template, static_file, request, redirect
import operator
import bottle
from collections import OrderedDict
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import httplib2
searchHistory = {}
lastCode = ""

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

#this lab has implemented bootstrap api (i.e. bootstrap css and bottstrap js) and jquery

#function to load static files (eg. images, js and css)
@route('/static/<filename:path>')
def send_static(filename) :
    return static_file(filename, root='./static/')
#root route "/"
@route('/account', method = 'GET' )
def home() :
    #check whether logged in
    s = bottle.request.environ.get('beaker.session')
    #print s
    logInStatus =  s.get('logInStatus',0)
    if logInStatus != 'loggedIn':
        #google sign in
        flow = flow_from_clientsecrets("client_secret_768721561947-cda1s6rph24pem3t6h4pa3e4016ua9rk.apps.googleusercontent.com.json",
        scope= 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
        redirect_uri="http://localhost:8080/")
        uri = flow.step1_get_authorize_url()
        redirect(str(uri))
        ####
    else:
        redirect('/')


@route('/', method = 'GET' )
def index() :
    ####

    global lastCode


    #check whether logged in
    s = bottle.request.environ.get('beaker.session')
    #print s
    logInStatus =  s.get('logInStatus',0)
    LogInOffHtml= ''
    userInforHtml = ''
    userInfoHtml = ''

    #s['']

    #if not logged in

    if logInStatus != 'loggedIn':
        accountName = 'Sign In'
        mode = 'Anonymous'
        s['mode'] = mode
        LogInOffHtml = '<li><a href="/account" class="lang btn-default btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userInfoHtml = '<li>' + accountEmail + '</li> <li class="divider"></li>'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="account" > Sign Out </a></li>'

  #process google login in
    code = request.query.get('code', '')
    if code and code != lastCode:
        lastCode = code
        print "now print code:"
        print code
        flow = OAuth2WebServerFlow(client_id='768721561947-cda1s6rph24pem3t6h4pa3e4016ua9rk.apps.googleusercontent.com',
                               client_secret='PTU6hiaZ7CdOdthZurcYLVk6',
                               scope='https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
                               redirect_uri='http://localhost:8080/')
        credentials = flow.step2_exchange(code)
        token = credentials.id_token['sub']
        http = httplib2.Http()
        http = credentials.authorize(http)
        # Get user email
        users_service = build('oauth2', 'v2', http=http)
        user_document = users_service.userinfo().get().execute()
        print user_document
        #user_email = user_document['email']
        #print user_emailss
        accountName = user_document['name']
        accountEmail = user_document['email']
        logInStatus = 'loggedIn'
        s['logInStatus'] = logInStatus
        mode = 'Signed-In'
        s['mode'] = mode
        s['userDocument'] = user_document
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="account" > Sign Out </a></li>'
        userInfoHtml = '<li >' + accountEmail + '</li> <li class="divider"></li>'
        s.save()

    #dictionary used to record keywordsS and number of appearance
    dictionary = OrderedDict()
    inputString = request.query.get('keywords')
    if not inputString:
        return template('index.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml)
    tempString = inputString.lower()
    #get rid of space
    splitString = tempString.split()
    #if splitString is empty (i.e. input string only consists of space or is empty), redirect route to root
    if not splitString:
       return template('index.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml)
       pass
    #parse query string
    for word in splitString:
        #if word already exits in dictionary, add one to its appearance
        if word in dictionary:
            dictionary[word] += 1
        else:
        #if word doesn't exist in dictionary, set one as its appearance
            dictionary[word] = 1
    print dictionary
  #store keywords in search history
    for row in dictionary:
          if row in searchHistory:
              searchHistory[row] += dictionary[row]
          else:
              searchHistory[row] = 1
#get length of history
    historyLen = len(searchHistory)
#if history length is less than 20, display all result in greatest first order
    if(historyLen < 20):
        sortedHistory = OrderedDict(sorted(searchHistory.iteritems(), key=operator.itemgetter(1), reverse=True)[:historyLen])
    else:
    #else display top 20 keywords in greatest first order
        sortedHistory = OrderedDict(sorted(searchHistory.iteritems(), key=operator.itemgetter(1), reverse=True)[:20])
    if s['mode'] == 'Signed-In':
        return template('searchResultLoggedIn.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory, accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml)
    else:
        return template('searchResultAnonymous.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory, accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml)

@route('/signOut')
def signOut( ):
    s = bottle.request.environ.get('beaker.session')
    s['logInStatus'] = 'offline'
    s['mode'] = 'Anonymous'
    s.save()
    redirect('/')




#route for about page
@route('/about')
def about( ):
    #check whether logged in
    s = bottle.request.environ.get('beaker.session')
    LogInOffHtml = ""
    userInforHtml = ''
    logInStatus =  s.get('logInStatus',0)
    if logInStatus != 'loggedIn':
        accountName = 'Sign In'
        s['mode'] = 'Anonymous'
        LogInOffHtml = '<li><a href="/account" class="lang btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userInfoHtml = '<li>' + accountEmail + '</li> <li class="divider"></li>'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="account" > Sign Out </a></li>'
    return template('about.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml , userInfoHtml = userInfoHtml)


run(host='localhost', port = 8080,  debug=True, reloader=True, app=app)
