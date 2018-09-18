def return_none_if_error(func):
    """
    Decorator for handling exception within a method. Returns
    expected response from method on success otherwise `None`.

    Example Usage::
        @return_none_if_error
        def my_method(a, b):
            return a / b
    """
    def wrapper(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            value = None
        return value

    return wrapper
