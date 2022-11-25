from datetime import datetime, date, time, timezone
import time
import json
import sys


""" Shell sign """
SHELL_S = "#_> "

""" Name of the file used """
#FILE_NAME = "tweetdhead300000.json"
FILE_NAME = "test.json"
FD = None

""" list of commands available """
s_commands = ['c', 'r', 'u', 'd', '$', '-', '+', '=', 'q', 'w', 'x', 'h']

""" Current tweet selected (as string) """
CURRENT_TWEET = dict()
""" Current tweet ID selected"""
CURRENT_TWEET_ID = -1

""" Memory tweets """
MEM_TWEETS = list()

##############################################################################################

""" --- Setup method.
Initialize the t_ID list with the index/number of each line
Consider starting from 1. As the first tweet is ID is 1
"""
def configureID():
    global MEM_TWEETS
    global FD

    try:
        FD = open(FILE_NAME, "rb")
          
        MEM_TWEETS = [json.loads(tweet) for tweet in FD if tweet != ""]

    except(FileExistsError, json.JSONDecodeError):
        print(f"Something went wrong with {FILE_NAME}. Try again.\n\nExiting...")
        sys.exit(-1)

           

""" --- Helper method/
# Help message showing available options in case of invalid input.
"""
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
        \t w :> Save/write to disk.\n\
        \t x :> Save and exit.\n")


""" Create a tweet function handler. 
@arg prompt: To prompt a user input text
@arg ttext: Text given without user prompt. (Testing purposes)
@arg verbose: Extra info output
"""
def create_tweet(tprompt=False, ttext="", verbose=True):

    global CURRENT_TWEET
    global CURRENT_TWEET_ID

    if verbose:
        print("Creating a tweet...")

    """ Input text from user."""
    if tprompt:
        ttext = input("Enter text: ")

    """ The exact time date this is occuring. """
    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year

    """ Assemble a new tweet as a dictionary. """ 
    new_tweet = {"text": ttext, "created_at": tdate}
    
    """ Set this new tweet to be the current one."""
    CURRENT_TWEET = new_tweet

    """ In case last tweet is an empty string """
    if MEM_TWEETS and MEM_TWEETS[-1] == "":
        MEM_TWEETS[-1] = CURRENT_TWEET
    else:
        """ Simply append/attach the new tweet to the end of the list."""
        MEM_TWEETS.append(CURRENT_TWEET)
    
    """ Set the current_id_tweet correctly."""
    CURRENT_TWEET_ID = len(MEM_TWEETS) - 1
    
    return tdate

    
""" Read a tweet function handler.  

@arg number: as in the number id of a tweet to be read.
@arg prompt: a prompt flag if no number is given, to prompt it from user on the spot
@arg verbose: Extra info output

@return True/False if successful or not reading occured.

"""
def read_tweet(number, prompt=False, verbose=False):

    if number < 0:
        print("Invalid tweet ID")
        return False

    global CURRENT_TWEET_ID
    global CURRENT_TWEET

    # Must get a number
    if prompt:
        number = input("Enter the ID of the tweet you want to read: ")
        if number.isnumeric() == False:
            return False
        number = int(number)
    
    # Check if number is valid
    if number < 1 or number > len(list(MEM_TWEETS)):
        if verbose:
            print("Invalid tweet ID")
        return False

    
    CURRENT_TWEET_ID = number - 1

    CURRENT_TWEET = MEM_TWEETS[CURRENT_TWEET_ID]

    if verbose:
        print(f"Reading tweet: {CURRENT_TWEET_ID + 1} ...")

    return True





    
    
""" Update a tweet function handler. 
@arg number: number of the tweet to update
@arg tprompt: if no @see argument 'number' is given, prompt a number at spot.
@arg vprompt: a flag whether to get a new text as in string for a tweet update. (USED FOR TESTING PURPOSES)
@arg ttext: a potential text input given already
@arg verbose: Extra info output

@returns the timedate variable of happening(Testing purposes)

"""  
def update_tweet(number, tprompt=False,
vprompt=False, ttext="", verbose=False):

    global CURRENT_TWEET
    global CURRENT_TWEET_ID

    # Read the tweet first. Set it as current and adjust id index via method @read_tweet
    if read_tweet(number, prompt=vprompt, verbose=verbose) == False:
        return None
    # Get the new text input
    if tprompt:
        ttext = input("Enter text: ")

    if verbose:
        print("Updating tweet...")

    tdate = datetime.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year
    
    # Update the tweet
    CURRENT_TWEET.update({"text":ttext})
    CURRENT_TWEET.update({"created_at":tdate})

    return tdate


    
