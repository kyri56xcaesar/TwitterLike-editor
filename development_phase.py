
import time
import json
import os



def testing_function():
 



    with open("test.json", "rb") as file:
    
        test = []
    
        for i, line in enumerate(file):
            test.append(i+1)
            print(i+1)
    
        print(test)
    
    
    return
    
    with open("tweetdhead300000.json", "rb") as file:

        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        
        last_line = file.readline().decode()
    
    print(last_line)




# list of commands available
s_commands = ['c', 'r', 'u', 'd', '$', '-', '+', '=', 'q', 'w', 'x', 'h']
    
# Tweets ID array/list record
t_ID = []

# Current tweet selected (as string)
current_tweet = ""

# Current tweet ID selected
current_tweet_id = 0

# number prompted when reading or updating a tweet
number = 0

# --- Setup method.
# Initialize the t_ID list with the index/number of each line
# Consider starting from 1. As the first tweet is ID is 1.
def configureID():
     with open("tweetdhead300000.json", "rb") as file:

        for i, line in enumerate(file):
            t_ID.append(i+1)

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

# Create a tweet function handler.  
def create_tweet():
    print("Creating a tweet...")
    testing_function()
    
# Read a tweet function handler.
def read_tweet(number, prompt=False):

    # Must get a number
    if prompt:
        number = int(input("Enter the ID of the tweet you want to read: "))
    else:
        print("Reading a tweet...")
    
    print(number)

    if number <= 1 or number >= len(t_ID):
        print("Invalid tweet ID")
        return
    
# Update a tweet function handler.
def update_tweet(number, prompt=False):
    # Must get a number
    if prompt:
        number = int(input("Enter the ID of the tweet you want to read: "))
    else:
        print("Updating a tweet...")
    
    print(number)

    if number <= 1 or number >= len(t_ID):
        print("Invalid tweet ID")
        return
    
# Delete a tweet function handler.
def delete_tweet():
    print("Deleting a tweet...")
    
    
# Read the Last tweet of the tweet function handler
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
    
    
    
def read_up():
    print("Going up.")

    global current_tweet_id
    
    if current_tweet_id <= 1:
        print("Can't do that.")
        return

    current_tweet_id = t_ID[current_tweet_id - 1] 

    
def read_down():
    print("Going down")

    global current_tweet_id
    
    if current_tweet_id > t_ID.length:
        print("Can't do that.")
        return

    current_tweet_id = t_ID[current_tweet_id + 1]

    
def print_current():
    print("\nPrinting current:\n")
    print(f"Current tweet ID: {current_tweet_id}")

    toPrint = input("Print the whole tweet? [y]")
    print(toPrint)
    print(type(toPrint))
    if toPrint.capitalize() == 'Y' or toPrint == "":
        print(current_tweet)
    
    
def quit(toSave=False):
    print("Quiting...")

    if toSave:
        save_prompt = input("\n*WARNING*\nContents will not be saved. Would you like to save them [Y]? ")
        if save_prompt.upper() == "Y":
            save();
    exit()
    
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
                # Check if number is given
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
                read_down()

            # Set the lower tweet as current.
            elif command == '+':
                read_up()

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
            elif args==[]:
                help()