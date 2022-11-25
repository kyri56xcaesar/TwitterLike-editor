import unittest
import refactoring as ref
import json

t_list_copy = []

def reset():
    ref.CURRENT_TWEET = {}
    ref.CURRENT_TWEET_ID = -1

def reboot():
    ref.MEM_TWEETS = t_list_copy.copy()

class DevTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        global t_list_copy
        super(DevTest, cls).setUpClass()
        #reset()
        ref.configureID()
        t_list_copy = ref.MEM_TWEETS.copy()
        


    def test_read(self):

        reset()

        # Test invalid id case
        ref.read_tweet(number=0, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID, -1) # current id must be -1
        # current tweet must be None
        self.assertEqual(ref.CURRENT_TWEET=={}, True)
        

        ref.read_tweet(number=1, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID == 0, True)
        self.assertEqual(ref.CURRENT_TWEET!={}, True)
        
        # reset CURRENT_TWEET and current tweet id
        reset()
        # read a large tweet ( must exist )
        ref.read_tweet(number=25674, verbose=False)
        if len(ref.MEM_TWEETS) > 25674:
            self.assertEqual(ref.CURRENT_TWEET_ID == 25674, False)
            self.assertEqual(ref.CURRENT_TWEET=={}, False)

        # reset
        reset()
        ref.read_tweet(len(ref.MEM_TWEETS) + 1, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID, -1)   
        self.assertEqual(ref.CURRENT_TWEET=={}, True)


        # read a new tweet
        ref.create_tweet(tprompt=False, ttext="new_tweet", verbose=False)
        ref.read_tweet(len(ref.MEM_TWEETS),prompt=False, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET.get("text"), "new_tweet")

        # read an updated tweet
        ref.update_tweet(number=1, tprompt=False, ttext="updated_tweet", verbose=False)
        reset()
        ref.read_tweet(1, prompt=False, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET.get("text"), "updated_tweet")

        # read upon a deletion (shift of position) # MUST EXIST
        ref.read_tweet(2, prompt=False, verbose=False)
        temp = ref.CURRENT_TWEET
        if ref.CURRENT_TWEET_ID != -1:
            # delete the first tweet
            ref.read_tweet(1, prompt=False, verbose=False)
            ref.delete_tweet(verbose=False)

            # check if previously read second tweet is now first
            ref.read_tweet(1, prompt=False, verbose=False)
            self.assertEqual(ref.CURRENT_TWEET, temp)
        




    def test_create(self):
        reset()
        time = ref.create_tweet(tprompt=False, ttext="test", verbose=False)

        # test if a tweet is created
        self.assertEqual(ref.CURRENT_TWEET.get("text")=="test", True)

        # test if time-date is correct
        self.assertEqual(ref.CURRENT_TWEET.get("created_at")==time, True)

        # test if CURRENT_TWEET is set correctly to the end of the list

        self.assertEqual(ref.CURRENT_TWEET_ID == len(ref.MEM_TWEETS) - 1, True)
        


    def test_update(self):
        
        # test update on an existing tweet
        reset()
        reboot()
        time = ref.update_tweet(number=5, tprompt=False, ttext="test", verbose=False)

        if ref.CURRENT_TWEET_ID != -1:
            # test if new text is set correctly
            self.assertEqual(ref.CURRENT_TWEET.get("text"), "test")

            # test if time is set correctly
            self.assertEqual(ref.CURRENT_TWEET.get("created_at")==time, True)

            # test if current id is at the correct place
            self.assertEqual(ref.CURRENT_TWEET_ID == 4, True)

        #############
        # Case when updating an invalid tweet number
        ref.update_tweet(number=0, tprompt=False, ttext="test2", verbose=False)
        
        if ref.CURRENT_TWEET_ID != -1:
            self.assertEqual(ref.CURRENT_TWEET_ID, 4)


        # go to 5
        ref.read_tweet(5, verbose=False, prompt=False)
        # test back and forth steadiness
        # must not be last or first
        if  ref.CURRENT_TWEET_ID != -1 and ref.CURRENT_TWEET_ID != 0 and ref.CURRENT_TWEET != len(ref.MEM_TWEETS):
            ref.read_prev(verbose=False)
            ref.read_next(verbose=False)
            self.assertEqual(ref.CURRENT_TWEET_ID, 4)
 
            ref.read_next(verbose=False)
            ref.read_prev(verbose=False)
            self.assertEqual(ref.CURRENT_TWEET_ID, 4)

    def test_delete(self):

        reset()

        # test delete if no tweet is selected
        ref.delete_tweet(verbose=False)

        # must check if everything is at the same place
        for id, tweet in enumerate(ref.MEM_TWEETS):
            ref.read_tweet(id + 1, prompt=False, verbose=False)
            self.assertEqual(ref.CURRENT_TWEET_ID == id, True)
            self.assertEqual(ref.CURRENT_TWEET != {}, True)

        # test delete if tweet is selected
        reset()
        ref.read_tweet(2, prompt=False, verbose= False)

        # hold 3rd tweet
        ref.read_tweet(3, prompt=False, verbose=False)
        third_t = ref.CURRENT_TWEET
        # go back to second
        ref.read_prev(verbose=False)

        # hold length before
        max_length = len(ref.MEM_TWEETS)

        # delete the second(current)
        ref.delete_tweet(verbose=False)

        # check if the new second tweet is the last third tweet.
        # read the new second
        ref.read_tweet(2, prompt=False, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET == third_t, True)

        # check if length is reduced by 1
        self.assertEqual(len(ref.MEM_TWEETS) == max_length - 1, True)






    def test_readPrev(self):
        
        #reset and test read_prev when we havent selected a tweet   
        reset()
        ref.read_prev(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID == -1, True)
        self.assertEqual(ref.CURRENT_TWEET=={}, True)
        
        #test pred_prev when we selected the first tweet(we stay on the current tweet)        
        reset()
        ref.read_tweet(1,verbose=False)
        ref.read_prev(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID, 0)
        self.assertEqual(ref.CURRENT_TWEET!={},True)
        
        #test read_prev for a random tweet that exists   
        reset()
        ref.read_tweet(25674,verbose=False)
        ref.read_prev(verbose=False)
        if ref.CURRENT_TWEET_ID != -1:
            self.assertEqual(ref.CURRENT_TWEET_ID==25672,True)
            self.assertEqual(ref.CURRENT_TWEET!={},True)


        # test read_prev if a tweet is deleted
        reset()
        ref.read_tweet(3, verbose=False) # hold in memory the third tweet.
        temp = ref.CURRENT_TWEET
        ref.read_tweet(2, verbose=False) # read the second and delete it
        if ref.CURRENT_TWEET_ID != -1: 
            ref.delete_tweet(verbose=False)
        
        ref.read_tweet(2, verbose=False) # read the new second and ensure its now the third
        self.assertEqual(temp, ref.CURRENT_TWEET)

        # test back and forth feature on an updated tweet
        reset()
        ref.read_tweet(2, verbose=False)
        temp = ref.CURRENT_TWEET
        ref.update_tweet(number=2, tprompt=False, ttext="updated test")
        ref.read_next(verbose=False)
        ref.read_prev(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET.get("text"), "updated test")


    def test_readNext(self):
        
        #reset and test read_next when we havent selected a tweet
        
        reset()
        ref.read_next(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID == -1, True)
        self.assertEqual(ref.CURRENT_TWEET=={}, True)
        
        #test read_next when we have selected the first tweet
        
        reset()
        ref.read_tweet(1,verbose=False)
        ref.read_next(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID,1)
        self.assertEqual(ref.CURRENT_TWEET!={},True)
        
        #test read_next when we have selected a random tweet that exists
        
        reset()
        ref.read_tweet(25674,verbose=False)
        ref.read_next(verbose=False)
        if ref.CURRENT_TWEET_ID != -1:
            self.assertEqual(ref.CURRENT_TWEET_ID==25674,True)
            self.assertEqual(ref.CURRENT_TWEET!={},True)

        #test read_next when we have selected the last tweet(we stay on the current tweet)
        
        reset()
        ref.read_tweet(len(ref.MEM_TWEETS) , verbose=False)
        ref.read_next(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID, len(ref.MEM_TWEETS) - 1)   
        self.assertEqual(ref.CURRENT_TWEET!={}, True)

        

    def test_print(self):
        reset()
        ref.print_current(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID, -1)
        self.assertEqual(ref.CURRENT_TWEET=={},True)
        ref.read_tweet(1, verbose=False)
        self.assertEqual(ref.CURRENT_TWEET_ID!= -1,True)
        self.assertEqual(ref.CURRENT_TWEET!= {}, True)

    
    #def test_save(self):
    #    
    #    # assume everything is transfered correctly into memory
    #
    #
    #    # change something
    #    ref.create_tweet(tprompt=False, ttext="foo", verbose=False)
    #    ref.update_tweet(len(ref.MEM_TWEETS), tprompt=False, ttext="foo x2", verbose=False)
    #    ref.delete_tweet(verbose=False)
    #
    #    # save to the file
    #    ref.save(verbose=False)
    #
    #    # check if file is written correctly
    #
    #    with open(ref.file_name, "r") as file:
    #        for i, line in enumerate(file):
    #            ref.read_tweet(i+1, prompt=False, verbose=False)
    #            self.assertEqual(ref.CURRENT_TWEET == json.loads(line.replace('\n', '')), True)
    #            self.assertEqual(ref.CURRENT_TWEET_ID==i, True)
    #    
    #
    #

    def test_readL(self):
        ref.read_Ltweet(verbose=False)
        self.assertEqual(len(ref.MEM_TWEETS)-1==ref.CURRENT_TWEET_ID,True)
        temp = ref.CURRENT_TWEET
        self.assertEqual(ref.CURRENT_TWEET!={},True)
        
        # Create a new tweet.
        # Check if its the last.
        ref.create_tweet(tprompt=False, ttext="test1", verbose=False)
        ref.read_Ltweet(verbose=False)
        temp2 = ref.CURRENT_TWEET
        self.assertEqual(ref.CURRENT_TWEET.get("text"), "test1")

        # Update the new tweet. 
        # Check if its still last
        ref.update_tweet(number=ref.CURRENT_TWEET_ID + 1, tprompt=False, ttext="test1.1", verbose=False)
        self.assertEqual(ref.CURRENT_TWEET.get("text"), "test1.1")


        # Delete the tweet.
        # Check if the last tweet is correct
        ref.delete_tweet(verbose=False)
        ref.read_Ltweet(verbose=False)
        self.assertEqual(ref.CURRENT_TWEET, temp)
    






if __name__ == "__main__":
    unittest.main()