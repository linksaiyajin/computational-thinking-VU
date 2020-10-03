import random
import re
import os
import sys


def update(word, dashes, guess):
    """updates the guess so far with the newly guessed letter"""
    updated = ""
    indices = [m.start() for m in re.finditer(guess, word)]
    if len(indices) == 1:                                                   # guess has only one occurrence
        if indices[0] == 0:
            updated = guess + dashes[indices[0]+1:]                         # guess is first letter of the word
        elif indices[0] == len(word) - 1:
            updated = dashes[:indices[0]] + guess                           # guess is last letter of the word
        else:
            updated = dashes[:indices[0]] + guess + dashes[indices[0]+1:]   # guess is neither first nor last letter
        return updated
    for k in range(len(indices)):                                           # guess has multiple occurrences
        if indices[k] == 0:
            updated = guess + dashes[indices[k]+1:]
        elif indices[k] == len(word) - 1:
            updated = dashes[:indices[k]] + guess
        else:
            updated = dashes[:indices[k]] + guess + dashes[indices[k]+1:]
        dashes = updated
    return updated


def drawfigures():
    """Draws all the possible states of the hangman figure. Produces hardcoded states that can be printed"""
    figure = [""]
    figure.append("\n" + "\n" + "\n" + "\n" + "\n" + "|_____")
    figure.append("\n" + "|\n" + "|\n" + "|\n" + "|\n" + "|_____")
    figure.append("__________\n" + "|\n" + "|\n" + "|\n" + "|\n" + "|_____")
    figure.append("__________\n" + "|        |\n" + "|\n" + "|\n" + "|\n" + "|_____")
    figure.append("__________\n" + "|        |\n" + "|        O\n" + "|\n" + "|\n" + "|_____")
    figure.append("__________\n" + "|        |\n" + "|        O\n" + "|      __|__\n" + "|\n" + "|_____")
    figure.append("__________\n" + "|        |\n" + "|        O\n" + "|      __|__\n" + "|        /\\" + "\n" + "|_____")
    figure.append("__________\n" + "|        |\n" + "|        O\n" + "|      __|__\n" + "|        /\\" + "\n" + "|       /  \\" + "\n" + "|_____")
    return figure


while True:                                         # makes sure that the name given is of type string
    name = input("What is your name?" + "\n")
    if isinstance(name, str):
        break
    else:
        print("Name is not of type string")
won = False
words = ["UNIVERSITY", "SCHOOL", "CAT", "DOG", "WORK", "SCIENCE", "ARTIFICIAL", "INTELLIGENCE", "COMPUTER", "THINKING", "PYTHON", "EXPERIENCE", "GAME", "NETHERLANDS"]
guessed = []
word = random.choice(words)                         # randomly chooses a word out of the list 'words'
dashes = "_" * len(word)                            # creates a string of dashes as long as the secret word
failcount = 0                                       # counts number of failed guesses to print the corresponding figure
figure = drawfigures()                              # draws all possible figure states
print("The secret word is: " + dashes + ". It has " + str(len(word)) + " letters")
while not won:                                      # game runs as long as its neither won nor lost yet
    guess = input("Guess one letter, " + name + "\n")  # gets the users guess
    if not guess.isalpha():                         # makes sure that the guess is a letter
        print("The guess is illegal, please guess again")
        continue
    guess = guess.capitalize()                      # capitalizes the guess in case it isn't
    if guess in word:                               # user guessed right
        if guess in guessed:                        # duplicate guess lets user try again for free
            print("You have already guessed this letter")
            continue
        else:
            guessed.append(guess)                   # adds guess to list of previous guesses
            dashes = update(word, dashes, guess)    # updates the guess so far
            print("Great! you have guessed a letter!")
            print(dashes)                           # shows what has been guessed so far
            if dashes == word:                      # guess is complete = won game
                won = True
            if not won:
                attempt = input("You may attempt to guess the word" + "\n")
                attempt = attempt.upper()
                if attempt == word:                 # if you guess the whole word right, wou win
                    won = True
                else:                               # if you guess wrong, you continue guessing letters
                    print("You guessed wrong!")
    else:                                           # if the letter is not in the secret word
        if guess in guessed:                        # no penalty if you have guessed this letter before
            print("You have already guessed this letter")
            continue
        failcount += 1                              # updates number of fails
        print("You guessed wrong!")
        print(figure[failcount])                    # prints the figure corresponding to the number of fails
        if failcount == 8:                          # reached maximum fails = lost game
            while True:                             # ask the user if he wants to play again
                answer = input("You have lost! " + "The secret word was " + word + ". " + "Do you want to play again? (y/n): " + "\n")
                if answer in ('y', 'n'):            # only allow (y/n) answer
                    break
                print("Invalid input.")
            if answer == 'y':
                os.execl(sys.executable, sys.executable, *sys.argv)  # restart game
            else:
                print("Goodbye " + name + "!")
                exit()                              # end game
while True:
    answer = input("You have won! Do you want to play again? (y/n): " + "\n")
    if answer in ('y', 'n'):                        # only allow (y/n) answer
        break
    print("Invalid input.")
if answer == 'y':
    os.execl(sys.executable, sys.executable, *sys.argv)  # restart game
else:
    print("Goodbye " + name + "!")                  # end game
