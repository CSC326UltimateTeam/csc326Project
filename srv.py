import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from bottle import route, run, template, static_file, request, redirect, error, Bottle
import operator
import bottle
import sqlite3
from collections import OrderedDict
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from collections import Counter
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import serverHelper as sh
import httplib2
from image_recognition import *

'''globals'''
searchHistory = {}
fullSearchHistory = {}
recentSearchList = []
lastCode = ""
category = 0
lastRouteTrack = ""
app = Bottle()
ignoreMistake = 0
conn = sqlite3.connect('Crawler.db')
c = conn.cursor()
c.execute("""SELECT distinct content from Words""")
WORDS = Counter([ str(i[0]) for i in c.fetchall()])


ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])
'''End of globals'''

image_model_init()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

@route('/screenshot', method = 'POST')
def screenshotWebPage():
    url = request.forms.get("url")
    imagepath = sh.webpageScreenshot(url)
    return imagepath

@route('/suggestion', method = 'POST')
def send_search_suggestion():

    userinput=request.forms.get("query")
    query_words = userinput.split(" ")
    if len(query_words)==1:
        list_suggestions=guess_from_word(query_words[0])

    else:
        list_suggestions=guess_from_setence(query_words)

    formatted_suggestions = sh.getHistoryBarHtml (list_suggestions)

    return formatted_suggestions

def guess_from_word(word):

    #find the words that match this input command
    match_list = [match for match in WORDS if word in match[:len(word)]]
    #if there are multiple matches, very often the case
    if len(match_list)>0:
        first_word = min(match_list)
    #otherwise find the closest possible one
    else:
        first_word = sh.autoCorrect(word)
    #this word will be our first suggestion
    sugg = [first_word]
    #then we find the searches that relate to this query
    prev_similar = {search: freq for search, freq in fullSearchHistory.items() if first_word in search}
    #select the top five
    sug_len = 5 if len(prev_similar)>5 else len(prev_similar)

    max_prev =  sorted(prev_similar.iteritems(), key=operator.itemgetter(1), reverse=True)[:sug_len]
    #return them all
    sugg += [sug[0] for sug in max_prev]

    return sugg

def guess_from_word(word):

    #find the words that match this input command
    match_list = [match for match in WORDS if word in match[:len(word)]]
    #if there are multiple matches, very often the case
    if len(match_list)>0:
        first_word = min(match_list)
    #otherwise find the closest possible one
    else:
        if word not in ignored_words:
            first_word = sh.autoCorrect(word)
        else:
            first_word=word
    #this word will be our first suggestion
    sugg = [first_word]
    #then we find the searches that relate to this query
    prev_similar = {search: freq for search, freq in fullSearchHistory.items() if first_word in search}
    #select the top five
    sug_len = 5 if len(prev_similar)>5 else len(prev_similar)

    max_prev =  sorted(prev_similar.iteritems(), key=operator.itemgetter(1), reverse=True)[:sug_len]
    #return them all
    sugg += [sug[0] for sug in max_prev]

    return sugg

def guess_from_setence(query_words):

    query_words_mod =[]
    for word in query_words:
        if word in ignored_words:
            query_words_mod.append(word)
        else:
            query_words_mod.append(sh.autoCorrect(word))

    list_words_in_searches = [ list(search.split()) for search in fullSearchHistory]

    search_hit={}
    for id, search_words in enumerate(list_words_in_searches):
        hit=0
        for word in search_words:
            for user_word in query_words_mod:

                if user_word==word:
                    hit+=1
        if (hit>0):
            search_hit[id] = hit

    sug_len = 5 if len(search_hit) > 5 else len(search_hit)

    max_prev = sorted(search_hit.iteritems(), key=operator.itemgetter(1), reverse=True)[:sug_len]
    return [' '.join(query_words_mod)] + [' '.join(list_words_in_searches[sug[0]]) for sug in max_prev]


