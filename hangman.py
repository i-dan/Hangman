from colorama import init
init()

HANGMAN_LOGO = '\033[33m' + """
  _    _
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/""" + '\033[39m'

MAX_TRIES = "\nYou have 6 tries to get the right answer, if you Failed - the man is Dead..\n\n"

#Hangman ascii art
HANGMAN_LEV0 = '\033[33m' + "	x-------x" + '\033[39m'

HANGMAN_LEV1 = '\033[33m' + """	x-------x
	|
	|
	|
	|
	|""" + '\033[39m'
HANGMAN_LEV2 = '\033[33m' + """	x-------x
	|       |
	|       0
	|
	|
	|""" + '\033[39m'
HANGMAN_LEV3 = '\033[33m' + """	x-------x
	|       |
	|       0
	|       |
	|
	|""" + '\033[39m'
HANGMAN_LEV4 = '\033[33m' + r"""	x-------x
	|       |
	|       0
	|      /|\
	|
	|""" + '\033[39m'
HANGMAN_LEV5 = '\033[33m' + r"""	x-------x
	|       |
	|       0
	|      /|\
	|      /
	|""" + '\033[39m'
HANGMAN_LEV6 = '\033[31m' + r"""	x-------x
	|       |
	|       0
	|      /|\
	|      / \
	|""" + '\033[39m'


HANGMAN_STATES  = {0: HANGMAN_LEV0, 1: HANGMAN_LEV1, 2: HANGMAN_LEV2, 3: HANGMAN_LEV3,
						4: HANGMAN_LEV4, 5: HANGMAN_LEV5, 6: HANGMAN_LEV6}

#Functions: ----------------------------------------------------------------------------
def choose_word(path, index):
	"""
	accept a file location, assume file contain a one-line string
	which contains words only. returns a word which will be the secret
	word for the game, the word choosen by th index parameter, if the index
	is higher than the number of words the file contain, so it goes again from
	the start of the file in a circular manner
	:param path: the file path
	:param index: an index number the word be chosen by
	:type path: str
	:type index: int
	:return: the secrete word for the game
	:rtype: str
	"""
	file = open(path, "r")
	content = file.read()
	words_list = content.split()
	file.close()
	return (words_list[(index-1) % len(words_list)])


def hide_word(word):
	"""
	accept the secret word and "hide" it as a sequence of "_" characters separated
	by a white space
	:para word: the word to hide
	:type word: str
	:return: "_ " sequence
	:rtype: str
	"""
	return ("_ ") * (len(word)-1) + "_"


# Validate the paramater is a singular letter
def is_valid_input(letter_guessed, prev_guesses):
	"""
	validate the user input for the current step in the game.
	if the input is illegal (more than 2 characters / not a letter/ letter
	in previus letter guessed list) returns false, otherwise return true
	:param letter_guessed: the current user input
	:param prev_guesses: a list contain user's previous guesses
	:type letter_guessed: str
	:type prev_guesses: str list
	:return: True if the guess is legallly, other wise False
	:rtype: boolean
	"""

	letter_guessed = letter_guessed.lower()
	if (len(letter_guessed) > 1 or not letter_guessed.isalpha() ):
		return False
	if (letter_guessed in prev_guesses):
		return False
	return True


def try_update_letter_guessed(letter_guessed, prev_guesses):
	"""
	try to update prev_guessed with the current user input
	if it's valid input, update prev_guesses and returns true
	otherwise print a string represents "X" to tell the user th einput is illegal
	and print a sequence of the prev_guesses letters to tell the user what
	were his tries so far. (for a case the input is illegal due to the fact it's at prev_gusses)
	:param letter_guessed: the current user input
	:param prev_gusses: list of the letters were already guessed
	:type letter_guessed: str
	:type prev_guesses: str list
	:return: True if prev_gusses was updated, otherwise False
	:rtype: boolean
	"""
	if is_valid_input(letter_guessed, prev_guesses):
		prev_guesses.append(letter_guessed)
		return True
	else:
		s = " -> "
		s = s.join(prev_guesses)
		print("X\n" + s + "\n")
		return False


def show_hidden_words(secret_word, prev_guesses):
	"""
	reveal only the letter that are in the prev_guesses list,
	the rest of "secret_word" letters will be hidden under "_" character
	:param secrete_word: the word to be revealed
	:param prev_guesses: list of the letters to reveal
	:type secret_word: str
	:type prev_guesses: str list
	:return: hidden word reveald at desired places
	:rtype: str
	"""
	hidden = ""
	for char in secret_word:
		if (char in prev_guesses or not char.isalpha()):
			hidden += char
		else:
			hidden += "_ "
	return hidden


def print_hangman(num_of_tries):
	"""
	print the hangman ascii figure according to the number of tries the user faild
	:param _num_of_tries: the number of tries the user faild
	:type num_of_tries: int
	:return: None
	"""
	print(HANGMAN_STATES[num_of_tries] + "\n")


def print_tries_left(num_of_tries):
	"""
	print an appropraite announcment according to remaining number of tries
	:param num_of_tries: the number of gusses the user faild
	:type num_of_tries: int
	:reutrn: None
	"""
	if num_of_tries == 6:
		print("The hangman is DEAD")
	elif num_of_tries > 3:
		print("You have left", '\033[31m' + str(6-num_of_tries) + '\033[39m', "tries to save the hangman\n")
	elif num_of_tries <= 3:
		print("You have left", 6-num_of_tries, "tries to save the hangman\n")


def check_win(secret_word, prev_guesses):
	"""
	check if the user win the game (the user manage to guesss all the letters in
	the secret waord)
	:param secret_word: the secret word to guess
	:param prev_guess: the user's previous guesses
	:type secret_word: str
	:type prev_guesses: str list
	:return: True if the user win the game, otherwise False
	:rtype: boolean
	"""
	temp = True

	for c in secret_word:
		if (c.isalpha()):
			if (c not in prev_guesses):
				temp = False
	return temp





def main():
	#Main variables-------------------------------------------------------------------------
	secret_word = ""
	num_of_tries = 0
	letters_guessed = ""
	prev_guesses = []
	hidden_word = ""

	#Start program--------------------------------------------------------------------------
	print(HANGMAN_LOGO)
	print(MAX_TRIES)

	file_path = input("Please enter a file path: ")
	index = int(input("Please enter index number: "))
	secret_word = choose_word(file_path, index)
	hidden_word = hide_word(secret_word)


	#---------------------------------------------------------------------------------------
	print("\nLet's start!\n")
	print(HANGMAN_STATES[0] + "\n")
	print(hidden_word + "\n")

	while (num_of_tries != 6):
		letter_guessed = input("Guess a letter: ")

		if try_update_letter_guessed(letter_guessed, prev_guesses):

			if letter_guessed in secret_word:
				hidden_word = show_hidden_words(secret_word, prev_guesses)
			else: #the input is valid but the user got the wrong guess
				num_of_tries += 1
				prev_guesses.append(letter_guessed) # even it's wrong guess, it adds the letter to the prev_guess
													# in case the user will guess this letter again
				print("wrong guess! :(")
				print_tries_left(num_of_tries)
				print_hangman(num_of_tries)
			print("\n" + hidden_word + "\n")

			if check_win(secret_word, prev_guesses):
				print("YOU WIN!\nCongratulations! you just saved the hangman! ")
				break
			elif (num_of_tries == 6):
				print("LOSS!")

if __name__ == "__main__":
	main()
