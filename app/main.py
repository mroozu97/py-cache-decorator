from typing import Callable
from functools import wraps


def cache(func: Callable) -> Callable:
    cache_storage = {}

    @wraps(func)
    def wrapper(*args) -> any:
        # Convert unhashable arguments (like lists) to tuples
        hashable_args = tuple(
            tuple(arg) if isinstance(arg, list) else arg for arg in args
        )

        if hashable_args in cache_storage:
            print("Getting from cache")
            return cache_storage[hashable_args]
        else:
            print("Calculating new result")
            result = func(*args)
            cache_storage[hashable_args] = result
            return result

    return wrapper


@cache
def long_time_func(first: int, second: int, third: int) -> int:
    if first == 0 or third == 0:
        raise ValueError("first and third must be "
                         "nonzero to avoid ZeroDivisionError")
    return (first ** second ** third) % (first * third)


@cache
def long_time_func_2(n_tuple: tuple, power: int) -> list[int]:
    return tuple(number ** power
                 for number in n_tuple)  # Convert list to tuple for caching


# Test cases
test1 = long_time_func(1, 2, 3)
test2 = long_time_func(2, 2, 3)
test3 = long_time_func_2((5, 6, 7), 5)
test4 = long_time_func(1, 2, 3)  # Should retrieve from cache
test5 = long_time_func_2((5, 6, 7), 10)
test6 = long_time_func_2((5, 6, 7), 10)  # Should retrieve from cache

print(test1, test2, test3, test4, test5, test6)
