def make_hangman(secret_word):
    secret = secret_word.lower()
    guesses = []
    def hangman_closure(letter):
        l = letter.lower()
        guesses.append(l)
        shown = "".join(ch if ch in guesses else "_" for ch in secret)
        print(shown)
        return all(ch in guesses for ch in secret)
    return hangman_closure

secret = input("Enter the secret word: ")
game = make_hangman(secret)
print("Start guessing letters.")
while True:
    g = input("Your guess: ")
    if not g:
        continue
    if game(g):
        print("You got it!")
        break