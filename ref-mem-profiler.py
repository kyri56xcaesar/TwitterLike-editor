from datetime import datetime, date, time, timezone
import time
import json
import sys
import random
from memory_profiler import profile


SHELL_S = "#_> "

FILE_NAME = "tweetdhead300000.json"
#FILE_NAME = "test.json"
FD = None

s_commands = ['c', 'r', 'u', 'd', '$', '-', '+', '=', 'q', 'w', 'x', 'h']

CURRENT_TWEET = dict()
CURRENT_TWEET_ID = -1

MEM_TWEETS = list()

##############################################################################################
@profile
def configureID():
    global MEM_TWEETS
    global FD

    try:
        FD = open(FILE_NAME, "rb")
          
        MEM_TWEETS = [json.loads(tweet) for tweet in FD if tweet != ""]

    except(FileExistsError, json.JSONDecodeError):
        print(f"Something went wrong with {FILE_NAME}. Try again.\n\nExiting...")
        sys.exit(-1)

################################################
@profile
def create_tweet(prompt=False, ttext="", verbose=True):

    global CURRENT_TWEET
    global CURRENT_TWEET_ID

    if verbose:
        print("Creating a tweet...")

    if prompt:
        ttext = input("Enter text: ")

    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year

    new_tweet = {"text": ttext, "created_at": tdate}
    
    CURRENT_TWEET = new_tweet

    if MEM_TWEETS and MEM_TWEETS[-1] == "":
        MEM_TWEETS[-1] = CURRENT_TWEET
    else:
        MEM_TWEETS.append(CURRENT_TWEET)
    
    CURRENT_TWEET_ID = len(MEM_TWEETS) - 1
    
    return tdate
##################################################
@profile
def read_tweet(number, prompt=False, verbose=True):

    if number < 0:
        print("Invalid tweet ID")
        return False

    global CURRENT_TWEET_ID
    global CURRENT_TWEET

    if prompt:
        number = input("Enter the ID of the tweet you want to read: ")
        if number.isnumeric() == False:
            return False
        number = int(number)
    
    if number < 1 or number > len(list(MEM_TWEETS)):
        if verbose:
            print("Invalid tweet ID")
        return False

    
    CURRENT_TWEET_ID = number - 1

    CURRENT_TWEET = MEM_TWEETS[CURRENT_TWEET_ID]

    if verbose:
        print(f"Reading tweet: {CURRENT_TWEET_ID + 1} ...")

    return True
##################################################
@profile
def update_tweet(number, tprompt=False,
vprompt=False, ttext="", verbose=True):

    global CURRENT_TWEET
    global CURRENT_TWEET_ID

    if read_tweet(number, prompt=vprompt, verbose=verbose) == False:
        return None
    if tprompt:
        ttext = input("Enter text: ")

    if verbose:
        print("Updating tweet...")

    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   
    
    CURRENT_TWEET.update({"text":ttext})
    CURRENT_TWEET.update({"created_at":tdate})

    return tdate
##################################################
@profile
def delete_tweet(verbose=True):

    global CURRENT_TWEET_ID
    global CURRENT_TWEET

    if CURRENT_TWEET_ID == -1:
        if verbose:
            print("There is no tweet selected currently")
        return False

    if verbose:
        print("Deleting a tweet...")

    ## UPDATE TWEET TABLE
    MEM_TWEETS.remove(MEM_TWEETS[CURRENT_TWEET_ID])
    
  
    CURRENT_TWEET_ID = -1
    CURRENT_TWEET = {}

    return True
##################################################
@profile
def read_Ltweet(verbose=True):
 
    if MEM_TWEETS == []:
        if verbose:
            print("Somehow you've deleted all the tweets<?. No tweets left to read.")
        return False

    if verbose:
        print("Reading last tweet...")
    
    global CURRENT_TWEET_ID
    global CURRENT_TWEET

    CURRENT_TWEET_ID = len(MEM_TWEETS) - 1

    CURRENT_TWEET = MEM_TWEETS[-1]

    return True
##################################################
@profile
def read_prev(verbose=True):

    global CURRENT_TWEET_ID

    if CURRENT_TWEET_ID == -1:
        if verbose:
            print("There is no tweet selected currently.")
        return False

    if CURRENT_TWEET_ID == 0:
        if verbose:
            print("Can't do that.")    
        return False

    if verbose:
        print("Going up...")

    read_tweet(CURRENT_TWEET_ID, verbose=verbose)

    return True
##################################################
@profile
def read_next(verbose=True):
    
    global CURRENT_TWEET_ID

    if CURRENT_TWEET_ID == -1:
        if verbose:
            print("There is no tweet selected currently.")
        return False
    
    if CURRENT_TWEET_ID == len(MEM_TWEETS) - 1:
        if verbose:
            print("Can't do that.")
        return False

    if verbose:
        print("Going down...")

    read_tweet(CURRENT_TWEET_ID+2, verbose=verbose)

    return True
##################################################
@profile
def print_current(prompt=False, verbose=True):

    if CURRENT_TWEET_ID == -1 or CURRENT_TWEET == {}:
        if verbose:
            print("No tweet selected.")
        return

    if verbose:
        print("Printing current:")
        print(f"Current tweet ID: {CURRENT_TWEET_ID+1}")

    if prompt:
        toPrint = input("Print the whole tweet? [y]")
        if toPrint.capitalize() == 'Y' or toPrint == "":
            print(CURRENT_TWEET)
    else:
        print("\t", end="")
        print(CURRENT_TWEET)
##################################################
@profile
def save(verbose=True):
    if verbose:
        print("Saving contents...")
    time.sleep(0.3)

    try:
        with open(FILE_NAME, "w") as file:
            for line in MEM_TWEETS:
                json.dump(line, file)
                file.write("\n")
    except (Exception):
        print("Something may have gone catastrophically bad.")
        raise Exception

    if verbose:
        print("\n\nContents saved!")
    


""" Main method """
if __name__ == "__main__":

    configureID()
    i=random.randint(0,20)
    read_tweet(i,prompt=False, verbose=False)
 
    create_tweet(prompt=False, ttext=f"test {i}", verbose=False)   
    update_tweet(len(MEM_TWEETS),tprompt=False, vprompt=False,ttext=f"test_v{352352/53252}", verbose=False)
    
    print_current(prompt=False, verbose=False)  
    delete_tweet(verbose=False)
    
    save(verbose=False)
        