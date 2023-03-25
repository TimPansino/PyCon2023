import wrapt


@wrapt.function_wrapper
def my_function_wrapper(wrapped, instance, args, kwargs):
    print(f"Before")
    result = wrapped(*args, **kwargs)
    print("After")
    return result


@my_function_wrapper
def hello_world():
    print("Hello, World!")


if __name__ == "__main__":
    hello_world()
    print(hello_world)
    print(type(hello_world))
