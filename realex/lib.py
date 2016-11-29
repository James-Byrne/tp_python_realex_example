import random


def remove_decimal_places(number):
    return str(int(float(number) * 100))


def generate_random_alphanumeric_string(length):
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(length))


def remove_white_space(param):
    return param.replace(" ", "")


def generate_basic_xml_headers():
    return {'Content-Type': 'application/xml'}
