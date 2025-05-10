def map_value(x, in_min, in_max, out_min, out_max):
    if x < in_min:
        return out_min
    elif x > in_max:
        return out_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

print(map_value(float(input()), 2, 10, 2, 3.3))