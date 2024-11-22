import re

def find_first_and_second_integers(s):
    'Find integers and returns both as strings.'
    # Use regex to match the pattern for the integers
    pattern = r'\((\d+)\[(\d+)\]'
    match = re.search(pattern, s)

    if match:
        first_integer = int(match.group(1))
        second_integer = int(match.group(2))
        return str(first_integer), str(second_integer)
    else:
        return None, None