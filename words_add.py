# imports
import json

# Takes the new words
words_to_add = open("words.txt", "r+")
output = open("all_words.json", "r+")

# sets the dict
word_dict = {

}

# Reads the words
all_words = words_to_add.read()
all_words = all_words.split("\n")

# adds the words to the all words file
for word in all_words:
    if len(word) in word_dict.keys():
        word_dict[(len(word))].append(word)
    else:
        word_dict.update({len(word): [word]})

json.dump(word_dict, fp=output, sort_keys=True, indent=4)
