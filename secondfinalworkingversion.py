# Imports
from threading import Timer

from config import dictionary_loc
from config import turntext_loc
from config import wheeltext_loc
from config import maxrounds
from config import roundstatus_loc
from config import final_round_text_loc

import random

# Defining Variables 
players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

round_num = 0
dictionary = []
turn_text = ""
wheellist = []
round_word = ""
blank_word = []
vowels = {"a", "e", "i", "o", "u"}
round_status = ""
final_round_text = ""
guessed_letter = []


# Defining Functions


def read_dictionary_file():
    global dictionary
    # Read dictionary file in from dictionary file location
    f = open(dictionary_loc, 'r')
    # Store each word in a list.
    dictionary = f.read().splitlines()
      
    
def read_turn_text_file():
    global turn_text   
    #read in turn intial turn status "message" from file
    f = open(turntext_loc, 'r')
    turn_text = f.read()
  

        
def read_finalround_text():
    global final_round_text   
    #read in turn intial turn status "message" from file
    f = open(final_round_text_loc, 'r')
    final_round_text = f.read()

def read_round_status_file():
    global round_status
    # read the round status  the Config round_statusloc file location 
    f = open(roundstatus_loc, 'r')
    round_status = f.read()

def read_wheeltext_file():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    f = open(wheeltext_loc, 'r')
    wheellist = f.read().splitlines()
    
def get_player_info():
    global players

    # read in player names from command prompt input
    first_player = str(input("Please Enter First Player Name: "))
    second_player = str(input("Please Enter Second Player Name: "))
    third_player = str(input("Please Enter Third Player Name: "))

    # Store player names in the players dictionary
    players[0]['name'] = first_player
    players[1]['name'] = second_player
    players[2]['name'] = third_player


def game_setup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turn_text
    global dictionary
        
    read_dictionary_file()
    read_turn_text_file()
    read_wheeltext_file()
    get_player_info()
    read_round_status_file()
    read_finalround_text() 
    
def get_word():
    global dictionary
    #choose random word from dictionary
    round_word = random.choice(dictionary)
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = ['_' for i in round_word]
    return round_word,roundUnderscoreWord

def wof_round_setup():
    global players
    global round_word
    global blank_word
    global guessed_letter
    # Set round total for each player = 0
    players[0]['roundtotal'] =0
    players[1]['roundtotal'] =0
    players[2]['roundtotal'] =0
    # Return the starting player number (random)
    init_player = int(random.choice(list(players.keys())))

    #Clear the guessed list
    guessed_letter = []
    # Use get_word function to retrieve the word and the underscore word (blank_word)
    round_word,blank_word = get_word()
    return init_player


def spin_wheel(player_num):
    global wheellist
    global players
    global vowels

    
    # Get random value for wheellist
    spin = random.choice(wheellist)
    # Check for bankrupcy, and take action.
    if spin == 'BANKRUPT':
        players[player_num]['roundtotal'] = 0
        print('You landed on: BANKRUPT')
        still_in_turn = False

    # Check for loose turn
    elif spin == 'Lose-a-Turn':
        print("You landed on: LOSE A TURN")
        still_in_turn = False

    # Get amount from wheel if not loose turn or bankruptcy
    elif spin != 'BANKRUPT' and spin != 'Lose-a-Turn':
        converted_spin = int(spin)     
        print(f'You landed on: ${spin}') 
         
    # Ask user for letter guess and Ensure that it's a consonate
        not_consonate = True
        while not_consonate == True:
            letter_guess = str(input("Please type a consonate: "))

            # Check if letter is in vowel and if it was already guessed
            is_letter_in_vowels = letter_guess in vowels
            is_letter_in_guessed_letter = letter_guess in guessed_letter

            # If the letter is a consonate and it was not guessed, add letter to guessed_letter list and break while loop, otherwise try again
            if is_letter_in_vowels == False and is_letter_in_guessed_letter == False:
                not_consonate = False
                guessed_letter.append(letter_guess)
                break
            else:
                print("This is a vowel or you already guessed this letter, try agin")
        # Use guess_letter function to see if guess is in word, and return count
        g, p = guess_letter(letter_guess,player_num)

        # Change player round total if they guess right.
        if g == True:
            money_to_add = ((converted_spin * int(p)) + int(players[player_num]['roundtotal']))
            players[player_num]['roundtotal'] = money_to_add
            still_in_turn = True
        else:
            still_in_turn = False   
  
    return still_in_turn


