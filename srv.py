from bottle import route, run, template, static_file, request, redirect
import operator
searchHistory = {}

@route('/static/<filename:path>')
def send_static(filename) :
    return static_file(filename, root='./static/')

@route('/')
def index() :
    return template('index.tpl')

@route('/test')
def index() :
    output = '<b> it works</b> !'
    return output

@route('/searchAction' , method = 'GET')
def search() :
    dictionary = {}
    inputString = request.query.get('keywords')
    splitString = inputString.split()
    if not splitString:
        redirect('/')
        pass
    #get search results
    for word in splitString:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
  #store keywords
    for row in dictionary:
          if row in searchHistory:
              searchHistory[row] += dictionary[row]
          else:
              searchHistory[row] = 1
    historyLen = len(searchHistory)
    if(historyLen < 20):
        sortedHistory = dict(sorted(searchHistory.iteritems(), key=operator.itemgetter(1), reverse=True)[:historyLen])
    else:
        sortedHistory = dict(sorted(searchHistory.iteritems(), key=operator.itemgetter(1), reverse=True)[:20])
    print sortedHistory
    return template('searchResult.tpl', dictionary = dictionary, keywords = inputString, history = sortedHistory)

@route('/about')
def about( ):
      template('about.tpl')

run(host='localhost', port = 8080,  debug=True, reloader=True)
