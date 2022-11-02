
import time
import json


def testing_function():
    with open("test.json", "r") as json_file,\
        open("new_test.json", "w") as json_new_file:
        tweet = json.loads()
        print(tweet)


    



current_tweet = ""

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
    #testing_function()
    
# Read a tweet function handler.
def read_tweet(number):
    print("Reading a tweet...")
    
    
# Update a tweet function handler.
def update_tweet(number):
    print("Updating a tweet...")
    
    
# Delete a tweet function handler.
def delete_tweet():
    print("Deleting a tweet...")
    
    
# Read the Last tweet of the tweet function handler
def read_Ltweet():
    print("Reading last tweet...")
    
    
def read_up():
    print("Going up.")
    
    
def read_down():
    print("Going down")
    

    
def print_current():
    print("Printing current:")
    
    
def quit():
    print("Quiting...")
    save_prompt = input("\n*WARNING*\nContents will not be saved. Would you like to save them [Y]? ")

    if save_prompt.upper() == "Y":
        save();

    exit()
    
def save():
    print("\n\nSaving contents...")
    time.sleep(0.3)

    print("\n\nContents saved!", end="")
    
    
def exterminate():
    print("Exiting.")
    save()

    exit()
    



if __name__ == "__main__":


    # SHELL 
    while(True):
        # Prompt input
        args = input("#_> ").split()
        
        args.reverse()

        while args != []:
            command = args.pop()

            # Handle choices with if statements.
            if command == 'c':
                create_tweet()

            elif command == 'r':
                if len(command) < 2:
                    print("Must provide a number!")
                else:
                    num = args.pop()
                    #if num.is
                    if num.isnumeric():
                        read_tweet(num)
                    else:
                        print("Must provide a number for a tweet to read")
                        break

            elif command == 'u':
                if len(command) < 2:
                    print("Must provide a number!")
                else:
                    num = args.pop()
                    if num.isnumeric():
                        update_tweet(args.pop())
                    else:
                        print("Must provide a number for a tweet to update")
                        break

            elif command == 'd':
                delete_tweet()

            elif command == '$':
                read_Ltweet()

            elif command == '-':
                read_down()

            elif command == '+':
                read_up()

            elif command == '=':
                print_current()

            elif command == 'q':
                quit()

            elif command == 'w':
                save()

            elif command == 'x':
                exterminate()
            # if false input or no input. print help
            else:
                help()