def guess_letter(letter, player_num): 
    global players
    global blank_word
    global round_word
    good_guess = False
    count = 1
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blank_word to the letter instead of underscore 
    for i, char in enumerate(round_word):
        if char == letter:
            blank_word[i] = char
    # return count of letters in word. 
            count = blank_word.count(letter)
            good_guess = True
    # return good_guess= true if it was a correct guess
    return good_guess, count

def buy_vowel(player_num):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost and subtract from roundtotal if they do
    if int(players[player_num]['roundtotal']) >= 250:
        new_total = int(players[player_num]['roundtotal'] - 250)
        players[player_num]['roundtotal'] = new_total
       
    # Use guess_letter function to see if the letter is in the file and make sure it was not already guessed
        is_vowel = False
        while is_vowel == False:
            vowel_guess = str(input("Type vowel: "))
            is_letter_in_vowels = vowel_guess in vowels
            is_letter_in_guessed_letter = vowel_guess in guessed_letter

            # If letter was a vowel and not yet guessed, add it to the guess letter list and break while loop, otherwise try again
            if is_letter_in_vowels == True and is_letter_in_guessed_letter == False:
                is_vowel = True
                guessed_letter.append(vowel_guess)
            else:
                print("This is not a vowel or you already guessed this vowel, Try again")
   
    # If letter is in the file let good_guess = True
        good_guess,count = guess_letter(vowel_guess,player_num)
    else: 
        good_guess = False
        print("You don't have enough money!!!!")

    
       
    
    return good_guess      
        
def guess_word(player_num):
    global players
    global blank_word
    global round_word
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    word_guess = str(input("Guess Word: "))
    if word_guess == round_word:
    # Fill in blankList with all letters, instead of underscores if correct 
        blank_word = [round_word]
        
    # return False ( to indicate the turn will finish)  
    
        return False
    else:
        return False
    
    
def wof_turn(player_num):  
    global round_word
    global blank_word
    global turn_text
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round (empty spaces and === are meant to beautify the output)
    print("                         ")
    print(f"{' '.join(blank_word)}  (hint:{round_word})")
    print("                         ")
    print("=========================================")
    print(f"{turn_text}, {players[player_num]['name']}")
    print(f"You have: ${players[player_num]['roundtotal']}") 

    
    still_in_turn = True
    while still_in_turn:
        
        # use the string.format method to output your status for the round
        print('======================================')
        print(" ")
        print(f"{' '.join(blank_word)}  (hint:{round_word})")
        print(" ")
        print(f"{turn_text} {players[player_num]['name']}")
        print(f"You have: ${players[player_num]['roundtotal']}") 
        print(" ")
        # Get user input S for spin, B for buy a vowel, G for guess the word
        #Continue player turn unti they guess incorrectly, spin bankrupt, or spin lose a turn
        choice = str(input("Would you like to (S) spin, (B) buy a vowel ($250), or (G) guess the word? "))
        print("           ")
        print("           ")        
        if(choice.strip().upper() == "S"):
            still_in_turn = spin_wheel(player_num)
        elif(choice.strip().upper() == "B"):
            still_in_turn = buy_vowel(player_num)
        elif(choice.upper() == "G"):
            still_in_turn = guess_word(player_num)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
        joined_blank_word = str(''.join(blank_word))
        if joined_blank_word == round_word:
            blank_word = [round_word]
            still_in_turn = False
            
        
        


