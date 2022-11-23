import unittest
import development_phase as dev
import json

t_list_copy = []

def reset():
    dev.current_tweet = {}
    dev.current_tweet_id = -1

def reboot():
    dev.mem_tweets = t_list_copy.copy()

class DevTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        global t_list_copy
        super(DevTest, cls).setUpClass()
        #reset()
        dev.configureID()
        t_list_copy = dev.mem_tweets.copy()
        


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
        # read a large tweet ( must exist )
        dev.read_tweet(25674, verbose=False)
        if len(dev.mem_tweets) > 25674:
            self.assertEqual(dev.current_tweet_id == 25674, False)
            self.assertEqual(dev.current_tweet=={}, False)

        # reset
        reset()
        dev.read_tweet(len(dev.mem_tweets) + 1, verbose=False)
        self.assertEqual(dev.current_tweet_id, -1)   
        self.assertEqual(dev.current_tweet=={}, True)


        # read a new tweet
        dev.create_tweet(prompt=False, ttext="new_tweet", verbose=False)
        dev.read_tweet(len(dev.mem_tweets),prompt=False, verbose=False)
        self.assertEqual(dev.current_tweet.get("text"), "new_tweet")

        # read an updated tweet
        dev.update_tweet(1, prompt=False, ttext="updated_tweet", verbose=False)
        reset()
        dev.read_tweet(1, prompt=False, verbose=False)
        self.assertEqual(dev.current_tweet.get("text"), "updated_tweet")

        # read upon a deletion (shift of position) # MUST EXIST
        dev.read_tweet(2, prompt=False, verbose=False)
        temp = dev.current_tweet
        if dev.current_tweet_id != -1:
            # delete the first tweet
            dev.read_tweet(1, prompt=False, verbose=False)
            dev.delete_tweet(verbose=False)

            # check if previously read second tweet is now first
            dev.read_tweet(1, prompt=False, verbose=False)
            self.assertEqual(dev.current_tweet, temp)
        




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
        
        # test update on an existing tweet
        reset()
        reboot()
        time = dev.update_tweet(5, prompt=False, ttext="test", verbose=False)

        if dev.current_tweet_id != -1:
            # test if new text is set correctly
            self.assertEqual(dev.current_tweet.get("text"), "test")

            # test if time is set correctly
            self.assertEqual(dev.current_tweet.get("created_at")==time, True)

            # test if current id is at the correct place
            self.assertEqual(dev.current_tweet_id == 4, True)

        #############
        # Case when updating an invalid tweet number
        dev.update_tweet(0, prompt=False, ttext="test2", verbose=False)
        
        if dev.current_tweet_id != -1:
            self.assertEqual(dev.current_tweet_id, 4)


        # go to 5
        dev.read_tweet(5, verbose=False, prompt=False)
        # test back and forth steadiness
        # must not be last or first
        if  dev.current_tweet_id != -1 and dev.current_tweet_id != 0 and dev.current_tweet != len(dev.mem_tweets):
            dev.read_prev(verbose=False)
            dev.read_next(verbose=False)
            self.assertEqual(dev.current_tweet_id, 4)
 
            dev.read_next(verbose=False)
            dev.read_prev(verbose=False)
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
        if dev.current_tweet_id != -1:
            self.assertEqual(dev.current_tweet_id==25672,True)
            self.assertEqual(dev.current_tweet!={},True)


        # test read_prev if a tweet is deleted
        reset()
        dev.read_tweet(3, verbose=False) # hold in memory the third tweet.
        temp = dev.current_tweet
        dev.read_tweet(2, verbose=False) # read the second and delete it
        if dev.current_tweet_id != -1: 
            dev.delete_tweet(verbose=False)
        
        dev.read_tweet(2, verbose=False) # read the new second and ensure its now the third
        self.assertEqual(temp, dev.current_tweet)

        # test back and forth feature on an updated tweet
        reset()
        dev.read_tweet(2, verbose=False)
        temp = dev.current_tweet
        dev.update_tweet(2, ttext="updated test")
        dev.read_next(verbose=False)
        dev.read_prev(verbose=False)
        self.assertEqual(dev.current_tweet.get("text"), "updated test")


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
        if dev.current_tweet_id != -1:
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

    
    #def test_save(self):
    #    
    #    # assume everything is transfered correctly into memory
    #
    #
    #    # change something
    #    dev.create_tweet(prompt=False, ttext="foo", verbose=False)
    #    dev.update_tweet(len(dev.mem_tweets), prompt=False, ttext="foo x2", verbose=False)
    #    dev.delete_tweet(verbose=False)
    #
    #    # save to the file
    #    dev.save(verbose=False)
    #
    #    # check if file is written correctly
    #
    #    with open(dev.file_name, "r") as file:
    #        for i, line in enumerate(file):
    #            dev.read_tweet(i+1, prompt=False, verbose=False)
    #            self.assertEqual(dev.current_tweet == json.loads(line.replace('\n', '')), True)
    #            self.assertEqual(dev.current_tweet_id==i, True)
    #    
    #
    #

    def test_readL(self):
        dev.read_Ltweet(verbose=False)
        self.assertEqual(len(dev.mem_tweets)-1==dev.current_tweet_id,True)
        temp = dev.current_tweet
        self.assertEqual(dev.current_tweet!={},True)
        
        # Create a new tweet.
        # Check if its the last.
        dev.create_tweet(prompt=False, ttext="test1", verbose=False)
        dev.read_Ltweet(verbose=False)
        temp2 = dev.current_tweet
        self.assertEqual(dev.current_tweet.get("text"), "test1")

        # Update the new tweet. 
        # Check if its still last
        dev.update_tweet(dev.current_tweet_id + 1, prompt=False, ttext="test1.1", verbose=False)
        self.assertEqual(dev.current_tweet.get("text"), "test1.1")


        # Delete the tweet.
        # Check if the last tweet is correct
        dev.delete_tweet(verbose=False)
        dev.read_Ltweet(verbose=False)
        self.assertEqual(dev.current_tweet, temp)
    
    def test_deleteIfEmpty(self):
        dev.delete_tweet(verbose=False)

        #dev.mem_tweets.clear()
        #self.assertEqual(dev.mem_tweets==[], True)
        #self.assertEqual(dev.current_tweet=={}, True)
        #self.assertEqual(dev.current_tweet_id == -1, True)







if __name__ == "__main__":
    unittest.main()