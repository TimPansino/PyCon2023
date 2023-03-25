
def spanish_inquisition():
    print("Nobody expects the Spanish Inquisition!")


def my_decorator(func):
    print(f"Decorating this function: {func}")
    return spanish_inquisition


@my_decorator
def hello_world():
    print("Hello, World!")
# hello_world = my_decorator(hello_world)


if __name__ == "__main__":
    hello_world()
    print(hello_world)
