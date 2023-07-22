# kieran hulsman
# july 22
# file io testing for project: wordle

words = []
file = open("test.txt", "r")
for line in file:
    for word in line.split():
        words.append(word)

print(words)