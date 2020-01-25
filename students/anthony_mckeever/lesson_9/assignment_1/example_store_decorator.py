STORAGE = []


def store_result(func):
    def stored(*args, **kwargs):
        return_value = func(*args, **kwargs)
        STORAGE.append(return_value)
    return stored


# With this example, the value will be stored in
# STORAGE as opposed to being returned.
@store_result
def increment_value_stored(value):
    return value + 1


# With this example, the value will be returned.
def increment_value(value):
    return value + 1


if __name__ == "__main__":
    for i in range(10):
        increment_value_stored(i)
        print(increment_value(i))
    
    print(*STORAGE)
