# project:wordle - formatting the list of prev wordle words for backtesting
# kieran hulsman
# aug 10

def get_raw () -> str:
    res = ""
    file = open("raw.txt", "r")
    for word in file:
        res += "{}".format(word)
    file.close()
    return res

def string_to_list (raw: str) -> list:
    return list(raw.split(" "))

def write_to_file (lst: list) -> None:
    file = open("answers.txt", "a")
    for word in lst:
        file.write("{}\n".format(word))
    file.close()

def main ():
    raw = get_raw()
    lower_case = raw.lower()
    word_list = string_to_list(lower_case)
    write_to_file(word_list)

main()