# Copyright (C) 2011 by Peter Goodman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
import re
import sqlite3

#This is the modified verion of the crawler done by 3 students from csc326

def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""


WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')

#this object stores all the information that may be useful for further development

class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.

    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    #added the option of verbose, the print statements are sometimes too annoying
    def __init__(self, db_conn, url_file, verbose=True):

        self.conn = sqlite3.connect(db_conn)

        self.databaseExe = self.conn.cursor()
        self.createSchema()

        self.verbose=verbose
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing."""
        self._url_queue = []
        self._doc_id_cache = {}
        self._word_id_cache = {}

        #these are the dictionaries for get_inverted_index()
        #and get_resolved_inverted_index()
        self._word_id_mapped_to_doc_id = {}

        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(7)(*args, **kargs)
        def visit_description(*args, **kargs):
            self._visit_description(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title
        self._enter['p'] = visit_description

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-7)

        # never go in and parse these tags
        self._ignored_tags = set([
            'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame',
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset',
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        self.databaseExe.execute("""select max(ID) from Webpages;""")
        result = self.databaseExe.fetchone()
        if result[0] is not None:
            self._next_doc_id=result[0]+1

        else:
            self._next_doc_id = 1

        self.databaseExe.execute("""select max(ID) from Words;""")
        result = self.databaseExe.fetchone()


        if result[0] is not None:
            self._next_word_id=result[0] +1

        else:
            self._next_word_id = 1

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 0
        self._curr_words = None

        # get all urls into the queue
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    self._url_queue.append((self._fix_url(line.strip(), ""), 0))
        except IOError as er:
            print (er)
            pass



    def createSchema (self):

        self.databaseExe.execute("""CREATE TABLE if not EXISTS Webpages(\
                                             ID int NOT NULL,\
                                             url text NOT NULL,\
                                             rank real not NULL,\
                                             title text,\
                                             description text,\
                                             last_accessed date,\
                                             visit_count int NOT NULL,\
                                             updated int NOT NULL,\
                                             PRIMARY KEY(url)\
                                             UNIQUE (ID)\
                                            );""")

        self.databaseExe.execute("""CREATE TABLE if not EXISTS Directs(\
                                            source int NOT NULL,\
                                            destination int NOT NULL,\
                                            times int,\
                                            PRIMARY KEY (source, destination));""")

        self.databaseExe.execute("""CREATE TABLE if not EXISTS Words(\
                                                     ID int NOT NULL,\
                                                     content text NOT NULL,\
                                                     PRIMARY KEY(content)\
                                                     UNIQUE (ID)\
                                                    );""")

        self.databaseExe.execute("""CREATE TABLE if not EXISTS WordExists(\
                                                             content text NOT NULL,\
                                                             inURL text not NULL,\
                                                             times int, \
                                                             PRIMARY KEY(content,inURL)\
                                                            );""")

        self.conn.commit()


    def _insert_document(self, url):
        """A function that pretends to insert a url into a document db table
        and then returns that newly inserted document's id."""
        '''
        try:

            self.databaseExe.execute("""INSERT INTO Webpages VALUES ( ?, ?,0, '', '', '', 0,0);"""\
                                     , (self._next_doc_id, url))

            inserted_id = self._next_doc_id
            self._next_doc_id +=1

            if self.verbose:
                print("\nInsertion: %s"%url)
            return inserted_id
        
        except sqlite3.IntegrityError:
        '''
        self.databaseExe.execute("""SELECT ID FROM Webpages WHERE url = ?;""" , (url,))
        ret = self.databaseExe.fetchone()
        if ret is not None:
            return ret[0]
        else:

            inserted_id = self._next_doc_id
            self._next_doc_id += 1
            return inserted_id


    def _insert_word(self, word):
        """A function that  insterts a word into the lexicon db table
        and then returns that newly inserted word's id."""
        try:
            self.databaseExe.execute ("""INSERT into Words values (?, ?);""",(self._next_word_id, str(word)))
            ret = self._next_word_id
            self._next_word_id+=1

            return ret

        except sqlite3.IntegrityError:

            self.databaseExe.execute("""select ID from Words WHERE content = ?;""", (str(word),))

            ret = self.databaseExe.fetchone()
            if ret is not None:
                return ret[0]



       #newly added funtion to return the new hash tables
    def get_inverted_index(self):

        return self._word_id_mapped_to_doc_id

    def get_resovled_inverted_index(self):

        return self._word_mapped_to_url


    def word_id(self, word):

        word_id= self._insert_word(word)

        try:
            self.databaseExe.execute( """INSERT into WordExists values (?, ?, 1.);""" ,(word, self._curr_url))

        except sqlite3.IntegrityError:

            self.databaseExe.execute( """UPDATE WordExists\
                                      SET times=times+1\
                                      where content=? and inURL=?;""",(word,self._curr_url))

        return word_id


    def document_id(self, url):
        """Get the document id for some url."""
        if url in self._doc_id_cache:
            return self._doc_id_cache[url]

        # TODO: just like word id cache, but for documents. if the document
        #       doesn't exist in the db then only insert the url and leave
        #       the rest to their defaults.

        doc_id = self._insert_document(url)

        self._doc_id_cache[url] = doc_id
        return doc_id

    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""

        # compute the new url based on import
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        return urlparse.urljoin(parsed_url.geturl(), rel)

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database, or increase the number of links between
        two pages in the database."""
        try:
            self.databaseExe.execute("""INSERT into Directs values (?,?,1) """,(from_doc_id,to_doc_id))


        except sqlite3.IntegrityError:
            self.databaseExe.execute("""UPDATE Directs SET times =  times +1 \
                                    where source = ? and destination =?""",(from_doc_id,to_doc_id))


    def _visit_title(self, elem):

        """Called when visiting the <title> tag."""
        self.title_text = self._text_of(elem).strip()
        #self.databaseExe.execute("""UPDATE Webpages SET title= ?""", (title_text,))

    def _visit_description(self, elem):
        text= self._text_of(elem).strip()
        cut = 300 if len(text) >300 else len(text)
        self.description_text = text[:cut] + "..."
        #self.databaseExe.execute("""UPDATE Webpages SET description= ?""", (description_text,))

    def _visit_a(self, elem):
        """Called when visiting <a> tags."""

        dest_url = self._fix_url(self._curr_url, attr(elem, "href"))

        # print "href="+repr(dest_url), \
        #      "title="+repr(attr(elem,"title")), \
        #      "alt="+repr(attr(elem,"alt")), \
        #      "text="+repr(self._text_of(elem))

        # add the just found URL to the url queue
        self._url_queue.append((dest_url, self._curr_depth))

        # add a link entry into the database from the current document to the
        # other document
        self.add_link(self._curr_doc_id, self.document_id(dest_url))

        # TODO add title/alt/text to index for destination url

    def _add_words_to_document(self):
        # TODO: knowing self._curr_doc_id and the list of all words and their
        #       font sizes (in self._curr_words), add all the words into the
        #       database for this document


        #in cur_words, each element is the word_id and the font size,
        #the font size is not of particular interest in this lab,
        #so only word[0] is used to created the dictionary

        for word in self._curr_words:
            if word[0] in self._word_id_mapped_to_doc_id:

                self._word_id_mapped_to_doc_id[word[0]].add(self._curr_doc_id)

            else:

                self._word_id_mapped_to_doc_id[word[0]] = set()
                self._word_id_mapped_to_doc_id[word[0]].add(self._curr_doc_id)

        #if self.verbose:
           # print ("    num words=" + str(len(self._curr_words)))

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""

        def increase_it(elem):
            self._font_size += factor

        return increase_it

    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""
        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue

            self._curr_words.append((self.word_id(word), self._font_size))

    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = []
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))

            return " ".join(text)
        else:
            return elem.string

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when entering
        and leaving tags. When we come accross some text, add it into the index. This
        handles ignoring tags that we have no business looking at."""

        class DummyTag(object):
            next = False
            name = ''

        class NextTag(object):
            def __init__(self, obj):
                self.next = obj

        tag = soup.html
        stack = [DummyTag(), soup.html]

        while tag and tag.next:

            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)

                    continue

                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

            # text (text, cdata, comments, etc.)
            else:
                self._add_text(tag)
        try:
            if self.title_text=='EECG Student Guide':
                return
            self.databaseExe.execute("""INSERT INTO Webpages VALUES ( ?, ?,1, ?, ?, '', 0,0);""" \
                                     , (self._curr_doc_id, self._curr_url,self.title_text,self.description_text))

            print "insertion: ", self._curr_url, "title: ", self.title_text
            self.title_text=''
            self.description_text=''

        except sqlite3.IntegrityError:
            pass

    def crawl(self, depth=2, timeout=1):
        """Crawl the web!"""
        seen = set()


        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            doc_id = self.document_id(url)

            # we've already seen this document
            if doc_id in seen:
                continue

            seen.add(doc_id)  # mark this document as haven't been visited

            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())

                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 0
                self._curr_words = []
                self._index_document(soup)
                self._add_words_to_document()
                self.conn.commit()

            except Exception as e:
                if self.verbose:
                    print(e)
                pass
            finally:
                if socket:
                    socket.close()



    #similar to the pagerank algorithm used by the reference function
    def calcRank(self, num_iterations=20,initial_pr=1.0):

        self.databaseExe.execute("""SELECT source, destination, times from Directs;""");
        links = self.databaseExe.fetchall()

        from collections import defaultdict
        import numpy as np
        page_rank = defaultdict(lambda: float(initial_pr))
        num_outgoing_links = defaultdict(float)
        incoming_link_sets = defaultdict(set)
        incoming_links = defaultdict(lambda: np.array([]))
        damping_factor = 0.85

        # collect the number of outbound links and the set of all incoming documents
        # for every document
        for (from_id, to_id, times) in links:
            num_outgoing_links[int(from_id)] += times
            incoming_link_sets[to_id].add(int(from_id))

        # convert each set of incoming links into a numpy array
        for doc_id in incoming_link_sets:
            incoming_links[doc_id] = np.array([from_doc_id for from_doc_id in incoming_link_sets[doc_id]])

        num_documents = float(len(num_outgoing_links))
        lead = (1.0 - damping_factor) / num_documents
        partial_PR = np.vectorize(lambda doc_id: page_rank[doc_id] / num_outgoing_links[doc_id])

        for _ in xrange(num_iterations):
            for doc_id in num_outgoing_links:
                tail = 0.0
                if len(incoming_links[doc_id]):
                    tail = damping_factor * partial_PR(incoming_links[doc_id]).sum()
                page_rank[doc_id] = lead + tail
                self.databaseExe.execute("""UPDATE Webpages SET rank = ? where ID = ?""", (lead + tail,doc_id))
                self.conn.commit()




if __name__ == "__main__":

#start crawling the web
    a=crawler('Crawler.db','urls.txt',verbose=True)
    a.crawl(depth=2);
    a.calcRank()

