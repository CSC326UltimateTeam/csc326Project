from crawler import crawler
import time
import sqlite3
import sys
''' this is a test class of the crawler '''


class backend_test (object):

    #initialization requries a file to be inputed, if there are exceptions throw in
    #creating the class, the initialization will fail as well
    def __init__(self,dbfile, urlfile, verbose=True, depth =1):
        print (" \n\n\n############## This is a test class of the cralwer's PageRank functionality #############\n\n"+
              "URLs specified will be crawled and inserted to the data base if not already done so.\n"+
              "The page rank scores from 0 to 1 will be calculated from the pagerank algorithm.\n"+
              "A higher score indicates a higher probability that a random browse to the internet\n"+
              "will likely end at this page.\n\n\n")

        self.verbose=verbose
        print ("******************** testing initilization ********************\n\nURLs in file: %s, result stored in SQL db: %s\n"%(urlfile,dbfile))

        self.urls=open(urlfile,'r')
        self.db=sqlite3.connect(dbfile)
        self.depth=depth
        try:

            self.test_crawler = crawler(dbfile, urlfile,verbose=verbose)
            print("******************** test: initilization passed ********************\n")
        except Exception:
            print ("******************** initialization failed ********************")
            print ("1 out of 1 test failed")
            exit(-1)



        #this class tests the proper funtionality of the crawler's "crawl" function
        #if the data stored in the database have inconsistent lengths, the crawler test
        #will fail, since there are data missing or repeated

    def test_crawl(self):
        print ("******************** testing crawler ********************\n")
        print ("crawing websites with depth " + str(self.depth) +", this may take a while...\n")
        if self.verbose:
            time.sleep(5)
        #crawl the web
        try:
            self.test_crawler.crawl(depth=self.depth)

            #after crawl, get the lengths of all interested data
            num_words= len(self.test_crawler._word_id_cache)

            #invterted_index_len = len(self.test_crawler.get_inverted_index())
            #resolved_inverted_index_len = len(self.test_crawler.get_resovled_inverted_index())


            print ("******************** test: crawler passed ********************\n")
        except Exception as er:
            print ("******************** test failed with uncaught exceptions: ********************\n" +str(er))
            print("1 out of 1 test failed")
            exit(-1)


        #tests the validity of the data, see if the data at different dictionaries
        #match with each other
        #this is assuming the data in word_id_cache and doc_id_cache are correct,
        #and other dictionaries are tested against the 2 above

    '''def test_inverted_index_validity(self):
        print "running validity test on all cached words, this may take a while"
        #wait a little for user to read this message
        if self.verbose:
            time.sleep(3)

        #no need to check if the database is empty
        if len(self.test_crawler._word_id_cache) ==0:
            return


        else:

            try:

                #each word will be tested
                numtests=0
                num_falied_tests=0;

                inverted_index=self.test_crawler.get_inverted_index()
                inverted_words=self.test_crawler.get_resovled_inverted_index()

                #go through each word in the word id cache
                for actual_word in self.test_crawler._word_id_cache:

                    #get the id of the corresponding wword
                    id=self.test_crawler._word_id_cache[actual_word]

                    if self.verbose:
                        print "running validity test on word: " + str(actual_word)+ " with ID: " +str(id)

                    #from the id provided, get the list of url ids corrsponding to that id, from the dict (inverted index) we generated
                    url_ids = list(inverted_index[id])
                    url_ids.sort()

                    #similarly, for each word strong, get the list of unicode urls from the dict (resolved inverted index) we generated
                    url_strings = inverted_words[actual_word]


                    num_urlId=len(url_ids)
                    num_urlString=len(url_strings)

                    #print out imformation if interested
                    if self.verbose:
                        print "url ids following the word: "+ str(actual_word) + " with id: " + str(id)
                        print url_ids
                        print "total of: " + str(num_urlId) + " url ids and total of " +str(num_urlString) + " url strings"

                    #check if the length of url ids and urls match
                    if (num_urlId!= num_urlString):
                        print "test failed for unmaching sizes"
                        num_falied_tests+=1
                        numtests+=1
                        continue

                    #aquires the list of url id's from the doc id cache, by providing the actual urls we got from the
                    #resolved inverted index
                    retrived_url_ids_from_cache = [self.test_crawler._doc_id_cache[url] for url in url_strings]
                    retrived_url_ids_from_cache.sort()

                    if self.verbose:
                        print "the returned ids based on the urls corresponding to the inverted dictionary"
                        print retrived_url_ids_from_cache

                    #check if the 2 lists of url ids are consistent
                    if retrived_url_ids_from_cache != url_ids:
                        print "test failed, the information in datebases are inconsistent"
                        num_falied_tests += 1
                        numtests += 1
                        continue


                    numtests += 1
                    if self.verbose:
                        print "data with word: {0} is correct \n".format(actual_word)

                if num_falied_tests >0:
                    print "test failed on validity of inverted tables"
                    print "{} of {} tests failed".format(num_falied_tests,numtests)
                    exit(-1)
                else:
                    print "{} of {} tests failed".format(num_falied_tests,numtests)
                    print "test: inverted index validity passed\n"

            except Exception as er:
                print "test failed with uncaught exceptions "
                print "message: "+ er
                exit(-1)


    #tests all the test implemented
    '''
    def  test_pageRank(self):
        print ("******************** testing the ranks of the website ********************\n\nunder the DFT of websites: \n" )
        for url in self.urls:
            print (url)
        try:
            self.test_crawler.calcRank()

            pageRanks=self.db.cursor().execute("""SELECT url, rank FROM Webpages ORDER BY rank DESC;""").fetchall()

            print("PageRank algorithm yeilds the following results of %d total websites" %len(pageRanks))

            askFlag=False
            for index,page in enumerate(pageRanks):
                print ("")
                print ("Rank: %d" % (index+1))
                print ("URL: {}".format(page[0]))
                print ("PageRank Coefficient: %.7f"% page[1])
                if page[1] <=0.00000001 and not askFlag:

                    userAnswer= raw_input("\n\nDo you want to display the webpages that do not have outgoing links(rank=0) given the current depth\nyes, no? >>")

                    if str(userAnswer) != 'yes':
                        break
                    askFlag=True



        except Exception as er:
            print("******************** test failed ********************\nuncaught exceptions: " + str(er))
            print("1 out of 1 test failed")
            exit(-1)

    def test_all (self):


        self.test_crawl()
        self.test_pageRank()

        print ("(3/3) tests passed")

if __name__ == '__main__':
    if len(sys.argv) <3:
        print ("\ninsufficient argument supplied\nProvide arguments as follows:\npython run_backend_test.py [verbose (0 or 1)] [depth] ")
        exit(-1)
    if sys.argv[1]=='1':
        verbose =True
    else:
        verbose=False
    depth = int(sys.argv[2])
    a=backend_test("Crawler.db", 'urls.txt', verbose=verbose, depth=depth)
    a.test_all()
