import unittest
import development_phase as dev

def reset():
    dev.current_tweet = ""
    dev.current_tweet_id = -1

class DevTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(DevTest, cls).setUpClass()
        #reset()
        dev.configureID()
        


    def test_read(self):

        # Test invalid id case
        dev.read_tweet(0, verbose=False)
        self.assertEqual(dev.current_tweet_id, -1) # current id must be -1
        # current tweet must be None
        self.assertEqual(dev.current_tweet=="", True)
        

        dev.read_tweet(1, verbose=False)
        self.assertEqual(dev.current_tweet_id == 0, True)
        self.assertEqual(dev.current_tweet!="", True)
        
        # reset current_tweet and current tweet id
        reset()
        dev.read_tweet(25674, verbose=False)
        self.assertEqual(dev.current_tweet_id == 25674, False)
        self.assertEqual(dev.current_tweet=="", False)

        # reset
        reset()
        dev.read_tweet(len(dev.mem_tweets) + 1, verbose=False)
        self.assertEqual(dev.current_tweet_id, -1)   
        self.assertEqual(dev.current_tweet=="", True)
        




    def test_create(self):
        pass

    def test_update(self):
        pass

 

    def test_delete(self):
        pass

    def test_readL(self):
        pass

    def test_readPrev(self):
        pass

    def test_readNext(self):
        pass

    def test_print(self):
        pass
    
    def test_save(self):
        pass

    pass


























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