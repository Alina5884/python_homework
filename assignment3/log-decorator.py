import logging
logger = logging.getLogger("parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(
            f"function: {func.__name__} positional parameters: {args} keyword parameters: {kwargs} return: {result}"
        )
        return result
    return wrapper

@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def all_true(*args):
    return True

@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

say_hello()
all_true(1, 2, 3, "x")
return_decorator(foo=123, bar="abc")