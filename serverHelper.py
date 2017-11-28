import sqlite3
import datetime
import math
import operator
from itertools import permutations
import spellingCorrection as sC
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
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
    urlHtml = ''
    result,displayEquation = mathEquationHandler(wholeString)
    if result != None:
        urlHtml += '<h1 style = "margin-left: 10%; margin-top: 0.5%; font-size: 20px">' + displayEquation + str(result) + '</h1>'
    keywords = wholeString.lower()
    keywords = wholeString.split()
    syntaxedWords = ' OR '.join(keywords)
    print syntaxedWords
    correctedString = autoCorrect(wholeString)
    print 'correctedString is', correctedString
    spellingMistake = (correctedString != wholeString)
    print 'spellingMistake is ',spellingMistake

    if  spellingMistake:
         urlHtml += '<h1 style="margin-left: 10%; margin-top: 1% ;font-size: 20px; color: #e1756e ; "> Did you mean: ' + '<a href="?keywords='  + correctedString + ' " style="color:#1C1BA8;">' + correctedString + '</a></h1>'
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
