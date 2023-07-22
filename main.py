# kieran hulsman
# wordle solver

# global variables
gray = set()
green = ['','','','','']
yellow_indexed = [[],[],[],[],[]]
yellow_set = set()
word_list = [] # gotten from text file

def isFirstGuess () -> bool:
    if len(gray) > 0: return False
    if len(yellow_set) > 0: return False
    
    green_isEmpty = True
    for letter in green:
        if letter != '': 
            green_isEmpty = False
    
    return green_isEmpty

def get_word_list ():
    file = open("valid-wordle-words.txt", "r")
    for line in file:
        for word in line.split():
            word_list.append(word)

def isValidGuess (guess: str) -> bool:

    # green
    for i, letter in enumerate(guess):
        if green[i] != '' and letter != green[i]:
            return False
        
    # gray
    for letter in guess:
        if letter in gray: return False

    # yellow set (guess must contain yellow letters)
    if len(yellow_set) > 0:
        isValid = False
        for letter in guess:
            if letter in yellow_set: 
                isValid = True
        if not isValid: return False
    
    # yellow indexed (letters must not be in the same index as yellow letters)
    for i,letter in enumerate(guess):
        for yellow_letter in yellow_indexed[i]:
            if letter == yellow_letter: return False
  
    return True

def get_guess () -> str:
    INITIAL_GUESS = "adieu"
    if isFirstGuess(): return INITIAL_GUESS
    
    for word in word_list:
        if isValidGuess(word): return word

    exit(1)

def get_feedback (guess: str) -> str:
    print("guess: {}".format(guess))
    feedback = input("feedback: ")
    return feedback

def update_filter (feedback: str) -> None:
    for i,c in enumerate(feedback):
        if c == 'x': gray.add(c)
        elif c == 'g': green.add(c)
        elif c == 'y':
            yellow_set.add(c)
            yellow_indexed[i].append(c)
        else:
            exit(1)

def main ():
    get_word_list()
    for i in range(6):
        guess = get_guess()
        feedback = get_feedback(guess)
        update_filter(feedback)

# testing function
def test ():
    get_word_list()
    for word in word_list:
        print(word)

if __name__=="__main__":
    test()