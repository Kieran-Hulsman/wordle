# kieran hulsman
# wordle solver

# global variables (filters)
gray = set()
green = ['','','','','']
yellow_indexed = [[],[],[],[],[]]
yellow_set = set()

def get_guess () -> str:
    pass

def get_feedback (guess: str) -> str:
    pass

def update_filter (feedback: str) -> None:
    pass

def main ():
    for i in range(6):
        guess = get_guess()
        feedback = get_feedback(guess)
        update_filter(feedback)

if __name__=="__main__":
    main()