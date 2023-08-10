# kieran hulsman
# project:wordle - freq sort testing
# aug 9 2023

'''
COMMANDS NEEDED TO INSTALL nltk
$ pip install nltk
$ python3
>>> import nltk
>>> nltk.download()

note: nltk_data is in /kieranhulsman/nltk_data
'''

import nltk # natural languague toolkit
from nltk.corpus import brown

def get_raw_words ():
    word_list = []
    src_file = open("alpha-sorted-words.txt", "r")
    for line in src_file:
        for word in line.split():
            word_list.append(word)
    src_file.close()
    return word_list

# ripped this code from stackoverflow
def sort_words (word_list: list):
    freqs = nltk.FreqDist([w.lower() for w in brown.words()])
    word_list = sorted(word_list, key=lambda x: freqs[x.lower()], reverse=True)
    return word_list

def write_to_file (word_list: list):
    dest_file = open("freq-sorted-words.txt", "a")
    for word in word_list:
        dest_file.write("{}\n".format(word))
    dest_file.close()


def main():
    word_list = get_raw_words() # user created obj's are pass by ref, not data types??
    word_list = sort_words(word_list)
    write_to_file(word_list)

main()