import secrets
import string
import base64


def generate_random_string(number_of_symbols, type_of_symbols):
    """
    Generates a string of certain length with certain characters
    :param number_of_symbols: string length
    :param type_of_symbols: character types
    :return: str
    """
    return ''.join(secrets.choice(type_of_symbols) for i in range(number_of_symbols))


def generate_user_data(number_of_symbols):
    """
    Generates a password with whitespaces
    :return: str
    """
    alphabet = string.ascii_letters + string.digits
    return generate_random_string(number_of_symbols, alphabet)


def encode_password(password):
    """
    Creates string encoded in base64
    :return: str
    """
    return base64.b64encode(password.encode()).decode("utf-8")
