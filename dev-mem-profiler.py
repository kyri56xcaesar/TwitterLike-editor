from datetime import datetime, date, time, timezone
import time
import json
import random
from memory_profiler import profile


#file_name = "test.json"
file_name = "tweetdhead300000.json"

s_commands = ['c', 'r', 'u', 'd', '$', '-', '+', '=', 'q', 'w', 'h']

current_tweet = {}
current_tweet_id = -1

mem_tweets = []

@profile
def configureID():
    global mem_tweets

    try:
        with open(file_name, "rb") as file:

            for line in file:
                mem_tweets.append(json.loads(line))
    except FileNotFoundError:
        print(f"File named: {file_name} not found.")   
        print("Exiting...\n\n")

        exit()
###################################################
@profile
def create_tweet(tprompt=False, ttext="", verbose=False):

    global current_tweet
    global current_tweet_id

    if verbose:
        print("Creating a tweet...")
    if tprompt:
        ttext = input("Enter text: ")
    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y') 

    new_tweet = {"text": ttext, "created_at": tdate}

    current_tweet = new_tweet

    if mem_tweets != [] and mem_tweets[-1] == "":
        mem_tweets[-1] = current_tweet
    else:
        mem_tweets.append(current_tweet)

    current_tweet_id = len(mem_tweets) - 1
    
    return tdate
##################################################
@profile
def read_tweet(number, prompt=False, verbose=False):


    if number < 0:
        print("Invalid tweet ID")
        return

    global current_tweet_id
    global current_tweet

    if prompt:
        number = input("Enter the ID of the tweet you want to read: ")
        if number.isnumeric() == False:
            return False
        number = int(number)
    
    if number < 1 or number > len(mem_tweets):
        if verbose:
            print("Invalid tweet ID")
        return False

    if verbose:
        print("Reading a tweet...")
    current_tweet_id = number - 1

    current_tweet = mem_tweets[current_tweet_id]

    return True
#############################################
@profile
def update_tweet(number, vprompt=False, tprompt=True, ttext="", verbose=False):

    global current_tweet
    global current_tweet_id

    if read_tweet(number, prompt=vprompt, verbose=verbose) == False:
        return
    if tprompt:
        ttext = input("Enter text: ")

    if verbose:
        print("Updating tweet...")

    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   
    
    current_tweet.update({"text":ttext})
    current_tweet.update({"created_at":tdate})

    return tdate
####################################################
@profile
def delete_tweet(verbose=False):


    global current_tweet_id
    global current_tweet

    if current_tweet_id == -1:
        if verbose:
            print("There is no tweet selected currently")
        return

    if verbose:
        print("Deleting a tweet...")

    mem_tweets.remove(mem_tweets[current_tweet_id])
    
  
    current_tweet_id = -1
    current_tweet = {}

    return current_tweet=={}
###################################################   
@profile
def read_Ltweet(verbose=False):
 
    if mem_tweets == []:
        if verbose:
            print("Somehow you've deleted all the tweets<?. No tweets left to read.")
        return

    if verbose:
        print("Reading last tweet...")
    
    global current_tweet_id
    global current_tweet

    current_tweet_id = len(mem_tweets) - 1

    current_tweet = mem_tweets[-1]
###################################################   
@profile
def read_prev(verbose=False):
    global current_tweet_id


    if current_tweet_id == -1:
        if verbose:
            print("There is no tweet selected currently.")
        return

    if current_tweet_id == 0:
        if verbose:
            print("Can't do that.")
      
        return
    if verbose:
        print("Going up...")

    
    read_tweet(current_tweet_id, prompt=False, verbose=verbose)
##################################################    
@profile
def read_next(verbose=False):
    global current_tweet_id

    if current_tweet_id == -1:
        if verbose:
            print("There is no tweet selected currently.")
        return
    
    if current_tweet_id == len(mem_tweets) - 1:
        if verbose:
            print("Can't do that.")
        return

    if verbose:
        print("Going down...")

    read_tweet(current_tweet_id+2, prompt=False, verbose=verbose)
##################################################
@profile
def print_current(prompt=False, verbose=False):

    if current_tweet_id == -1 or current_tweet == {}:
        if verbose:
            print("No tweet selected.")
        return

    if verbose:
        print("Printing current:")
        print(f"Current tweet ID: {current_tweet_id+1}")

    if prompt:
        toPrint = input("Print the whole tweet? [y]")
        if toPrint.capitalize() == 'Y' or toPrint == "":
            print(current_tweet)
    else:
        print("\t", end="")
        print(current_tweet)
##################################################    
@profile
def save(verbose=False):
    if verbose:
        print("Saving contents...")
    time.sleep(0.3)

    with open(file_name, "w") as file:
        for line in mem_tweets:
            json.dump(line, file)
            file.write("\n")
       
    if verbose:
        print("\n\nContents saved!")

    



if __name__ == "__main__":

    configureID()
    i=random.randint(0,20)
    read_tweet(i,prompt=False, verbose=False)
 
    create_tweet(prompt=False, ttext=f"test {i}", verbose=False)   
    update_tweet(len(mem_tweets),tprompt=False, vprompt=False,ttext=f"test_v{352352/53252}", verbose=False)
    
    print_current(prompt=False, verbose=False)  
    delete_tweet(verbose=False)
    
    save(verbose=False)