@route('/imagenet', method='POST')
def image_net():
    upload = request.files.get('imageSearch')
    name, ext = os.path.splitext(upload.filename)
    save_path = "/tmp/imagenet/"
    if not os.path.exists(save_path):
       os.makedirs(save_path)
    file_path = "{path}{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path, overwrite = True)
    print 'uploaded file at ', file_path

    redirect('/?keywords= {}'.format(run_search(upload.filename)[0]))





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
    global ignoreMistake

    #check whether logged in
    s = bottle.request.environ.get('beaker.session')
    #print s
    logInStatus =  s.get('logInStatus',0)
    LogInOffHtml= ''
    changePhotoHtml = ''
    userInfoHtml = '<div class="userInfo"><li style="font-size: 20px; font-weight: bold;" class="lang" key="hiStranger"> Hi Stranger!</li></div>'
    userImage = "static/images/anonymous.png"
    #s['']

    #if not logged in

    if logInStatus != 'loggedIn':
        accountName = '<span class="lang" key="signIn">Sign In</span>'
        mode = 'Anonymous'
        s['mode'] = mode
        LogInOffHtml = '<li class="divider"></li><li><a href="/account" class="lang btn-default btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userImage = user_document['picture']
        changePhotoHtml = '<input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >'
        userInfoHtml = '<li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li>'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="signOut" > Sign Out </a></li>'

  #process google login in
    code = request.query.get('code', '')
    if code and code != lastCode:
        lastCode = code
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
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="signOut" > Sign Out </a></li>'
        userInfoHtml = '<li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li>'
        s.save()

    #dictionary used to record keywordsS and number of appearance
    #first sort current history
    historyLen = len(fullSearchHistory)
    firstSortedHistory = OrderedDict(sorted(fullSearchHistory.iteritems(), key=operator.itemgetter(1), reverse=True)[:historyLen])
    dictionary = OrderedDict()
    inputString = request.query.get('keywords')
    pageString = request.query.get('page')
    tempIgnoreMistake = request.query.get('ignoreMistake')
    historyBarHtml = '<label for="imagenet-upload"> <li style="font-size: 19px; text-align:left;margin-left:4%" class="lang" key="searchImage">Search with Image </li></label>'
    resultHistoryBarHtml = '<label for="imagenet-upload"> <li style="font-size:13px; text-align:left;margin-left:4%" class="lang" key="searchImage">Search with Image </li></label>'
    if not pageString:
        page = 1
    else:
        page = int(pageString)
    if not tempIgnoreMistake and not pageString:
        ignoreMistake = 0
    if tempIgnoreMistake and not pageString:
        ignoreMistake = 1
    if not inputString:
        return template('index.tpl', accountText = accountName,
                        LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml,
                        userImage = userImage, changePhotoHtml = changePhotoHtml,
                        historyBarHtml = historyBarHtml)

    tempString = inputString.lower()
    #get rid of space
    splitString = tempString.split()
    #if splitString is empty (i.e. input string only consists of space or is empty), redirect route to root
    if not splitString:
       return template('index.tpl', accountText = accountName,
                       LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml,
                       userImage = userImage, changePhotoHtml = changePhotoHtml,
                       historyBarHtml = historyBarHtml)

    #parse query string
    firstKeyWord = inputString.split()[0]
    if not page or page == 1:
        pageStart = 0
        page = 1
    else:
        pageStart = (page - 1)*5
    urlHtml, resultNumber = sh.searchKeyWord(firstKeyWord, inputString,  pageStart,ignoreMistake)
    navUrl = sh.createPageNavs(resultNumber,page,inputString)
    if inputString in fullSearchHistory:
        fullSearchHistory[inputString] += 1
    else:
        fullSearchHistory[inputString] = 1

    for word in splitString:
        if logInStatus == 'loggedIn':
            recentSearchList.append(word)
        #if word already exits in dictionary, add one to its appearance
        if word in dictionary:
            dictionary[word] += 1
        else:
        #if word doesn't exist in dictionary, set one as its appearance
            dictionary[word] = 1
    for row in dictionary:
          if row in searchHistory:
              searchHistory[row] += dictionary[row]
          else:
              searchHistory[row] = 1
  #store keywords in search history
    #if logInStatus == 'loggedIn':
        #for row in dictionary:
        #      if row in searchHistory:
        #          searchHistory[row] += dictionary[row]
        #      else:
        #          searchHistory[row] = 1
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
    return template('searchResultAnonymous.tpl', dictionary = dictionary,
                    keywords = inputString, history = sortedHistory, accountText = accountName,
                    LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage,
                    changePhotoHtml = changePhotoHtml , urlHtml = urlHtml,
                    resultNumber = resultNumber, navUrl = navUrl,historyBarHtml=resultHistoryBarHtml)
    if s['mode'] == 'Signed-In':
        return template('searchResultLoggedIn.tpl', dictionary = dictionary,
                        keywords = inputString, history = sortedHistory, accountText = accountName,
                        LogInOffHtml = LogInOffHtml, userInfoHtml = userInfoHtml, userImage = userImage ,
                        changePhotoHtml = changePhotoHtml, mostRecentSearch = mostRecentSearch, navUrl = navUrl )
    else:
        return template('searchResultAnonymous.tpl', dictionary = dictionary, keywords = inputString,
                        history = sortedHistory, accountText = accountName, LogInOffHtml = LogInOffHtml,
                        userInfoHtml = userInfoHtml, userImage = userImage, changePhotoHtml = changePhotoHtml ,
                        urlHtml = urlHtml, resultNumber = resultNumber, navUrl = navUrl, historyBarHtml=resultHistoryBarHtml)

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
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path, overwrite = True)
    s = bottle.request.environ.get('beaker.session')
    user_document = s['userDocument']
    user_document["picture"] = file_path
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
        accountName = '<span class="lang" key="signIn">Sign In</span>'
        s['mode'] = 'Anonymous'
        LogInOffHtml = '<li class="divider"></li><li><a href="/account" class="lang btn btn-default" key="account"> Log In With Google </a></li>'
        s.save()
    else:
        user_document = s['userDocument']
        accountName = user_document['name']
        accountEmail = user_document['email']
        userInfoHtml = '<div class="userInfo"><li style="font-size: 20px; font-weight: bold;">' + accountName + '</li>' + '<li>' + accountEmail + '</li> <li class="divider"></li></div>'
        LogInOffHtml = '<li><a href="/signOut" class="lang btn btn-default" key="signOut" > Sign Out </a></li>'
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

run(host='0.0.0.0', port = 80,  debug=True, reloader=True, app=app)
