''' Errors '''

class AccessError(Exception):
    ''' Empty access error '''
    # pass

# raises TypeError if value is not a valid string,
# othwise returns the string value
def check_str(value, name):
    ''' Check if a given value is a string '''
    if value is None or not isinstance(value, str):
        raise TypeError(name + ' is not a string')
    return str(value)

# raises TypeError if value is not a valid integer,
# othwise returns the integer value
def check_int(value, name):
    ''' Check if a given value is an integer '''
    if value is None or (not isinstance(value, int) and not value.isdigit()):
        raise TypeError(name + ' is not an integer')
    return int(value)

# raises ValueError if the given condition is false
def check(condition, error):
    ''' Check if a condition is false '''
    if not condition:
        raise ValueError(error)
