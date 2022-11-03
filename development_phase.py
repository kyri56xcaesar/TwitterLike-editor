from datetime import datetime, date, time, timezone
import time
import json
import os
import ast



# TODO : 
#   -handle tasks and save
#   -finish update
#   -scoope delete



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


# Tasks to do in order to save
tasks = []


# --- Setup method.
# Initialize the t_ID list with the index/number of each line
# Consider starting from 1. As the first tweet is ID is 1.
def configureID():
     with open("tweetdhead300000.json", "rb") as file:

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

# Create a tweet function handler.      --> DONE
def create_tweet():
    print("Creating a tweet...")

    # text
    ttext = input("Enter text: ")

    # created at
    tdate = date.today().strftime('%a %b %d %H:%M:%S +0200%Z %Y')   # Day Month Day/Month HH:mm:ss timezone year
 
    # Create a new JSON tweet
    new_tweet = json.dumps({'text': ttext,'created at':tdate})
    
    # Schedule a task
    tasks.append(({"n":new_tweet}, current_tweet_id))

    ## TO BE MOVED
    # save to file?
    with open("test.json", "a") as file:
        file.write(new_tweet+"\n")

    # Set this new tweet as the current tweet 
    current_tweet_id = t_ID[-1]
    # Set the new current_tweet
    current_tweet = new_tweet
    
    # Update the tweetID list
    t_ID.append(current_tweet)
    


    
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
    else:
        print("Reading a tweet...")
    
    # Check if number is valid
    if number < 1 or number > len(t_ID):
        print("Invalid tweet ID")
        return False

    # Find the corresponding tweet
    with open("tweetdhead300000.json", "r") as rfile:
        for i, line in enumerate(rfile):
            if i + 1 == number:
                current_tweet=line
                current_tweet_id = i
                break

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

    # Update the current tweet
    current_tweet.find("text")

    # Schedule task
    tasks.append(({"u":current_tweet}, current_tweet_id))

    # read_tweet handles current_id position
    
    
# Delete a tweet function handler. --> TODO
def delete_tweet():

    global current_tweet_id
    global current_tweet

    print("Deleting a tweet...")

    tasks.append(({"d":current_tweet}, current_tweet_id))

    ## UPDATE TWEET TABLE
    for i in range(len(t_ID) - current_tweet_id + 1):
        t_ID[current_tweet_id] = t_ID[current_tweet_id + 1]

    # restart index
    current_tweet_id = 0
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

    
    
    with open("tweetdhead300000.json", "rb") as file:

        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        
        current_tweet=file.readline().decode()
    
    
# Head the tweet id index - 1 ---> DONE
def read_prev():
    print("Going up.")

    global current_tweet_id
    
    if current_tweet_id <= 0:
        print("Can't do that.")
        return

    current_tweet_id = t_ID[current_tweet_id - 1] 
    read_tweet(current_tweet_id+1)
    

# Head the tweet id index + 1 ---> DONE
def read_next():
    print("Going down")

    global current_tweet_id
    
    if current_tweet_id >= len(t_ID) - 1:
        print("Can't do that.")
        return

    current_tweet_id = t_ID[current_tweet_id + 1]
    read_tweet(current_tweet_id+1)


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
            save();
    exit()
    
## SAVE method - Overwrites the file --> TODO
def save():
    print("\n\nSaving contents...")
    time.sleep(0.3)

    print("\n\nContents saved!")
    
    

    



if __name__ == "__main__":


    configureID()

    # SHELL 
    while(True):
        # Prompt input
        args = input("#_> ").split()
        args.reverse()

        while args != []:
            command = args.pop()


            # Not sure how to handle garbage arguments. Ignore or iterate next ;<?

            # Handle choices with if statements.
            if command == 'c':
                create_tweet()

            # Read a tweet.
            elif command == 'r':
                number = 'foo'
                # Check if number is given
                if args != []:
                    number = args.pop()            
   
                if number.isnumeric() == False:
                    read_tweet(0, True)    # If no number is provided. Prompt inside.
                    args.insert(1, number) # Restore argument
                else:
                    read_tweet(int(number), False)
                    
                        
            # Update a tweet.
            elif command == 'u':
                # Check if a number is given
                number = args.pop()

                if number.isnumeric() == False:
                    update_tweet(0, True)  # If no number is provided. Prompt inside.
                    args.insert(1, number) # Restore argument
                else:
                    update_tweet(int(number), False)

            # Delete the current tweet.
            elif command == 'd':
                delete_tweet()

            # Read the last tweet.
            elif command == '$':
                read_Ltweet()

            # Set the upper tweet as current.
            elif command == '-':
                read_prev()

            # Set the lower tweet as current.
            elif command == '+':
                read_next()

            # Print the current tweet.
            elif command == '=':
                print_current()

            # Quit without saving.
            elif command == 'q':
                quit()

            # Save/Write to file.
            elif command == 'w':
                save()

            # Quit and Save.
            elif command == 'x':
                save()
                quit()
            
            # If h is asked implicitely
            elif command == 'h' and len(args) != 1:
                help()

            # if false input or no input. print help
            #elif args==[]:
            #    help()