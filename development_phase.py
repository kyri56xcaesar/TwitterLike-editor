from datetime import datetime, date, time, timezone
import time
import json
import os
import ast
from line_profiler import LineProfiler
import random
# Name of the file used
file_name = "tweetdhead300000.json"

# list of commands available
s_commands = ['c', 'r', 'u', 'd', '$', '-', '+', '=', 'q', 'w', 'h']

    
# Tweets ID array/list record
t_ID = []
# Current tweet selected (as string)
current_tweet = ""
# Current tweet ID selected
current_tweet_id = -1

# number prompted when reading or updating a tweet
number = 'foo'



# Memory tweets
mem_tweets = []
# Tasks to do in order to save
tasks = []


# --- Setup method.
# Initialize the t_ID list with the index/number of each line
# Consider starting from 1. As the first tweet is ID is 1.
def configureID():
     with open(file_name, "rb") as file:

        for i, line in enumerate(file):
            t_ID.append(i)

# --- Helper method/
# Help message showing available options in case of invalid input.
def help():
    print("Options: \n\
        \t c :> Create a tweet.\n\
        \t r <number> :> Read a tweet of the given number.\n\
        \t u <number> :> Update a tweet of the given number.\n\
        \t d :> Delete the current tweet.\n\
        \t $ :> Read the last existing tweet.\n\
        \t - :> Navigate to previous tweet.\n\
        \t + :> Navigate to next tweet.\n\
        \t = :> Print current tweet.\n\
        \t q :> Quit without save.\n\
        \t w :> Save and write to disk.\n\
        \t x :> Exit and save.\n")

def print_table(f, to):

    for i in range(to - f):
        if f + i < len(t_ID):
            print(t_ID[f + i])

# Create a tweet function handler.      --> DONE
def create_tweet():

    global current_tweet
    global current_tweet_id

    print("Creating a tweet...")

    # text
    ttext = input("Enter text: ")

    # created at
    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year
    print(tdate)

    # Create a new JSON tweet
    new_tweet = json.dumps({'text': ttext,'created at':tdate})
    
    # Schedule a task
    tasks.append(({"n":new_tweet}, current_tweet_id))

    # Set this new tweet as the current tweet 
    if t_ID != []:
        current_tweet_id = int(t_ID[-1]) + 1
    else:
        current_tweet_id = 0
    # Set the new current_tweet
    current_tweet = new_tweet
    
    # Update the tweetID list
    t_ID.append(current_tweet_id)
    


    
# Read a tweet function handler.  --> DONE
# Returns True if it reads False if not.
def read_tweet(number, prompt=False):

    if number < 0:
        print("Invalid tweet ID")
        return

    global current_tweet_id
    global current_tweet

    # Must get a number
    if prompt:
        number = input("Enter the ID of the tweet you want to read: ")
        if number.isnumeric() == False:
            return False
        number = int(number)
    
    # Check if number is valid
    if number < 1 or number > len(t_ID):
        print("Invalid tweet ID")
        return False

    print("Reading a tweet...")
    current_tweet_id = number - 1


    #number = t_ID[current_tweet_id]

    # Find the corresponding tweet
    with open(file_name, "r") as rfile:
        for i, line in enumerate(rfile):
            if i == current_tweet_id:
                current_tweet=line
                break

    print("Current tID: " + str(current_tweet_id))
    return True
    
# Update a tweet function handler.   --> TODO
def update_tweet(number, prompt=False):

    global current_tweet
    global current_tweet_id

    # Read the tweet first. Set it as current and adjust id index via method @read_tweet
    if read_tweet(number, prompt) == False:
        return
    # Get the new text input
    new_text = input("Enter text: ")

    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year
    
    # Update the tweet
    # create a dictionary out of the tweet
    current_tweet = json.loads(current_tweet)
    current_tweet.update({"text":new_text})
    current_tweet.update({"created_at":tdate})
    current_tweet = '{"'+str(list(current_tweet.keys())[0])+'": "'+current_tweet.get("text")+'", "'+str(list(current_tweet.keys())[1])+'": "'+current_tweet.get("created_at")+'"}\n'
   

    # for improvement.
    # save in memory
    #mem_tweets.append({current_tweet_id:current_tweet})
    

    # Schedule task
    tasks.append(({"u":current_tweet}, current_tweet_id))

    
    
