"""
Wordel infinite
Ryan Seegmiller
start date 2/2/22
"""
# imports
import base64
import json
import random
from colorama import Fore

# globals
global correct_letters
global correct_letters_wrong_spot
global incorrect_letters
global guessed_words

global guess


correct_letters_wrong_spot = []
incorrect_letters = []
guessed_words = {
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "6": ""
}

guess = 0


# Classes


class New_Word:
    """
        A class to get and encode a new word from the words json file.

        ...

        Attributes
        ----------
        word : str
            stores the encoded word
        letters_list : list
         list of the alphabet
        encoded_word : str
            encoded word string
        word_check : list
            stores the encoded letters in a list

        Methods
        ----------
        file_read : Collects a random word from the all_words.json file

        word_encode : Takes the random word and encrypts it

    """

    def __init__(self):
        """
            Constructs all the necessary attributes

        """
        self.word = ""
        self.letters_list = []
        self.encoded_word = ""
        self.word_check = []

    def file_read(self, letter_count=5):
        """
            Collects a random word from the words.json file

            Parameters
            ----------
            self :
        """
        # Picks a random letter of 26

        # Opens the file and collects the data t
        with open("all_words.json") as f:
            data = json.load(f)

            # picks a random word
            words = data[str(letter_count)]
            self.word = random.choice(words)
        # Encodes the word
        self.word_encode()

    def word_encode(self, user_word=''):
        """
              Takes a word and encrypts it

              Parameters
              ----------
              self :

              user_word : str optional
                    Collects the user input to encode
        """
        # collects the word input and turns it into a list
        if user_word != '':
            self.word = user_word
        self.word = list(self.word)

        # Encodes the word
        for i in self.word:
            byte = bytes(i, "utf-8")
            encoded_letter = base64.b64encode(byte)
            index = self.word.index(i)
            self.word.remove(i)
            self.word.insert(index, encoded_letter)
        for i in self.word:
            i = str(i.decode("utf-8"))
            i = i.replace("==", "")
            self.encoded_word += i
            self.word_check.append(i)
        self.word = self.encoded_word


class Word_Check:
    """
        A class to gets and check the word the user inputs for a match on the correct word.

        ...

        Attributes
        ----------
        word_check : list
            list of encoded letters
        user_word_input : str
            The users input

        Methods
        ----------
        decode_word : Decodes the word and checks the letters to see if they match

        letter_count : Verify the word for correct length, str compatibility and word

    """

    def __init__(self, user_word_input, word_check, letters):
        """
            Constructs all the necessary attributes

            Parameters
            ----------
            word_check : list
            list of encoded letters
            user_word_input : str
            The users input
        """

        self.word_check = word_check
        self.user_word_input = user_word_input
        self.letters_count = letters
    def decode_word(self, encoded_letters):
        """
           Decodes the word and checks the letters to see if they match

           Parameters
           ----------
           encoded_letters : list
           list of letters to decode and check compared to the other letters

        """
        # encodes the users input
        user_check = New_Word()
        user_check.word_encode(user_word=self.user_word_input)
        user_encoded_letters = user_check.word_check

        # Decrypts the words and sorts the letters into the correct lists
        for i in user_encoded_letters:
            if i in encoded_letters:
                if i == user_encoded_letters[encoded_letters.index(i)]:
                    correct_encoded_letter = i + "=="
                    correct_encoded_letter = bytes(correct_encoded_letter, "utf-8")
                    correct_letter = base64.b64decode(correct_encoded_letter)
                    correct_letter = str(correct_letter.decode("utf-8"))
                    correct_letters[str(user_encoded_letters.index(i) + 1)] = correct_letter
                else:
                    correct_encoded_letter = i + "=="
                    correct_encoded_letter = bytes(correct_encoded_letter, "utf-8")
                    correct_letter = base64.b64decode(correct_encoded_letter)
                    correct_letter = str(correct_letter.decode("utf-8"))
                    correct_letters_wrong_spot.append(correct_letter)
            else:
                incorrect_encoded_letter = i + "=="
                incorrect_encoded_letter = bytes(incorrect_encoded_letter, "utf-8")
                incorrect_letter = base64.b64decode(incorrect_encoded_letter)
                incorrect_letters.append(incorrect_letter)

    def letter_verify(self):
        """
            Verify the word for correct length, str compatibility and word

        """
        # Checks if it's a 5 letter string
        for i in self.user_word_input:
            if i.isdigit():
                return f"invalid input, please enter a {str(self.letters_count)} letter word"
        if len(self.user_word_input) != self.letters_count:
            return f"invalid input, please enter a {str(self.letters_count)} letter word"

        # Detects if the word is in the words file
        with open("all_words.json") as f:
            data = json.load(f)
            words_check = data[str(self.letters_count)]
            if self.user_word_input not in words_check:
                return "Not a word"
        return True


