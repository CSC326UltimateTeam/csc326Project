import sqlite3
import datetime
import math

conn = sqlite3.connect('Crawler.db')
c = conn.cursor()
maxUrlPage = 10


def searchKeyWord(keyword, wholeString):
    keyPair = (keyword,)
    print "keyword is ", keyword
    urlHtml = {}
    resultNumber = 0
    startime = datetime.datetime.now()
    data = c.execute('SELECT * FROM Documents WHERE title=?  ORDER BY rank',  keyPair)
    endtime = datetime.datetime.now()
    runtime = endtime - startime
    result=c.fetchone()
    print runtime
    if not result:
        urlHtml = '<div class="" style="margin-left: 13%; margin-top: 5%; font-size:16px;">' + '<p>Your search  <strong>' +wholeString+ '</strong> did not match any documents</p><br>' + '<p>Suggestions:</p><li>Make sure that all words are spelled correcly</li><li>Try different keywords</li><li>Try more general keywords</li><li>Try fewer keywords</li>' + '<img style="margin-left:45%; width:20%; margin-top:-15%"  src="static/images/noResult.png" alt="">'
    else:
        urlHtml, resultNumber = createUrls(data)
    print urlHtml
    return urlHtml, resultNumber
    #for row in data:
         # print row


def createUrl(title,url,description):
    urlHtml =  '<div class="" style="margin-left:12%">' + '<h3><a href=" ' + url +' " style="color: #1C1BA8">'+title+'</a></h3>' +'<p style="margin-top:-1.2%; "><a href="#" style=" color:green;">'+url+'</a></p>'+'<p style="margin-top:-0.5%;">'+description+'</p><p></p> </div>'
    return urlHtml

def createUrls(data):
    resHtml = ''
    resNumber = 0
    for row in data:
        resNumber += 1
        (id,rank,title,description,accesstime,whatever) = row
        print title
        url = 'https://www.google.ca'
        resHtml += createUrl(title,url,description)
        #print row
    return resHtml, resNumber

def createPageNavs(resultNumber):
      navUrl = ''
      print 'resultnumber is ', resultNumber
      pageNumber = int(math.ceil(resultNumber/5.0))
      if pageNumber > 1:
          navUrl = ' <div class="paging-nav">'
          for pageCreating in range(pageNumber+1)[1:]:
                 navUrl +=  '<a href="" class="pagenav">' +str(pageCreating)  + '</a>'
          navUrl += '</div>'
      return navUrl
