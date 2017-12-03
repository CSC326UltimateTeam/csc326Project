import sqlite3
import datetime
import math
import operator
import os
from itertools import permutations
import spellingCorrection as sC
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
from depot.manager import DepotManager
from selenium import webdriver

depot = DepotManager.get()
driver = webdriver.PhantomJS()
driver.set_window_size(400, 320) # set the window size that you need

conn = sqlite3.connect('Crawler.db')
c = conn.cursor()
maxUrlPage = 10
cache = {}
ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

def webpageScreenshot(url):
    driver.get(url)
    currentPath = os.getcwd()
    path = currentPath + '/static/images/screenshot/webpage.png'
    driver.save_screenshot(path)
    return '/images/screenshot/webpage.png'


def autoCorrect(wholeString):
    keywords = wholeString.split()
    newString = ''
    correctedWords = []
    for word in keywords:
        correctedWords.append(sC.correction(word))
    newString = ' '.join(correctedWords)
    return newString

def searchKeyWord(keyword, wholeString, startingIndex,ignoreMistake):
    global lastString
    urlHtml = ''
    resultNumber=0

    result,displayEquation = mathEquationHandler(wholeString)

    if result != None:
        urlHtml += '<h1 style = "margin-left: 10%; margin-top: 0.5%; font-size: 20px">' + displayEquation + str(result) + '</h1>'

    correctedString = []
    for word in wholeString.split():
        if (word in ignored_words):
            correctedString.append(word)

        else:
            correctedString.append(autoCorrect(word))
    correctedString = ' '.join(correctedString)


    spellingMistake = (correctedString != wholeString)


    lowerKeywords = correctedString.lower()

    if  spellingMistake and ignoreMistake == 0:
         urlHtml += '<h1 style="margin-left: 10%; margin-top: 1% ;font-size: 20px; margin-bottom:-1% "> <span class="lang" key="showingResults">Showing results for</span> <a href="?keywords='  + correctedString + ' " style="color:#1C1BA8; font-style: italic;">' + correctedString +  '</a></h1> <h1 style="margin-left: 10%; margin-top:1px;"><span style="font-size:16px; font-weight:normal;"><span class="lang" key="searchInstead">Search Instead for</span> <a href="?keywords='  + wholeString + '&ignoreMistake=1" style="color:#1C1BA8;">' + wholeString + '</a></span></h1>'

    if spellingMistake and ignoreMistake == 1:
        urlHtml += '<h1 style="margin-left: 10%; margin-top: 1% ;font-size: 20px; margin-bottom:-1%; color: #df6257; "> <span class="lang" key="didMean">Did you mean</span>: <a href="?keywords='  + correctedString + ' " style="color:#1C1BA8;">' + correctedString +  '</a></h1>'

    if lowerKeywords in cache:
        result = cache[lowerKeywords]
    else:

        result = wordsearch(lowerKeywords)
    #print result
    if not result:
        urlHtml += '<div class="" style="margin-left: 13%; margin-top: 5%; font-size:16px;">' + '<p><span class="lang" key="yourSearch">Your search</span>  <strong>' +wholeString+ '</strong> <span class="lang" key="notMatching">did not match any documents</span></p><br>' + '<p class="lang" key="suggestionTitle">Suggestions:</p><li class="lang" key="suggestionOne">Make sure that all words are spelled correcly</li><li class="lang" key="suggestionTwo">Try different keywords</li><li class="lang" key="suggestionThree">Try more general keywords</li><li class="lang" key="suggestionFour">Try fewer keywords</li>' + '<div style="margin-left:25%; width:75%; margin-top:-20%; margin-bottom:-9%" id="emojiAnimation"></div>'  #'<img style="margin-left:45%; width:20%; margin-top:-15%"  src="static/images/noResult.png" alt="">'
    else:
        modifiedRes = removeDuplicate(result)
        result = modifiedRes
        cache[lowerKeywords] = result
        resultNumber = len(result)
        urlHtml += createUrls(result,startingIndex,resultNumber)
    return urlHtml, resultNumber

def removeDuplicate(list):
    #a list of tuples: (title,url,description)
    #if title and description match then only show one re
    seen = set()
    return [(a,b,c) for (a,b,c) in list if not ((a,c) in seen or seen.add((a,c)))]


