from crawler import crawler
import time

''' this is a test class of the crawler '''


class backend_test (object):

    #initialization requries a file to be inputed, if there are exceptions throw in 
    #creating the class, the initialization will fail as well
    def __init__(self, urlfile, verbose=True):

        self.verbose=verbose
        print "testing initilization"
        try:
            self.test_crawler = crawler(None, urlfile,verbose=verbose)
        except Exception:
            print "initialization failed"
            print "1 out of 1 test failed"
            exit(-1)
        print "test: initilization passed\n"


        #this class tests the proper funtionality of the crawler's "crawl" function
        #if the data stored in the database have inconsistent lengths, the crawler test
        #will fail, since there are data missing or repeated 

    def test_crawl(self, depth=1):
        print "testing crawler"
        print "crawing website with depth " + str(depth) +", this may take a while"

        #crawl the web
        self.test_crawler.crawl(depth=depth)

        #after crawl, get the lengths of all interested data
        num_words= len(self.test_crawler._word_id_cache)

        invterted_index_len = len(self.test_crawler.get_inverted_index())
        resolved_inverted_index_len = len(self.test_crawler.get_resovled_inverted_index())

        if  self.verbose:
            print "number of word in cache: " + str(num_words)
            print "number of inverted index int keys: " + str(invterted_index_len)
            print "number of inverted index string keys: " + str(resolved_inverted_index_len)

        #check consistent length
        if (not (num_words==invterted_index_len==resolved_inverted_index_len)):
            print "inconsistent lengths across dictionaries "
            print "1 out of 1 test failed"
            exit(-1)
        print "test: crawler passed\n"


        #tests the validity of the data, see if the data at different dictionaries 
        #match with each other
        #this is assuming the data in word_id_cache and doc_id_cache are correct, 
        #and other dictionaries are tested against the 2 above

    def test_inverted_index_validity(self):
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

    def test_all (self):


        self.test_crawl()
        self.test_inverted_index_validity()

        print "all tests passed"

if __name__ == '__main__':
    a=backend_test('/Users/Nix/Desktop/CSC326/csc326Project/urls.txt', verbose=False)
    a.test_all()




