from bottle import route, run, template, static_file, request

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
  inputString = request.query.get('keywords')
  return inputString




run(host='localhost', port = 8080,  debug=True)
