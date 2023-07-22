# kieran hulsman
# wordle solver
word_list = [] # from text file
INITIAL_GUESS = "adieu"
def init_filter ():
    global gray
    global green
    global yellow_indexed
    global yellow_set
    global word_list
    
    gray = set()
    green = ['','','','','']
    yellow_indexed = [[],[],[],[],[]]
    yellow_set = set()

    assert(isFirstGuess())

def isFirstGuess () -> bool:
    if len(gray) > 0: return False
    if len(yellow_set) > 0: return False
    
    green_isEmpty = True
    for letter in green:
        if letter != '': 
            green_isEmpty = False
    
    return green_isEmpty

def get_word_list ():
    global word_list

    file = open("valid-wordle-words.txt", "r")
    for line in file:
        for word in line.split():
            word_list.append(word)

def update_filter (feedback: str, guess: str) -> None:
    for i,c in enumerate(feedback):
        if c == 'x': gray.add(guess[i])
        elif c == 'g': green[i] = guess[i]
        elif c == 'y':
            yellow_set.add(guess[i])
            yellow_indexed[i].append(guess[i])
        else:
            exit(1)

def isValidGuess (guess: str) -> bool:

    # green
    for i, letter in enumerate(guess):
        if green[i] != '' and letter != green[i]:
            return False
        
    # gray
    for letter in guess:
        if letter in gray: return False

    # yellow set (guess must contain yellow letters)
    for yellow_letter in yellow_set:
        isValid = False
        for guess_letter in guess:
            if yellow_letter == guess_letter:
                isValid = True
        if not isValid: return False
    
    # yellow indexed (letters must not be in the same index as yellow letters)
    for i,letter in enumerate(guess):
        for yellow_letter in yellow_indexed[i]:
            if letter == yellow_letter: return False
  
    return True

def get_guess () -> str:
    if isFirstGuess(): return INITIAL_GUESS
    
    for word in word_list:
        if isValidGuess(word): return word

    exit(1)

def get_feedback (guess: str) -> str:
    print("guess: {}".format(guess))
    feedback = input("feedback: ")
    return feedback

def check_win_conditions (feedback: str, guess: str) -> None:
    if feedback == "ggggg":
        print("WINNER WINNER CHICKEN DINNER! the wordle is: {}".format(guess))
        exit(0)

def lose_conditions () -> None:
    print("sad sad. we lost :(")

# testing
def TEST_isFirstGuess ():
    assert(isFirstGuess())
    
    gray.add('a')
    assert(not isFirstGuess())
    init_filter()

    green[4] = 'a'
    assert(not isFirstGuess())
    init_filter()

    yellow_set.add('a')
    assert(not isFirstGuess())

def TEST_get_word_list ():
    get_word_list()
    for word in word_list:
        print(word)
    
def TEST_isValidGuess ():
    pass

def TEST_update_filter ():

    update_filter("xxxxx", "abcde")
    assert('a' in gray)
    assert('b' in gray)
    assert('c' in gray)
    assert('d' in gray)
    assert('e' in gray)
    init_filter()

    update_filter("yyyyy", "abcde")
    assert('a' in yellow_set)
    assert('b' in yellow_set)
    assert('c' in yellow_set)
    assert('d' in yellow_set)
    assert('e' in yellow_set)
    assert(len(yellow_indexed[0])==1 and yellow_indexed[0][0]=='a')
    assert(len(yellow_indexed[1])==1 and yellow_indexed[1][0]=='b')
    assert(len(yellow_indexed[2])==1 and yellow_indexed[2][0]=='c')
    assert(len(yellow_indexed[3])==1 and yellow_indexed[3][0]=='d')
    assert(len(yellow_indexed[4])==1 and yellow_indexed[4][0]=='e')
    init_filter()

    update_filter("ggggg", "abcde")
    assert(green[0]=='a')
    assert(green[1]=='b')
    assert(green[2]=='c')
    assert(green[3]=='d')
    assert(green[4]=='e')
    init_filter()

    update_filter("xxygx", "abcde")
    assert('a' in gray)
    assert('b' in gray)
    assert('c' in yellow_set)
    assert(len(yellow_indexed[2])==1 and yellow_indexed[2][0]=='c')
    assert(green[3]=='d')
    assert('e' in gray)
    init_filter()

def TEST_isValidGuess ():
    update_filter("xxxxx", "abcde")
    assert(not isValidGuess("abcde"))
    init_filter()

    update_filter("gxxxx", "abcde")
    assert(not isValidGuess("zzzzz"))
    assert(isValidGuess("azzzz"))
    init_filter()

    update_filter("yxxxx", "abcde")
    assert(not isValidGuess("azzzz"))
    assert(not isValidGuess("zzzzz"))
    assert(isValidGuess("zazzz"))
    init_filter()

    update_filter("xxxyx", "adieu")
    assert(not isValidGuess("louse"))
    assert(isValidGuess("froze"))
    init_filter()

    update_filter("xxxyx", "adieu")
    update_filter("xyxyx", "bebop")
    assert(not isValidGuess("check"))
    init_filter()

def TEST_get_guess ():
    get_word_list()
    assert(get_guess() == INITIAL_GUESS)
    update_filter("xxxyx", INITIAL_GUESS)
    print(get_guess())
    init_filter()

def TEST_get_feedback ():
    feedback = get_feedback(INITIAL_GUESS)
    print("\n\nTEST result: {}".format(feedback))

def TEST_check_win_conditions ():
    check_win_conditions("ggggy", "abcde")
    print("TEST line, you should see")
    check_win_conditions("ggggg", "abcde")
    assert(0)

def TEST_lose_conditions():
    lose_conditions()

def report_filter_status ():
    gray_list = list(gray)
    gray_list.sort()
    yellow_list = list(yellow_set)
    yellow_list.sort()
    
    print("\n---FILTER STATUS START---")
    print("green: {}".format(green))

    print("yellow set: {}".format(yellow_list))
    print("yellow indexed: {}".format(yellow_indexed))

    print("gray: {}".format(gray_list))
    print("---FILTER STATUS END  ---\n")

# control centre
def test ():
    init_filter()
    get_word_list()

    ### TESTS HERE ###
    TEST_isValidGuess()

def main ():
    init_filter()
    get_word_list()
    for i in range(6):
        guess = get_guess()
        feedback = get_feedback(guess)
        check_win_conditions(feedback, guess)
        update_filter(feedback, guess)
    lose_conditions()

if __name__=="__main__":
    main()