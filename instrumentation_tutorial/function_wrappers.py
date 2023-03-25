import functools


def my_decorator_function(arg):
    def my_decorator(func):
        @functools.wraps(func)
        def my_function_wrapper(*args, **kwargs):
            print(f"Before ({arg = })")
            result = func(*args, **kwargs)
            print("After")
            return result

        return my_function_wrapper
    
    return my_decorator

@my_decorator_function(1)
def hello_world():
    print("Hello, World!")


if __name__ == "__main__":
    hello_world()
    print(hello_world)
