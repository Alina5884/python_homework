# Write your code here.

# Task 1:

def hello():
    return "Hello!"

print(hello())


# Task 2:

def greet(name):
    return (f"Hello, {name}!")

print(greet("Liam"))


# Task 3:

def calc(a, b, operation="multiply"):

    try:
        if operation == "multiply":
            return a * b

        elif operation == "add":
            return a + b

        elif operation == "subtract":
            return a - b

        elif operation == "divide":
            return a / b

        elif operation == "modulo":
            return a % b

        elif operation == "int_divide":
            return a // b

        elif operation == "power":
            return a ** b

        else:
            return "Invalid operation was provided."

    except ZeroDivisionError:
        return "You can't divide by 0!"

    except TypeError:
        return "You can't multiply those values!"

print(calc(8, 2, "multiply"))
print(calc(8, 2, "add"))
print(calc(8, 2, "subtract"))
print(calc(8, 2, "divide"))
print(calc(8, 2, "modulo"))
print(calc(8, 2, "int_divide"))
print(calc(8, 2, "power"))
print(calc(8, 2, "powerrr"))
print(calc(8, 0, "divide"))
print(calc("8", 2, "power"))


# Task 4:

def data_type_conversion(value, type):

    try:
        if type == "float":
            return float(value)

        elif type == "str":
            return str(value)

        elif type == "int":
            return int(value)

        else:
            return "Invalid type was provided."

    except ValueError:
            return (f"You can't convert {value} into a {type}.")

print(data_type_conversion(57, "float"))
print(data_type_conversion(12.78, "str"))
print(data_type_conversion("34", "int"))
print(data_type_conversion(906, "Oooo"))
print(data_type_conversion("eleven", "int"))


# Task 5:

def grade(*args):

    try:
        for i in args:
            if not isinstance(i, (int, float)):
                raise ValueError

        average = sum(args) / len(args)

        if average >= 90:
            return "A"

        elif average >= 80:
            return "B"

        elif average >= 70:
            return "C"

        elif average >= 60:
            return "D"

        else:
            return "F"

    except ValueError:
        return "Invalid data was provided."

print(grade(96, 95, 94))
print(grade(60, 88, 95))
print(grade(83, 59, 89))
print(grade(71, 85, 45))
print(grade(20, 65, 35))
print(grade("lime", "time", 35))


# Task 6:

def repeat(string, count):

    try:
        new_string = ""

        for i in range(count):
            new_string += string

        return new_string

    except Exception as e:
        return str(e)

print(repeat("Straighten Up!", 5))
print(repeat("Start Now!", 1))
print(repeat("Time is a choice!", 3))


# Task 7:

def student_scores(param, **kwargs):

    try:
        if param == "best":
            best_student = max(kwargs, key = kwargs.get)
            return best_student

        elif param == "mean":
            average_score = sum(kwargs.values()) / len(kwargs)
            return average_score

        else:
            return "Invalid parameter was provided!"

    except Exception as e:
        return str(e)

print(student_scores("best", Ford = 43, Green = 99, Broom = 68))
print(student_scores("mean", Ford = 43, Green = 99, Broom = 68))


# Task 8:

def titleize(string):

    small_words = [ "a", "on", "an", "the", "of", "and", "is", "in"]

    words = string.split()

    for i, word in enumerate(words):

        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()

        elif word.lower() not in small_words:
            words[i] = word.capitalize()

        else:
            words[i] = word.lower()

    return (" ".join(words))

print(titleize("failure is an opportunity"))


# Task 9:

def hangman(secret, guess):

    final_guess = ""

    for letter in secret:

        if letter in guess:
            final_guess += letter

        else: final_guess += "_"

    return final_guess

print(hangman("planet", "pn"))


# Task 10

def pig_latin(string):

    vowels = ["a", "e", "i", "o", "u"]
    words = string.split()
    result = []

    for word in words:
        if word[0] in vowels:
            new_word = word + "ay"

        elif "qu" in word:
            index = word.index("qu")
            new_word = word[index+2:] + word[:index+2] + "ay"

        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                i+=1

            new_word = word[i:] + word[:i] + "ay"

        result.append(new_word)

    return (" ".join(result))

print(pig_latin("time is elastic"))
print(pig_latin("i have a quick question"))