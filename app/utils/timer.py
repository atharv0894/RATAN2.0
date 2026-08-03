import time
from functools import wraps
from typing import Any, Callable

def time_it(func: Callable) -> Callable:
    """Decorator to measure execution time of a function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper
