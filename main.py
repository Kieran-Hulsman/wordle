# kieran hulsman
# wordle solver
# version 2.0 - updating algo
import copy

word_list = [] # from text file
INITIAL_GUESS = "slate"

class Filter ():
    def __init__ (self):
        self.gray = set()
        self.green = ['', '', '', '', '']
        self.yellow_indexed = [[], [], [], [], []]
        self.yellow_set = set()
        assert(self.isEmpty())

    def update (self, feedback: str, guess: str) -> None:
        for i,c in enumerate(feedback):
            if c == 'x': self.gray.add(guess[i])
            elif c == 'g': self.green[i] = guess[i]
            elif c == 'y':
                self.yellow_set.add(guess[i])
                self.yellow_indexed[i].append(guess[i])
            else:
                exit(1)

    def report_status (self) -> None:
        gray_list = list(self.gray)
        gray_list.sort()
        yellow_list = list(self.yellow_set)
        yellow_list.sort()
        
        print("\n---FILTER STATUS START---")
        print("green: {}".format(self.green))

        print("yellow set: {}".format(self.yellow_list))
        print("yellow indexed: {}".format(self.yellow_indexed))

        print("gray: {}".format(self.gray_list))
        print("---FILTER STATUS END  ---\n")

    # resets filter
    def clear (self) -> None:
        self.gray = set()
        self.green = ['', '', '', '', '']
        self.yellow_indexed = [[], [], [], [], []]
        self.yellow_set = set()
        assert(self.isEmpty())

    def isEmpty (self) -> bool:
        if len(self.gray) > 0: return False
        if len(self.yellow_set) > 0: return False
        
        green_isEmpty = True
        for letter in self.green:
            if letter != '': 
                green_isEmpty = False
        
        return green_isEmpty
    
    def TEST_isEmpty (self):
        obj = Filter()
        assert(obj.isEmpty())
        
        obj.gray.add('a')
        assert(not obj.isEmpty())
        obj.clear()

        obj.green[4] = 'a'
        assert(not obj.isEmpty())
        obj.clear()

        obj.yellow_set.add('a')
        assert(not obj.isEmpty())

    def TEST_update (self):

        self.update("xxxxx", "abcde")
        assert('a' in self.gray)
        assert('b' in self.gray)
        assert('c' in self.gray)
        assert('d' in self.gray)
        assert('e' in self.gray)
        self.clear()

        self.update("yyyyy", "abcde")
        assert('a' in self.yellow_set)
        assert('b' in self.yellow_set)
        assert('c' in self.yellow_set)
        assert('d' in self.yellow_set)
        assert('e' in self.yellow_set)
        assert(len(self.yellow_indexed[0])==1 and self.yellow_indexed[0][0]=='a')
        assert(len(self.yellow_indexed[1])==1 and self.yellow_indexed[1][0]=='b')
        assert(len(self.yellow_indexed[2])==1 and self.yellow_indexed[2][0]=='c')
        assert(len(self.yellow_indexed[3])==1 and self.yellow_indexed[3][0]=='d')
        assert(len(self.yellow_indexed[4])==1 and self.yellow_indexed[4][0]=='e')
        self.clear()

        self.update("ggggg", "abcde")
        assert(self.green[0]=='a')
        assert(self.green[1]=='b')
        assert(self.green[2]=='c')
        assert(self.green[3]=='d')
        assert(self.green[4]=='e')
        self.clear()

        self.update("xxygx", "abcde")
        assert('a' in self.gray)
        assert('b' in self.gray)
        assert('c' in self.yellow_set)
        assert(len(self.yellow_indexed[2])==1 and self.yellow_indexed[2][0]=='c')
        assert(self.green[3]=='d')
        assert('e' in self.gray)
        self.clear()

def isFirstGuess (filter: Filter) -> bool:
    return filter.isEmpty()

def get_word_list ():
    global word_list

    file = open("valid-wordle-words.txt", "r")
    for line in file:
        for word in line.split():
            word_list.append(word)

