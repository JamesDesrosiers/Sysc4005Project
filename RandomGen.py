import numpy as np
import time
import datetime
import pandas


def uni_rand_gen(size):
    """
    Generates an array of random values
    :param size: The number of randomly generated values
    :return: An array of random uniform values
    """
    mod, multi = curr_date_int()
    seed = int(time.time())
    rand_vals = np.zeros(size)
    rand_val = (seed * multi + 1) % mod
    rand_vals[0] = rand_val / mod
    for i in range(1, size):
        rand_val = (rand_val * multi + 1) % mod
        rand_vals[i] = rand_val / mod
    return rand_vals


def uni_rand_gen_range(low, high, size):
    """
    Generates an array of random values between the ranges of low and high
    :param low: The lowest possible value
    :param high: The highest possible value
    :param size: The number of generated values
    :return: An array of random values between the ranges of low and high
    """
    rand_vals = uni_rand_gen(size)
    for index in range(0, len(rand_vals)):
        rand_vals[index] = low + (high - low) * rand_vals[index]
    return rand_vals


def curr_date_int():
    """
    Generates a value from the current date and a value from the current time of the day
    :return: a value generated from the current date and a value generated from the current time of the day
    """
    today = datetime.datetime.now()
    date_val = int(today.strftime("%Y") + today.strftime("%M") + today.strftime("%d"))
    time_val = int(today.strftime("%H") + today.strftime("%m") + today.strftime("%S"))
    return date_val, time_val


def exp_rand_gen(lamb, size):
    """
    Generates an array of random values following an exponential distribution.
    :param lamb: The value of lambda used in the Inverse Transformation Technique
    :param size: The number of values generated
    :return: An array of random values that follow an exponential distribution
    """
    rand_vals = uni_rand_gen(size)
    for index in range(0, len(rand_vals)):
        rand_vals[index] = -(np.log(1 - rand_vals[index])) / lamb

    return rand_vals


def exp_rand_gen_range(lamb, low, high, size):
    """
    Generates an arroy of random values between the low and high values following an exponential distribution.
    :param lamb: The value of lambda used in the Inverse Transformation Technique
    :param low: The lowest possible value
    :param high: The highest possible value
    :param size: The number of generated values
    :return: An array of random values between the ranges of low and high
    """
    rand_vals = exp_rand_gen(lamb, size)
    for index in range(0, len(rand_vals)):
        rand_vals[index] = low + (high - low) * rand_vals[index]

    return rand_vals


if __name__ == "__main__":
    num_samples = 300
    inspect1_c1_rand = exp_rand_gen_range(10.35791, 0.087, 76.284, num_samples)
    inspect2_c2_rand = exp_rand_gen_range(15.58843, 0.13, 114.43, num_samples)
    inspect2_c3_rand = exp_rand_gen_range(20.63276, 0.031, 104.02, num_samples)
    ws1_rand = exp_rand_gen_range(4.604417, 0.007, 29.375, num_samples)
    ws2_rand = exp_rand_gen_range(10.93212, 0.091, 59.078, num_samples)
    ws3_rand = exp_rand_gen_range(8.79558, 0.102, 51.418, num_samples)
    dictionary = {
        'Inspector 1 C1': inspect1_c1_rand,
        'Inspector 2 C2': inspect2_c2_rand,
        'Inspector 2 C3': inspect2_c3_rand,
        'Workstation 1': ws1_rand,
        'Workstation 2': ws2_rand,
        'Workstation 3': ws3_rand
    }
    df = pandas.DataFrame.from_dict(dictionary)
    df.to_csv('rand_gen_test.csv')
    print(df)

