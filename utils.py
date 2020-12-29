def create_multi_dimensional_array(*sizes, default_value=None):
    if len(sizes) == 0:
        raise TypeError("create_multi_dimensional_array expected at list 1 positional argument, got 0")

    ret_val = []

    if len(sizes) == 1:
        for index in range(sizes[0]):
            ret_val.append(default_value)
        return ret_val

    for index in range(sizes[0]):
        ret_val.append(create_multi_dimensional_array(*sizes[1:], default_value))
    return ret_val
