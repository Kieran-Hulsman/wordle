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

def isWin (feedback: str) -> bool:
    return feedback == "ggggg"

def report_win (answer: str) -> None:
    print("WINNER WINNER CHICKEN DINNER! the wordle is: {}".format(answer))
    exit(0)

def report_loss () -> None:
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

def TEST_isWin ():
    assert(not isWin("ggggy"))
    assert(isWin("ggggg"))

def TEST_report_loss():
    report_loss()

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

# reports efficacy of the bot, used for comparing subsequent versions
class Evaluation:
    UNINITIALIZED_VALUE = -1
    def __init__ (self):
        self.min_score = self.UNINITIALIZED_VALUE
        self.max_score = self.UNINITIALIZED_VALUE
        self.total_guesses = 0
        self.num_words = 0
        get_word_list()

    def get_avg (self) -> float:
        return round(self.total_guesses / self.num_words, 2)
    
    def get_automated_feedback (self, guess: str, ans: str) -> str:
        res = ""
        ans_set = set(ans)
        for i,c in enumerate(guess):
            if c == ans[i]: res += 'g'
            elif c in ans_set: res += 'y'
            else: res += 'x'
        return res
    
    def get_wordle_score (self, ans: str) -> int:
        init_filter()
        for i in range(1000):
            guess = get_guess()
            feedback = self.get_automated_feedback(guess, ans)
            if isWin(feedback): return i+1
            update_filter(feedback, guess)
        exit(1)

    def generate_evaluation (self) -> None:
        for i,word in enumerate(word_list):
            print(i) # testing
            score = self.get_wordle_score(word)
            if self.min_score==self.UNINITIALIZED_VALUE or score < self.min_score:
                self.min_score = score
            if self.max_score==self.UNINITIALIZED_VALUE or score > self.max_score:
                self.max_score = score
            self.total_guesses += score
            self.num_words += 1
    
    def report_evaluation (self) -> None:
        # eval must be generated in order for this function to work
        print("---WORDLE BOT VERSION EVALUATION REPORT---")
        print("min score: {}".format(self.min_score))
        print("max score: {}".format(self.max_score))
        print("avg score: {}".format(self.get_avg()))
        print("---WORDLE BOT VERSION EVALUATION REPORT---")

    def TEST_init (self):
        obj = Evaluation()
        assert(obj.min_score == self.UNINITIALIZED_VALUE)
        assert(obj.max_score == self.UNINITIALIZED_VALUE)
        assert(obj.total_guesses == 0)
        assert(obj.num_words == 0)

    def TEST_get_avg (self):
        NUMERATOR = 5
        DENOMINATOR = 7
        ACCEPTABLE_ERR = 0.0001
        obj = Evaluation()
        obj.total_guesses = NUMERATOR
        obj.num_words = DENOMINATOR
        assert(abs(obj.get_avg() - NUMERATOR/DENOMINATOR) < ACCEPTABLE_ERR)
    
    def TEST_get_automated_feedback (self):
        obj = Evaluation()
        assert(obj.get_automated_feedback(guess="abcde", ans="fghij") == "xxxxx")
        assert(obj.get_automated_feedback(guess="abcde", ans="abcde") == "ggggg")
        assert(obj.get_automated_feedback(guess="abcde", ans="baecd") == "yyyyy")
        assert(obj.get_automated_feedback(guess="abcde", ans="aczzz") == "gxyxx")
    
    def TEST_get_wordle_score (self):
        get_word_list()
        obj = Evaluation()

        # these tests only word for current iteration (version 1.0)
        assert(obj.get_wordle_score("zymic") == 6)
        assert(obj.get_wordle_score("whale") == 6)
    
    def TEST_generate_evaluation (self):
        # won't work with generate_evaluation function that's released to prod
        # will only work with version 1.0
        get_word_list() # main algorithm functions rely on this being generated, does not affect test
        TEST_WORD_LIST = ["whale", "zymic", "earth"]
        obj = Evaluation()
        obj.generate_evaluation(TEST_WORD_LIST)
        assert(obj.min_score == 5)
        assert(obj.max_score == 6)
        assert(obj.total_guesses == 6 + 6 + 5)
        assert(obj.num_words == len(TEST_WORD_LIST))

    def run_tests (self):
        self.TEST_init()
        self.TEST_get_avg()
        self.TEST_get_automated_feedback()
        self.TEST_get_wordle_score()
        self.TEST_generate_evaluation()

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
        if isWin(feedback): report_win(guess)
        update_filter(feedback, guess)
    report_loss()

if __name__=="__main__":
    eval = Evaluation()
    eval.generate_evaluation()
    eval.report_evaluation()