def wof_round():
    global players
    global round_word
    global blank_word
    global round_status
    init_player = wof_round_setup()
    
    # Keep doing things in a round until the round is done ( word is solved)
   
    while blank_word != [round_word]:
        # While still in the round keep rotating through players
        # Use the wof_turn fuction to dive into each players turn until their turn is done.
        if init_player == 0:
            wof_turn(init_player)
            init_player = 1
        elif init_player == 1:
            wof_turn(init_player)
            init_player = 2
        elif init_player == 2:
            wof_turn(init_player)
            init_player = 0
           

    # Print round_status with string.format, tell people the state of the round as you are leaving a round.
    print("         ")
    print("         ")
    print("Word Solved")
    print(f"The word was: {round_word}")
    print(round_status)
    print("Round Earnings")
    print("---------------")
    #Store round winnings
    playerzero_winnings = int(players[0]['roundtotal'])
    playerone_winnings = int(players[1]['roundtotal'])
    playertwo_winnings = int(players[2]['roundtotal'])

    # Find the player who had the maximum roundtotal and store that into their gametotal
    max_winnings = max(playerone_winnings,playertwo_winnings,playerzero_winnings)
    for i in players:
        if players[i]['roundtotal'] == max_winnings:
            players[i]['gametotal'] = players[i]['roundtotal'] + players[i]['gametotal']
    
    #print all of the players round total and game total
    for i in players:
        print(f"{players[i]['name']}: ${players[i]['roundtotal']}")
    
    print("          ")
    print("Game Total")
    print("-----------")
    for i in players:
        print(f"{players[i]['name']}: ${players[i]['gametotal']}")
    print("                ")
    print("                ")


def timer():
    #Timer to time out after 5 seconds during the final round and return the guess, if there is one
   timeout = 5
   t = Timer(timeout, print, ['Time is up, Press Enter to Continue'])
   t.start()
   guess_final_word = str(input("Guess Word: "))
   t.cancel()


   return guess_final_word

def wof_final_round():
    global round_word
    global blank_word
    global final_round_text
    win_player = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing and stored as the win_player.
    playerzero_game_winnings = int(players[0]['gametotal'])
    playerone_game_winnings = int(players[1]['gametotal'])
    playertwo_game_winnings = int(players[2]['gametotal'])

    max_game_winnings = max(playerone_game_winnings,playertwo_game_winnings,playerzero_game_winnings)
    for i in players:
        if players[i]['gametotal'] == max_game_winnings:
            win_player = i
            amount = max_game_winnings

    # Print out instructions for that player and who the player is.
    print(f"{final_round_text} ")
    print(f"{players[win_player]['name']} you are our Contestant")
    print("=======================")

    # Use the get_word function to reset the round_word and the blank_word ( word with the underscores)
    round_word, blank_word = get_word()

    # Use the guess_letter function to check for {'R','S','T','L','N','E'}
    guess_letter('r',win_player)
    guess_letter('s',win_player)
    guess_letter('t',win_player)
    guess_letter('l',win_player)
    guess_letter('n',win_player)
    guess_letter('e',win_player)

    # Print out the current blank_word with whats in it after applying {'R','S','T','L','N','E'}
    print(f"Here is the final word: {' '.join(blank_word)}")

    # Gather 3 consonats and 1 vowel and use the guess_letter function to see if they are in the word
    consonant_one = str(input("Please enter first consonant: "))
    consonant_two = str(input("Please enter second consonant: "))
    consonant_three = str(input("Please enter third consonant: "))
    vowel_one = str(input("Please enter a vowel: "))
    guess_letter(consonant_one,win_player)
    guess_letter(consonant_two,win_player)
    guess_letter(consonant_three,win_player)
    guess_letter(vowel_one,win_player)

    # Print out the current blank_word again
    print(f"{' '.join(blank_word)}")

    # Get user to guess word within 5 seconds, otherwise time out
    guess_final_word = timer()

    # If guess is correct, player adds $50,000 to their game total winings, which is printed out
    if guess_final_word == round_word:
        players[win_player]['gametotal'] = int(players[win_player]['gametotal'] + 50000)
        print("                          ")
        print("============================")
        print(f"The word was: {round_word}")
        print("                           " )
        print(f"You Won!!!!!! Here are your total Winings: ${players[win_player]['gametotal']}")
    else:
        print(f"The word was: {round_word}")
        print(f"You did not win the final round. Your winnings are: ${players[win_player]['gametotal']}")

#Running the game
def main():
    game_setup()
    
    for i in range(0,maxrounds):
        if i in [0,1]:
            print("                    ")
            print(f'This is round {i+1}')
            print("=====================")
            wof_round()
        else:
            wof_final_round()
   
if __name__ == "__main__":
    main()
    
    
