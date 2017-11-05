from bottle import route, run, template, static_file, request, redirect, error, Bottle
import operator
import bottle
import sqlite3
from collections import OrderedDict
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import serverHelper as sh
import httplib2
import os
import random
searchHistory = {}
recentSearchList = []
lastCode = ""
category = 0
lastRouteTrack = ""
app = Bottle()

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
        redirect_uri="http://ec2-34-233-27-14.compute-1.amazonaws.com/")
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
    changePhotoHtml = ''
    userInfoHtml = '<div class="userInfo"><li style="font-size: 20px; font-weight: bold;"> Hi Stranger!</li></div>'
    userImage = "static/images/anonymous.png"
    #s['']

    #if not logged in

    if logInStatus != 'loggedIn':
        accountName = 'Sign In'
        mode = 'Anonymous'
        s['mode'] = mode
        LogInOffHtml = '<li class="divider"></li><li><a href="/account" class="lang btn-default btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userImage = user_document['picture']
        print "user document photo is "
        print user_document['picture']
        changePhotoHtml = '<input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >'
        userInfoHtml = '<li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li>'
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
                               redirect_uri='http://ec2-34-233-27-14.compute-1.amazonaws.com/')
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
        userImage = user_document['picture']
        changePhotoHtml = '<input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="account" > Sign Out </a></li>'
        userInfoHtml = '<li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li>'
        s.save()

    #dictionary used to record keywordsS and number of appearance
    dictionary = OrderedDict()
    inputString = request.query.get('keywords')
    pageString = request.query.get('page')
    if not pageString:
        page = 1
    else:
        page = int(pageString)
    if not inputString:
        return template('index.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage, changePhotoHtml = changePhotoHtml)
    tempString = inputString.lower()
    #get rid of space
    splitString = tempString.split()
    #if splitString is empty (i.e. input string only consists of space or is empty), redirect route to root
    if not splitString:
       return template('index.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage, changePhotoHtml = changePhotoHtml)
       pass
    #parse query string
    firstKeyWord = inputString.split()[0]
    if not page or page == 1:
        pageStart = 0
        page = 1
    else:
        pageStart = (page - 1)*10
    urlHtml, resultNumber = sh.searchKeyWord(firstKeyWord, inputString,  pageStart)
    navUrl = sh.createPageNavs(resultNumber,page,inputString)

    for word in splitString:
        if logInStatus == 'loggedIn':
            recentSearchList.append(word)
        #if word already exits in dictionary, add one to its appearance
        if word in dictionary:
            dictionary[word] += 1
        else:
        #if word doesn't exist in dictionary, set one as its appearance
            dictionary[word] = 1
    print dictionary
    print "recent search list:"
    print recentSearchList
  #store keywords in search history
    if logInStatus == 'loggedIn':
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
    #now for recent search keywords
    reversedRecentSearch = recentSearchList[::-1]
    if len(reversedRecentSearch) < 15:
        mostRecentSearch = reversedRecentSearch
    else:
        mostRecentSearch = reversedRecentSearch[:15]
    if s['mode'] == 'Signed-In':
        return template('searchResultLoggedIn.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory, accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage , changePhotoHtml = changePhotoHtml, mostRecentSearch = mostRecentSearch, navUrl = navUrl )
    else:
        return template('searchResultAnonymous.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory, accountText = accountName, LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage, changePhotoHtml = changePhotoHtml , urlHtml = urlHtml, resultNumber = resultNumber, navUrl = navUrl)

@route('/signOut')
def signOut( ):
    s = bottle.request.environ.get('beaker.session')
    s['logInStatus'] = 'offline'
    s['mode'] = 'Anonymous'
    s.save()
    redirect('/')


#route for profilePhoto
@route('/changeProfilePhoto', method='POST')
def changeProfilePhoto( ):
    global category
    upload = request.files.get("profilePhoto")
    name, ext = os.path.splitext(upload.filename)
    save_path = "static/tmp"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print upload.filename
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path, overwrite = True)
    print "path is "
    print file_path
    s = bottle.request.environ.get('beaker.session')
    user_document = s['userDocument']
    user_document["picture"] = file_path
    print "picture after change phto"
    s.save()
    redirect('/')



#route for about page
@route('/about')
def about( ):
    #check whether logged in
    s = bottle.request.environ.get('beaker.session')
    LogInOffHtml = ""
    changePhotoHtml = ''
    userInfoHtml ='<div class="userInfo"><li style="font-size: 20px; font-weight: bold;"> Hi Stranger!</li></div>'
    userImage = "static/images/anonymous.png"
    logInStatus =  s.get('logInStatus',0)
    if logInStatus != 'loggedIn':
        accountName = 'Sign In'
        s['mode'] = 'Anonymous'
        LogInOffHtml = '<li class="divider"></li><li><a href="/account" class="lang btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userInfoHtml = '<div class="userInfo"><li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li></div>'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="account" > Sign Out </a></li>'
        changePhotoHtml = '<input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >'
        userImage = user_document['picture']
    return template('about.tpl', accountText = accountName, LogInOffHtml = LogInOffHtml , userInfoHtml = userInfoHtml, userImage = userImage, changePhotoHtml=changePhotoHtml)


#route for error message
@error(404)
def errorHandler(error):
     return template('error404Page.tpl')

@error(500)
def errorHandler(error):
    return template('error500Page.tpl')

#@error()
#def errorHandler(error):
#     return  template('otherError.tpl')

#run(host='0.0.0.0', port = 80,  debug=True, reloader=True, app=app)
run(host='localhost', port = 8080,  debug=True, reloader=True, app=app)