#given a list of keywords, use multiple queries and the related ranks to findout the
#best way to sort thses pages
def wordsearch(lower_keywords):
    words = lower_keywords.split()
    #single word search
    if (len(words)<=1):
        c.execute("""SELECT DISTINCT title,url,description \
                    FROM Webpages join WordExists on url = inURL \
                    WHERE content = ? ORDER BY rank*(1+0.1*times) DESC""", (words[0],))
        return c.fetchall()
    else:
        url_ID_dict ={}
        for word in words:

            #first get the links that contain the words
            c.execute("""SELECT ID, times, avg_position, rank \
                        FROM Webpages join WordExists on url = inURL \
                        WHERE content = ? """, (word,))

            for row in c.fetchall():

                id, times, avg_position, rank = row

                if id not in url_ID_dict:
                    #found a new url, we store its rank, teh number of hits of this word, and
                    #the position normal, which is 0 because it is only one word
                    position_normal=avg_position * times
                    #rank, total appearance, positio normal for relevance, last time position, last_time appearance
                    url_ID_dict[id]= (rank, times, position_normal, avg_position,times )
                else:
                    #this url is already the candidate, need to compute the hitrate
                    #and the new position normal
                    rank, preve_times, preve_normal, last_word_position, last_word_appearance = url_ID_dict[id]
                    new_times= times+preve_times
                    new_normal = preve_normal + \
                                 abs(last_word_position-avg_position) * max((last_word_appearance,times))
                    #update info
                    url_ID_dict[id] = (rank, new_times, new_normal, avg_position,times)

       #now we have all the information to compare which url should go first
        sortfunction =lambda (k,v):(v[0]+1)* (v[1]**2/v[2])

        result=[]
        for id,val in sorted(url_ID_dict.iteritems(), key=sortfunction, reverse=True):

            c.execute("""SELECT DISTINCT title,url,description FROM Webpages where ID=?""", (id, ))
            for ele in c.fetchall():
                result.append(ele)

        return result



def createUrl(title,url,description):
    originalUrl = url
    if not title:
        title = url.replace("http://","")
        title = title.replace("https://","")
        title = title.replace("www.","")
        title = title.split('/')[0]
    if not description:
        description = "No Description Available"
    if len(url) > 90:
        url = url[:91]+'...'

    urlHtml =  '<div  style="margin-left:10%; margin-top:1.5%">' + '<p><a href=" ' + originalUrl +' " style="color: #1C1BA8; font-size: 18px;">'+title+'</a></p>' +'<p style="margin-top:-0.8%;font-size:12px; color:green;">&nbsp;&nbsp;'+url+'<div class="dropdown" style="font-size:10px; margin-top:-2.4%;margin-left:-0.5%"><span class="dropdown-toggle"  data-toggle="dropdown" onclick="linkTools()" style="color:green;">&#9668;</span>'+createLinkToolHtml(originalUrl)+'</p> <p style="margin-top:-1%; font-size:13px; width:45%">'+description+'</p><p></p> </div>'
    return urlHtml

def createLinkToolHtml(url):
    toolHtml = '<ul  class="dropdown-menu dropdown-menu-right" style="text-align:center; min-width:10px; margin-left:-6%; margin-top:-0.5%"> <li style="font-size:11px" class="screenshotBtn" key=' + url +'><a class="lang" key="preview">Preview</a></li></ul></div>'
    return toolHtml



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

      if pageNumber > 1:
          if page != 1:
             navUrl = ' <div class="paging-nav" style="margin-left:8.5% ; margin-top:3%"> <a href="?keywords='  +keywords +  '&page='  + str(page-1) +  '" class="pagenav lang" style="margin-left:14px; font-size:12px" key="previous">Previous</a> '
          else:
             navUrl = '<div class="paging-nav" style="margin-left:8.5%">'
          if pageNumber <= 10:
              for pageCreating in range(pageNumber+1)[1:]:
                     activeString = ''
                     if page == pageCreating:
                        activeString = 'page-active'
                     navUrl +=  '<a href="?keywords=' +keywords +  '&page=' + str(pageCreating) + '" class="pagenav  ' + activeString +  '" style="margin-left:14px" >' +str(pageCreating)  + '</a>'

              if page !=  pageNumber:
                  navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav lang" style="margin-left:14px; font-size:12px" key="next">Next</a></div>'
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
                      navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav lang" style="margin-left:14px; font-size:12px" key="next">Next</a></div>'
                  else:
                      navUrl += '</div>'
             else:
                 for pageCreating in range(pageNumber+1)[page-4:page+5]:
                        activeString = ''
                        if page == pageCreating:
                           activeString = 'page-active'
                        navUrl +=  '<a href="?keywords=' +keywords +  '&page=' + str(pageCreating) + '" class="pagenav  ' + activeString +  '" style="margin-left:14px" >' +str(pageCreating)  + '</a>'

                 if page !=  pageNumber:
                     navUrl += '<a href="?keywords='  + keywords + '&page=' + str(page+1) + '" class="pagenav lang" style="margin-left:14px; font-size:12px" key="next">Next</a></div>'
                 else:
                     navUrl += '</div>'
      return navUrl


def getHistoryBarHtml(history):
      historyBarHtml = ''
      length = len(history)
      if length == 0:
          return '<li style="text-align:left"> <a>No suggestion </a> </li>'
      if length < 5:
          for item in history:

              historyBarHtml += getHistoryBarLi(str(item))
      else:
           i = 0
           for item in history:
               if i == 5:
                   break
               historyBarHtml += str(getHistoryBarLi(str(item)))
               i += 1
      return historyBarHtml


def getHistoryBarLi(item):
    return '<li style="text-align:left" ><a href="?keywords=' +item + '">' + item + '</a></li>'


class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor <<= atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr <<= term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val



def mathEquationHandler(inputString):
    tempString = inputString
    tempString = tempString.replace('=','')
    nsp = NumericStringParser()
    try:
        evalRes = nsp.eval(tempString)
        tempWords = tempString.split()
        tempEquation = ''.join(tempWords)
        finalEquation = ' '.join(tempEquation)
        return nsp.eval(tempString), (finalEquation+' = ')
    except:
        return None, None
