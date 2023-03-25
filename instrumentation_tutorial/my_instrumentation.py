import wrapt
from import_hooks import register_import_hook


def my_wrapper(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)
    return result + " - Wrapped!"


def instrument_my_imported_module(module):
    wrapt.wrap_function_wrapper(module, "my_function", my_wrapper)
    wrapt.wrap_function_wrapper(module, "MyClass.my_method", my_wrapper)


register_import_hook("my_imported_module", instrument_my_imported_module)


def main():
    import my_imported_module
    register_import_hook("my_imported_module", instrument_my_imported_module)

    print(my_imported_module.my_function())
    print(my_imported_module.MyClass().my_method())
    print(my_imported_module.my_object.my_method())


def main():
    from my_imported_module import my_function, my_object, MyClass
    register_import_hook("my_imported_module", instrument_my_imported_module)

    print(my_function())
    print(MyClass().my_method())
    print(my_object.my_method())


if __name__ == "__main__":
    main()

"""
my_function
my_method - Wrapped!
my_method - Wrapped!
"""