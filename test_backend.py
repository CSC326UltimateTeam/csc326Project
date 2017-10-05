from crawler import crawler
import time
class backend_test (object):
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

    def test_crawl(self, depth=1):
        print "testing crawler"
        print "crawing website with depth " + str(depth) +", this may take a while"
        self.test_crawler.crawl(depth=depth)
        num_words= len(self.test_crawler._word_id_cache)

        invterted_index_len = len(self.test_crawler.get_inverted_index())
        resolved_inverted_index_len = len(self.test_crawler.get_resovled_inverted_index())

        if  self.verbose:
            print "number of word in cache: " + str(num_words)
            print "number of inverted index int keys: " + str(invterted_index_len)
            print "number of inverted index string keys: " + str(resolved_inverted_index_len)

        if (not (num_words==invterted_index_len==resolved_inverted_index_len)):
            print "inconsistent lengths across dictionaries "
            print "1 out of 1 test failed"
            exit(-1)
        print "test: crawler passed\n"


    def test_inverted_index_validity(self):
        print "running validity test on all cached words, this may take a while"
        time.sleep(3)
        if len(self.test_crawler._word_id_cache) ==0:
            return
        else:

            try:

                numtests=0
                num_falied_tests=0;
                inverted_index=self.test_crawler.get_inverted_index()
                inverted_words=self.test_crawler.get_resovled_inverted_index()

                for actual_word in self.test_crawler._word_id_cache:

                    id=self.test_crawler._word_id_cache[actual_word]
                    if self.verbose:
                        print "running validity test on word: " + str(actual_word)+ " with ID: " +str(id)
                    url_ids = list(inverted_index[id])
                    url_ids.sort()

                    url_strings = inverted_words[actual_word]

                    num_urlId=len(url_ids)
                    num_urlString=len(url_strings)

                    if self.verbose:
                        print "url ids following the word: "+ str(actual_word) + " with id: " + str(id)
                        print url_ids
                        print "total of: " + str(num_urlId) + " url ids and total of " +str(num_urlString) + " url strings"

                    if (num_urlId!= num_urlString):
                        print "test failed for unmaching sizes"
                        num_falied_tests+=1
                        numtests+=1
                        continue

                    retrived_url_ids_from_cache = [self.test_crawler._doc_id_cache[url] for url in url_strings]
                    retrived_url_ids_from_cache.sort()

                    if self.verbose:
                        print "the returned ids based on the urls corresponding to the inverted dictionary"
                        print retrived_url_ids_from_cache

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
                    print "'{0}' of {0} tests failed".format(num_falied_tests,numtests)
                    exit(-1)
                else:

                    print "test: inverted index validity passed\n"

            except Exception as er:
                print "test failed with uncaught exceptions "
                print "message: "+ er
                exit(-1)



    def test_all (self):


        self.test_crawl()
        self.test_inverted_index_validity()

        print "all tests passed"

if __name__ == '__main__':
    a=backend_test('/Users/Nix/Desktop/CSC326/csc326Project/urls.txt', verbose=False)
    a.test_all()




