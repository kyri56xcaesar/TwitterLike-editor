import unittest
import development_phase as dev
import json

def reset():
    dev.current_tweet = {}
    dev.current_tweet_id = -1

class DevTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(DevTest, cls).setUpClass()
        #reset()
        dev.configureID()
        


    def test_read(self):

        reset()

        # Test invalid id case
        dev.read_tweet(0, verbose=False)
        self.assertEqual(dev.current_tweet_id, -1) # current id must be -1
        # current tweet must be None
        self.assertEqual(dev.current_tweet=={}, True)
        

        dev.read_tweet(1, verbose=False)
        self.assertEqual(dev.current_tweet_id == 0, True)
        self.assertEqual(dev.current_tweet!={}, True)
        
        # reset current_tweet and current tweet id
        reset()
        dev.read_tweet(25674, verbose=False)
        self.assertEqual(dev.current_tweet_id == 25674, False)
        self.assertEqual(dev.current_tweet=={}, False)

        # reset
        reset()
        dev.read_tweet(len(dev.mem_tweets) + 1, verbose=False)
        self.assertEqual(dev.current_tweet_id, -1)   
        self.assertEqual(dev.current_tweet=={}, True)
        




    def test_create(self):
        reset()
        time = dev.create_tweet(prompt=False, ttext="test", verbose=False)

        # test if a tweet is created
        self.assertEqual(dev.current_tweet.get("text")=="test", True)

        # test if time-date is correct
        self.assertEqual(dev.current_tweet.get("created_at")==time, True)

        # test if current_tweet is set correctly to the end of the list

        self.assertEqual(dev.current_tweet_id == len(dev.mem_tweets) - 1, True)
        


    def test_update(self):
        reset()
        time = dev.update_tweet(5, prompt=False, ttext="test", verbose=False)

        # test if new text is set correctly
        self.assertEqual(dev.current_tweet.get("text"), "test")
        
        # test if time is set correctly
        self.assertEqual(dev.current_tweet.get("created_at")==time, True)

        # test if current id is at the correct place
        self.assertEqual(dev.current_tweet_id == 4, True)

        #############
        # Case when updating an invalid tweet number
        dev.update_tweet(0, prompt=False, ttext="test2", verbose=False)

        self.assertEqual(dev.current_tweet_id, 4)
 

    def test_delete(self):

        reset()

        # test delete if no tweet is selected
        dev.delete_tweet(verbose=False)

        # must check if everything is at the same place
        for id, tweet in enumerate(dev.mem_tweets):
            dev.read_tweet(id + 1, prompt=False, verbose=False)
            self.assertEqual(dev.current_tweet_id == id, True)
            self.assertEqual(dev.current_tweet != {}, True)

        # test delete if tweet is selected
        reset()
        dev.read_tweet(2, prompt=False, verbose= False)

        # hold 3rd tweet
        dev.read_tweet(3, prompt=False, verbose=False)
        third_t = dev.current_tweet
        # go back to second
        dev.read_prev(verbose=False)

        # hold length before
        max_length = len(dev.mem_tweets)

        # delete the second(current)
        dev.delete_tweet(verbose=False)

        # check if the new second tweet is the last third tweet.
        # read the new second
        dev.read_tweet(2, prompt=False, verbose=False)
        self.assertEqual(dev.current_tweet == third_t, True)

        # check if length is reduced by 1
        self.assertEqual(len(dev.mem_tweets) == max_length - 1, True)






    def test_readPrev(self):
        
        #reset and test read_prev when we havent selected a tweet
        
        reset()
        dev.read_prev(verbose=False)
        self.assertEqual(dev.current_tweet_id == -1, True)
        self.assertEqual(dev.current_tweet=={}, True)
        
        #test pred_prev when we selected the first tweet(we stay on the current tweet)
        
        reset()
        dev.read_tweet(1,verbose=False)
        dev.read_prev(verbose=False)
        self.assertEqual(dev.current_tweet_id, 0)
        self.assertEqual(dev.current_tweet!={},True)
        
        #test read_prev for a random tweet that exists
        
        reset()
        dev.read_tweet(25674,verbose=False)
        dev.read_prev(verbose=False)
        self.assertEqual(dev.current_tweet_id==25672,True)
        self.assertEqual(dev.current_tweet!={},True)

    def test_readNext(self):
        
        #reset and test read_next when we havent selected a tweet
        
        reset()
        dev.read_next(verbose=False)
        self.assertEqual(dev.current_tweet_id == -1, True)
        self.assertEqual(dev.current_tweet=={}, True)
        
        #test read_next when we have selected the first tweet
        
        reset()
        dev.read_tweet(1,verbose=False)
        dev.read_next(verbose=False)
        self.assertEqual(dev.current_tweet_id,1)
        self.assertEqual(dev.current_tweet!={},True)
        
        #test read_next when we have selected a random tweet that exists
        
        reset()
        dev.read_tweet(25674,verbose=False)
        dev.read_next(verbose=False)
        self.assertEqual(dev.current_tweet_id==25674,True)
        self.assertEqual(dev.current_tweet!={},True)

        #test read_next when we have selected the last tweet(we stay on the current tweet)
        
        reset()
        dev.read_tweet(len(dev.mem_tweets) , verbose=False)
        dev.read_next(verbose=False)
        self.assertEqual(dev.current_tweet_id, len(dev.mem_tweets) - 1)   
        self.assertEqual(dev.current_tweet!={}, True)

        

    def test_print(self):
        dev.print_current(verbose=False)
        self.assertEqual(dev.current_tweet_id, -1)
        self.assertEqual(dev.current_tweet=={},True)
        dev.read_tweet(1, verbose=False)
        self.assertEqual(dev.current_tweet_id!= -1,True)
        self.assertEqual(dev.current_tweet!= {}, True)

    
    def test_save(self):
        
        # assume everything is transfered correctly into memory


        # change something
        dev.create_tweet(prompt=False, ttext="foo", verbose=False)
        dev.update_tweet(len(dev.mem_tweets), prompt=False, ttext="foo x2", verbose=False)
        dev.delete_tweet(verbose=False)

        # save to the file
        dev.save(verbose=False)

        # check if file is written correctly

        with open(dev.file_name, "r") as file:
            for i, line in enumerate(file):
                dev.read_tweet(i+1, prompt=False, verbose=False)
                self.assertEqual(dev.current_tweet == json.loads(line.replace('\n', '')), True)
                self.assertEqual(dev.current_tweet_id==i, True)
        



    def test_readL(self):
        dev.read_Ltweet(verbose=False)
        self.assertEqual(len(dev.mem_tweets)-1==dev.current_tweet_id,True)
        self.assertEqual(dev.current_tweet!={},True)
        

        # Testing case of empty tweet lists.
        # Tweet list will be set to empty. This is the last test
        reset()
        #dev.mem_tweets.clear()
        #dev.read_Ltweet(verbose=False)
        #self.assertEqual(dev.current_tweet_id == -1, True)
        #self.assertEqual(dev.current_tweet == {}, True)

    
    def test_deleteIfEmpty(self):
        dev.delete_tweet(verbose=False)

        #dev.mem_tweets.clear()
        #self.assertEqual(dev.mem_tweets==[], True)
        #self.assertEqual(dev.current_tweet=={}, True)
        #self.assertEqual(dev.current_tweet_id == -1, True)























#
#class ProfTest(unittest.TestCase):
#    pass
#
#class LogTest(unittest.TestCase):
#    pass
#
#class RefTest(unittest.TestCase):
#    pass
#
#
if __name__ == "__main__":
    unittest.main()