def isValidGuess (guess: str, filter: Filter) -> bool:
    # green
    for i,letter in enumerate(guess):
        if filter.green[i] != '' and letter != filter.green[i]:
            return False

    # gray
    for i,letter in enumerate(guess):
        if letter in filter.gray and letter != filter.green[i]: 
            return False

    # yellow set (guess must contain yellow letters)
    for yellow_letter in filter.yellow_set:
        isValid = False
        for i,guess_letter in enumerate(guess):
            if guess_letter == yellow_letter and guess_letter != filter.green[i]:
                isValid = True
        if not isValid: return False
    
    # yellow indexed (letters must not be in the same index as yellow letters)
    for i,letter in enumerate(guess):
        for yellow_letter in filter.yellow_indexed[i]:
            if letter == yellow_letter: return False
  
    return True

# the algorithm
def get_guess (filter: Filter) -> str:
    if isFirstGuess(filter): return INITIAL_GUESS

    UNINITALIZED_VALUE = ''
    TOTAL_NUM_WORDS = 14855

    res = UNINITALIZED_VALUE
    min_words_remaning = TOTAL_NUM_WORDS

    for word in word_list:
        if isValidGuess(word, filter):
            predicted_words_remaining = get_predicted_words_remaining(word, filter)

            if predicted_words_remaining < min_words_remaning:
                res = word
                min_words_remaning = predicted_words_remaining
    
    if res == UNINITALIZED_VALUE: assert(0)
    return res

def get_words_remaining (filter: Filter) -> int:
    res = 0
    for word in word_list:
        if isValidGuess(word, filter): res += 1
    return res

def get_predicted_words_remaining (guess: str, filter: Filter) -> int:
    temp_filter = copy.deepcopy(filter)
    temp_filter.update(get_predicted_feedback(guess, temp_filter), guess)
    return get_words_remaining(temp_filter)

# pre: guess is valid
def get_predicted_feedback (guess: str, filter: Filter) -> str:
    res = ""
    for i,letter in enumerate(guess):
        if letter == filter.green[i]: res += 'g'
        elif letter in filter.yellow_set: res += 'y'
        else: res += 'x'
    return res

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