""" Delete a tweet function handler. 
Deletes the current tweet, removes it from list, sets id to -1.

@arg verbose: Extra info output

@return True/False if successful or not deletion occured.

"""
def delete_tweet(verbose=False):

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
    
    
""" Read the Last tweet of the tweet function handler.
Simply reads the last tweet of the list.

@arg verbose: Extra info output

@return True/False if successful or not reading occured.

"""
def read_Ltweet(verbose=False):
 
    if MEM_TWEETS == []:
        if verbose:
            print("Somehow you've deleted all the tweets<?. No tweets left to read.")
        return False

    if verbose:
        print("Reading last tweet...")
    
    global CURRENT_TWEET_ID
    global CURRENT_TWEET

    # Get the last tweet
    CURRENT_TWEET_ID = len(MEM_TWEETS) - 1
    #print("Current tID is: " + str(CURRENT_TWEET_ID))

    CURRENT_TWEET = MEM_TWEETS[-1]

    return True

    
""" Head the current_tweet_id index - 1 

@arg verbose: Extra info output

@return True/False if successful or not reading occured.

"""
def read_prev(verbose=False):

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
    

""" Head the current_tweet_id index + 1 

@arg verbose: Extra info output

@return True/False if successful or not reading occured.

"""
def read_next(verbose=False):
    
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


""" Print the curret_tweet 

@arg verbose: Extra info output

"""
def print_current(prompt=False, verbose=False):

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


    
""" QUIT method  

Quit method exits the program without saving it.

@argument toSave to warn the user about it and potentially save as well.

"""
def quit(toSave=False):
    
    global FD

    print("Quiting...")

    if toSave:
        save_prompt = input("\n*WARNING*\nContents will not be saved. Would you like to save them [Y]? ")
        if save_prompt.upper() == "Y":
            save()

    FD.close()
    sys.exit()
    

""" SAVE method - Overwrites the file 

@arg verbose: Extra info output

"""
def save(verbose=False):
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

    # Initialize
    configureID()
    help()

    # SHELL 
    while(True):
        # Prompt input
        args = input(SHELL_S).split()
        args.reverse()

        while args:

            command = args.pop()
        
            # Guard case statement
            if command not in s_commands:
                help()
                continue


            # Handle choices with if statements.
            if command == 'c':
                create_tweet(tprompt=True, verbose=True)

            # Read a tweet.
            elif command == 'r':
                number = 'foo'
                # Check if number is given
                if args:
                    number = args.pop()            
   
                if number.isnumeric() == False:
                    read_tweet(0, True)    # If no number is provided. Prompt inside.
                    if number in s_commands:
                        args.insert(1, number) # Restore argument
                else:
                    read_tweet(int(number), False)
                    
                        
            # Update a tweet.
            elif command == 'u':
                number = 'foo'
                # Check if a number is given
                if args:
                    number = args.pop()

                if number.isnumeric() == False:
                    update_tweet(number=0,\
                         vprompt=True,\
                         tprompt=True,\
                         verbose=True)
                           # If no number is provided. Prompt inside.
                    if number in s_commands:
                        args.insert(1, number) # Restore argument
                else:
                    update_tweet(number=int(number),\
                        vprompt=False,\
                        tprompt=True,\
                        verbose=True)

            # Delete the current tweet.
            elif command == 'd':
                delete_tweet(verbose=True)

            # Read the last tweet.
            elif command == '$':
                read_Ltweet(verbose=True)

            # Set the upper tweet as current.
            elif command == '-':
                read_prev(verbose=True)

            # Set the lower tweet as current.
            elif command == '+':
                read_next(verbose=True)

            # Print the current tweet.
            elif command == '=':
                print_current(verbose=True)

            # Quit without saving.
            elif command == 'q':
                quit()

            # Save/Write to file.
            elif command == 'w':
                save(verbose=True)

            # Quit and Save.
            elif command == 'x':
                save(verbose=True)
                quit()
            
            # If h is asked implicitely
            elif command == 'h' and len(args) != 1:
                help()


        