# Delete a tweet function handler. --> TODO
def delete_tweet():


    global current_tweet_id
    global current_tweet

    if current_tweet_id == -1:
        print("There is no tweet selected currently")
        return

    print("Deleting a tweet...")


    # Tasking IMPROVEMENT
    tasks.append(({"d":current_tweet}, current_tweet_id))

    ## UPDATE TWEET TABLE
    t_ID.remove(t_ID[current_tweet_id])
    
  
    current_tweet_id = -1
    current_tweet = ""

    
    
# Read the Last tweet of the tweet function handler --> DONE
def read_Ltweet():
 
    if t_ID == None:
        print("Somehow you've deleted all the tweets<?. No tweets left to read.")
        return

    print("Reading last tweet...\n")
    
    global current_tweet_id
    global current_tweet

    # Get the last tweet
    current_tweet_id = t_ID[-1]
    #print("Current tID is: " + str(current_tweet_id))

    
    
    with open(file_name, "rb") as file:

        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        
        current_tweet=file.readline().decode()
    
    
# Head the tweet id index - 1 ---> DONE
def read_prev():
    global current_tweet_id


    if current_tweet_id == -1:
        print("There is no tweet selected currently.")
        return

    if current_tweet_id == 0:
        print("Can't do that.")
      
        return
    print("Going up...\n\n")

    
    read_tweet(current_tweet_id)
    

# Head the tweet id index + 1 ---> DONE
def read_next():
    global current_tweet_id

    if current_tweet_id == -1:
        print("There is no tweet selected currently.")
        return


    
    if current_tweet_id == len(t_ID) - 1:
        print("Can't do that.")
        return

    print("Going down...\n\n")

    read_tweet(current_tweet_id+2)



# Print the curret_tweet --> DONE
def print_current(prompt=False):

    if current_tweet_id == -1 or current_tweet == "":
        print("No tweet selected.")
        return

    print("\nPrinting current:\n")
    print(f"Current tweet ID: {current_tweet_id}")

    if prompt:
        toPrint = input("Print the whole tweet? [y]")
        if toPrint.capitalize() == 'Y' or toPrint == "":
            print(current_tweet)
    else:
        print(current_tweet)
    
## QUIT method      ---> DONE
def quit(toSave=False):
    print("Quiting...")

    if toSave:
        save_prompt = input("\n*WARNING*\nContents will not be saved. Would you like to save them [Y]? ")
        if save_prompt.upper() == "Y":
            save()
    exit()
    
## SAVE method - Overwrites the file --> TODO
def save():
    print("\n\nSaving contents...")
    time.sleep(0.3)

    print("\n\nContents saved!")
    
# task structure : ({whatToDo, tweet}, tId)
def task_handler():


    while tasks != []:
        task = tasks.pop()
        if list(task[0].keys())[0] == "n":
            with open(file_name, "a") as file:
                try:
                    print(file.tell())
                    file.seek(0, 2)
                    print(file.tell())
                    if file.tell() != 0:
                        file.write("\n")
                    print(task[0].get("n"))
                    file.write(task[0].get("n"))
                    #json.dump(task[0].get("n"), file, indent=0)
                except OSError:
                    print("error")
                    file.seek(0)
        
     
     
        if list(task[0].keys())[0] == "d":
            lines = []
            # delete the tweet from the file
            with open(file_name, "r") as fp:
                lines = fp.readlines()

            with open(file_name, "w") as fp:
                for number, line in enumerate(lines):
                    if number != task[1]:
                        fp.write(line)
     
            
        if list(task[0].keys())[0] == "u":

            lines = []
            # read all the lines
            with open(file_name, "r") as fp:
                lines = fp.readlines()

            # rewrite all the lines but with the updated ones
            with open(file_name, "w") as fp:
                for number, line in enumerate(lines):
                    if number == current_tweet_id:
                        fp.write(current_tweet)
                    else:
                        fp.write(line)

                
        
        


if __name__ == "__main__":


    configureID()
    i=random.randint(0, 100)
    n = 100
    lp = LineProfiler()
    lp_wrapper = lp(read_tweet)
    lp_wrapper(n)
    print("Line Profiler For Read Tweet")
    
    
    lp_wrapper = lp(task_handler)
    lp_wrapper()
    print("Line Profiler For Reading Task")
    

    lp_wrapper = lp(delete_tweet)
    lp_wrapper()
    print("Line Profiler For delete Tweet")
    
    
    lp_wrapper = lp(task_handler)
    lp_wrapper()
    print("Line Profiler For Deleting Task")
    lp.print_stats()