class Main:
    """
        A class that runs the main program

        ...

        Attributes
        ----------
        encoded_word : str
            encoded word
        word : str
            holds the decoded word


        Methods
        ----------
        main_game : runs the program till done

        display : displays the letters and spaces

        word_decode : decodes the word completely

        end_main_check : checks if the program needs to end or not

    """

    def __init__(self, word_get, letters):
        """
            Constructs all the necessary attributes

            Parameters
            ----------
            word_get : class
                class to get the current word

        """

        self.encoded_word = word_get.word
        self.word = ''
        self.letter_count = letters
    def main_game(self):
        """
            runs the program till done

        """
        # Declares the global
        global guess

        # Checks the end of the game
        end_game = self.end_main_check()
        if end_game == "Congrats game won":
            self.display()
            print(end_game)
            return "end"
        if guess >= 6:
            print(end_game)
            return "end"

        # Displays the prints
        self.display()

        # user input
        word_input = input("enter a word: \n")
        # word check
        verifier = Word_Check(user_word_input=word_input, word_check=word_get, letters=self.letter_count)
        verified = verifier.letter_verify()
        if isinstance(verified, str):
            print(verified)
            return
        else:
            guess += 1
            guessed_words[str(guess)] = list(word_input)

        # verifies letters
        encoded_letters = word_get.word_check
        verifier.decode_word(encoded_letters)

    def display(self):
        """
            displays the letters and spaces

        """
        # Takes the correct letters and makes the yellow and white then prints the rest of the lines
        for i in range(1, 7):
            if guessed_words[str(i)] != "":
                for j in guessed_words[str(i)]:
                    key = str(guessed_words[str(i)].index(j) + 1)
                    if j == correct_letters[key]:
                        print(Fore.GREEN + (j + " "), end="")
                    elif j in correct_letters_wrong_spot:
                        print(Fore.YELLOW + (j + " "), end="")
                    else:
                        print(Fore.WHITE + (j + " "), end="")
                print("")
            else:
                print(Fore.WHITE + "_ " * letters)

    def word_decode(self):
        """
             decodes the word completely

        """
        # Decodes the word
        for i in range(len(self.encoded_word)):
            if i % 2 == 0:
                encoded_letter = self.encoded_word[i: i + 2] + "=="
                byte_encoded_letter = bytes(encoded_letter, "utf-8")
                byte_letter = base64.b64decode(byte_encoded_letter)
                letter = byte_letter.decode("utf-8")
                self.word += letter

    def end_main_check(self):
        """
            checks if the program needs to end or not

        """
        # Checks what's correct
        correct = 0
        for i in correct_letters:
            if correct_letters[i] != "":
                correct += 1
        if correct == self.letter_count:
            return "Congrats game won"
        elif guess == 6:
            self.word_decode()
            return f"Game lost the word was {self.word}"


# Selects the word to guess
valid = False
while not valid:
    letters = input("How big would you like the word? \n3-18\n")
    try:
        letters = int(letters)
        valid = True
    except:
        print("Invalid")

word_get = New_Word()
word_get.file_read(letter_count=letters)
correct_letters = {}
for i in range(1, letters + 1):
    correct_letters[str(i)] = ""
# Runs the main program till done
while __name__ == "__main__":
    main = Main(word_get, letters)
    end = main.main_game()
    if end == "end":
        quit()
