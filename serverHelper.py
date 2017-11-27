import sqlite3
import datetime
import math
from itertools import permutations
import spellingCorrection as sC
#from autocorrect import spell

conn = sqlite3.connect('Crawler.db')
c = conn.cursor()
maxUrlPage = 10
cache = {}


def autoCorrect(wholeString):
    keywords = wholeString.split()
    newString = ''
    correctedWords = []
    for word in keywords:
        correctedWords.append(sC.correction(word))
    newString = ' '.join(correctedWords)
    return newString

def searchKeyWord(keyword, wholeString, startingIndex):
    keywords = wholeString.lower()
    keywords = wholeString.split()
    syntaxedWords = ' OR '.join(keywords)
    print syntaxedWords
    correctedString = autoCorrect(wholeString)
    print 'correctedString is', correctedString
    spellingMistake = (correctedString != wholeString)
    print 'spellingMistake is ',spellingMistake
    urlHtml = ''
    if  spellingMistake:
         urlHtml = '<h1 style="margin-left: 10%; margin-top: 1% ;font-size: 20px; color: #e1756e ; "> Did you mean: ' + '<a href="?keywords='  + correctedString + ' " style="color:#1C1BA8;">' + correctedString + '</a></h1>'
    keyword = keyword.lower()
    keyPair = (keyword,)
    if keyword in cache:
        result = cache[keyword]
    else:
        data = c.execute('SELECT title,url,description FROM Webpages join WordExists on url = inURL WHERE content=?  ORDER BY rank desc '  ,  keyPair)
        result = c.fetchall()
        cache[keyword] = result
    resultNumber = len(result)
    #print result
    if not result:
        urlHtml += '<div class="" style="margin-left: 13%; margin-top: 5%; font-size:16px;">' + '<p>Your search  <strong>' +wholeString+ '</strong> did not match any documents</p><br>' + '<p>Suggestions:</p><li>Make sure that all words are spelled correcly</li><li>Try different keywords</li><li>Try more general keywords</li><li>Try fewer keywords</li>' + '<img style="margin-left:45%; width:20%; margin-top:-15%"  src="static/images/noResult.png" alt="">'
    else:
        urlHtml += createUrls(result,startingIndex,resultNumber)
    #print urlHtml
    return urlHtml, resultNumber
    #for row in data:
         # print row


def createUrl(title,url,description):
    if not title:
        title = url.replace("http://","")
        title = title.replace("https://","")
        title = title.replace("www.","")
        title = title.split('/')[0]
    if not description:
        description = "No Description Available"
    if len(url) > 90:
        url = url[:91]+'...'
    urlHtml =  '<div class="" style="margin-left:10%; margin-top:1.5%">' + '<p><a href=" ' + url +' " style="color: #1C1BA8; font-size: 18px;">'+title+'</a></p>' +'<p style="margin-top:-0.8%;font-size:12px; color:green;">'+url+'</p>'+'<p style="margin-top:-1%; font-size:13px; width:45%">'+description+'</p><p></p> </div>'
    return urlHtml

def createUrls(data,startingIndex,resultNumber):
    #print 'starting index is' ,startingIndex
    resHtml = ''
    #print "data is ",data
    endingIndex = startingIndex+5
    if endingIndex >= resultNumber:
        endingIndex = resultNumber
    for row in data[startingIndex:endingIndex]:
        (title,url,description) = row
        resHtml += createUrl(title,url,description)
        #print row
    return resHtml

def createPageNavs(resultNumber,page,keywords):
      navUrl = ''
      #print 'pageNumber is ', page
      pageNumber = int(math.ceil(resultNumber/5.0))
      print "page number is", pageNumber
      if pageNumber > 1:
          if page != 1:
             navUrl = ' <div class="paging-nav" style="margin-left:8.5% ; margin-top:3%"> <a href="?keywords='  +keywords +  '&page='  + str(page-1) +  '" class="pagenav" style="margin-left:14px; font-size:12px">Previous</a> '
          else:
             navUrl = '<div class="paging-nav" style="margin-left:8.5%">'
          if pageNumber <= 10:
              for pageCreating in range(pageNumber+1)[1:]:
                     activeString = ''
                     if page == pageCreating:
                        activeString = 'page-active'
                     navUrl +=  '<a href="?keywords=' +keywords +  '&page=' + str(pageCreating) + '" class="pagenav  ' + activeString +  '" style="margin-left:14px" >' +str(pageCreating)  + '</a>'

              if page !=  pageNumber:
                  navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav" style="margin-left:14px; font-size:12px">Next</a></div>'
              else:
                  navUrl += '</div>'
          else:
             if page < 5:
                  for pageCreating in range(pageNumber+1)[1:11]:
                         activeString = ''
                         if page == pageCreating:
                            activeString = 'page-active'
                         navUrl +=  '<a href="?keywords=' +keywords +  '&page=' + str(pageCreating) + '" class="pagenav  ' + activeString +  '" style="margin-left:14px" >' +str(pageCreating)  + '</a>'

                  if page !=  pageNumber:
                      navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav" style="margin-left:14px; font-size:12px">Next</a></div>'
                  else:
                      navUrl += '</div>'
             else:
                 for pageCreating in range(pageNumber+1)[page-4:page+5]:
                        activeString = ''
                        if page == pageCreating:
                           activeString = 'page-active'
                        navUrl +=  '<a href="?keywords=' +keywords +  '&page=' + str(pageCreating) + '" class="pagenav  ' + activeString +  '" style="margin-left:14px" >' +str(pageCreating)  + '</a>'

                 if page !=  pageNumber:
                     navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav" style="margin-left:14px; font-size:12px">Next</a></div>'
                 else:
                     navUrl += '</div>'
      return navUrl


def getHistoryBarHtml(history):
      historyBarHtml = ''
      length = len(history)
      if length == 0:
          return '<li style="font-size:19px; text-align:left"> <a>History not Available </a> </li>'
      if length < 5:
          for item in history:
              historyBarHtml += getHistoryBarLi(item)
      else:
           i = 0
           for item in history:
               if i == 5:
                   break
               historyBarHtml += getHistoryBarLi(item)
               i += 1
      return historyBarHtml


def getHistoryBarLi(item):
    return '<li style="font-size:19px; text-align:left" ><a href="?keywords=' +item + '">' + item + '</a></li'
