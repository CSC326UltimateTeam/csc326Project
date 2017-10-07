from bottle import route, run, template, static_file, request, redirect
import operator
from collections import OrderedDict
searchHistory = {}

#this lab has implemented bootstrap api (i.e. bootstrap css and bottstrap js) and jquery

#function to load static files (eg. images, js and css)
@route('/static/<filename:path>')
def send_static(filename) :
    return static_file(filename, root='./static/')
#root route "/"
@route('/', method = 'GET' )
def index() :
    #dictionary used to record keywords and number of appearance
    dictionary = OrderedDict()
    inputString = request.query.get('keywords')
    if not inputString:
        return template('index.tpl')
    tempString = inputString.lower()
    #get rid of space
    splitString = tempString.split()
    #if splitString is empty (i.e. input string only consists of space or is empty), redirect route to root
    if not splitString:
       return template('index.tpl')
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
    return template('searchResult.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory)



#route for testing
@route('/test')
def index() :
    output = '<b> it works</b> !'
    return output


#route for about page
@route('/about')
def about( ):
      return template('about.tpl')

run(host='localhost', port = 8080,  debug=True, reloader=True)