# algo testing
class Test ():
    def __init__ (self):
        self.filter = Filter()
        get_word_list()

    def TEST_get_word_list (self):
        for word in word_list:
            print(word)
    
    def TEST_isValidGuess (self):
        assert(self.filter.isEmpty())
        assert(isValidGuess(INITIAL_GUESS, self.filter))
        self.filter.clear()

        self.filter.update("xxxxx", "abcde")
        assert(not isValidGuess("abcde", self.filter))
        self.filter.clear()

        self.filter.update("gxxxx", "abcde")
        assert(not isValidGuess("zzzzz", self.filter))
        assert(isValidGuess("azzzz", self.filter))
        self.filter.clear()

        self.filter.update("yxxxx", "abcde")
        assert(not isValidGuess("azzzz", self.filter))
        assert(not isValidGuess("zzzzz", self.filter))
        assert(isValidGuess("zazzz", self.filter))
        self.filter.clear()

        self.filter.update("xxxyx", "adieu")
        assert(not isValidGuess("louse", self.filter))
        assert(isValidGuess("froze", self.filter))
        self.filter.clear()

        self.filter.update("xxxyx", "adieu")
        self.filter.update("xyxyx", "bebop")
        assert(not isValidGuess("check", self.filter))
        self.filter.clear()

        # green/gray duplicate test
        self.filter.update("xggxy", "carat")
        assert(isValidGuess("party", self.filter))
        assert(not isValidGuess("aarty", self.filter))
        self.filter.clear()

        # green/yellow duplicate test
        self.filter.update("yggyx", "aarty")
        assert(isValidGuess("carat", self.filter))
        assert(not isValidGuess("aarat", self.filter))
        assert(not isValidGuess("aarxt", self.filter))
        assert(not isValidGuess("carxt", self.filter))
        self.filter.clear()

        self.filter.update("xygxg", "slate")
        self.filter.update("xxggg", "veale")
        assert(isValidGuess("whale", self.filter))
        self.filter.clear()

    def TEST_get_guess (self):
        assert(get_guess(self.filter) == INITIAL_GUESS)
        self.filter.update("xxxyx", INITIAL_GUESS)
        print(get_guess(self.filter))
        self.filter.clear()

    def TEST_get_feedback (self):
        feedback = get_feedback(INITIAL_GUESS)
        print("\n\nTEST result: {}".format(feedback))

    # only works for version2.0
    def TEST_get_predicted_feedback (self):
        filter = Filter()

        filter.update("xxxxx", "abcde")
        assert(get_predicted_feedback("fghij", filter) == "xxxxx")
        filter.clear()

        filter.update("yxxxx", "abcde")
        assert(get_predicted_feedback("zaaaa", filter) == "xyyyy")
        assert(get_predicted_feedback("zafgh", filter) == "xyxxx")
        filter.clear()

        filter.update("xxxxg", "abcde")
        assert(get_predicted_feedback("fghie", filter) == "xxxxg")
        filter.clear()

    def TEST_isWin (self):
        assert(not isWin("ggggy"))
        assert(isWin("ggggg"))

    def TEST_report_win (self):
        report_win(INITIAL_GUESS)

    def TEST_report_loss (self):
        report_loss()

    def run_tests (self):
        # self.TEST_get_word_list()
        self.TEST_isValidGuess()
        # self.TEST_get_guess()
        # self.TEST_get_feedback()
        self.TEST_get_predicted_feedback()
        self.TEST_isWin()
        # self.TEST_report_win()
        # self.TEST_report_loss()

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
        UNINITIALIZED_VALUE = ''
        res_list = [UNINITIALIZED_VALUE]*5
        
        ans_map = {}
        for letter in ans:
            if letter in ans_map:
                ans_map[letter] += 1
            else:
                ans_map[letter] = 1

        # green letters (fixes yellow/green bug)
        for i,c in enumerate(guess):
            if c == ans[i]:
                res_list[i] = 'g'
                ans_map[c] -= 1

        # yellow and gray letters
        for i,c in enumerate(guess):
            if res_list[i] == UNINITIALIZED_VALUE:
                if c in ans_map and ans_map[c] > 0: 
                    res_list[i] = 'y'
                else: 
                    res_list[i] = 'x'
        
        return ''.join(res_list)
    
    def get_wordle_score (self, ans: str) -> int:
        filter = Filter()
        for i in range(1000):
            guess = get_guess(filter)
            feedback = self.get_automated_feedback(guess, ans)
            if isWin(feedback): return i+1
            filter.update(feedback, guess)
        exit(1)

    # param word_list: used to test on smaller data set
    def generate_evaluation (self, word_list) -> None:
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
        ACCEPTABLE_ERR = 0.01
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

        # green/gray duplicate
        assert(obj.get_automated_feedback(guess="carat", ans="party") == "xggxy")
        assert(obj.get_automated_feedback(guess="tarac", ans="ytrap") == "yxggx")

        # green/yellow duplicate
        assert(obj.get_automated_feedback(guess="aarty", ans="carat") == "yggyx")
        assert(obj.get_automated_feedback(guess="ytraa", ans="tarac") == "xyggy")


    def TEST_get_wordle_score (self):
        # only works with version 1.0
        obj = Evaluation()

        # these tests only word for current iteration (version 1.0)
        # assert(obj.get_wordle_score("zymic") == 6)
        # assert(obj.get_wordle_score("whale") == 6)
    
    def TEST_generate_evaluation (self):
        # won't work with generate_evaluation function that's released to prod
        # will only work with version 1.0
        TEST_WORD_LIST = ["whale", "zymic", "earth"]
        obj = Evaluation()
        obj.generate_evaluation(TEST_WORD_LIST)
        print("min score: {}".format(obj.min_score))
        print("max score: {}".format(obj.max_score))

        # assert(obj.min_score == 5)
        # assert(obj.max_score == 6)
        # assert(obj.total_guesses == 6 + 6 + 5)
        
        assert(obj.num_words == len(TEST_WORD_LIST))

    def run_tests (self):
        self.TEST_init()
        self.TEST_get_avg()
        self.TEST_get_automated_feedback()
        self.TEST_get_wordle_score()
        self.TEST_generate_evaluation()

def main ():
    filter = Filter()
    get_word_list()
    for i in range(6):
        guess = get_guess(filter)
        feedback = get_feedback(guess)
        if isWin(feedback): report_win(guess)
        filter.update(feedback, guess)
    report_loss()

if __name__=="__main__":
    test = Test()
    test.TEST_isValidGuess()
    # eval = Evaluation()
    # eval.run_tests()
    # eval.generate_evaluation(word_list)
    # eval.report_evaluation()