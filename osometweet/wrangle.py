"""
A collection of convenience functions for manipulating data.
"""

from collections.abc import MutableMapping

def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(dictionary: dict, parent_key: str = '', sep: str = '.'):
    """
    Flatten a nested dictionary (such as a Twitter data object).

    For example, convert the dictionary:
        {"a":{"b":{"c":1234}}}

    into:
        {'a.b.c': 1234}

    Parameters:
    ----------
    - dictionary (dict) : A dictionary object to flatten
    - parent_key (str) : The base string that will prefix all
        keys. Typically, left as and empty string (i.e., '')
        unless you know what you're doing.
    - sep (str) : The text you would like to separate key path items.
        Default is a period (i.e., ".")

    Returns:
    ----------
    - flat_dict (dict) : a flattened version of `dictionary`

    Raises:
    ----------
    - TypeError

    ---------
    Examples:

    # Create dictionary
    dictionary = {
        "a" : 1,
        "b" : {
            "c" : 2,
            "d" : 5
        },
        "e" : {
            "f" : 4,
            "g" : 3
        },
        "h" : 3
    }

    ### 1. Using function as is
    flatten_dict(dictionary)

    # Returns:
    {'a': 1, 'b.c': 2, 'b.d': 5, 'e.f': 4, 'e.h': 3, 'i': 3}

    ~~~
    ### 2. Changing `parent_key`
    # Parent key will add `parent_key` as a prefix to all keys
    flatten_dict(dictionary, parent_key = "NEW")

    # Returns
    {'NEW.a': 1, 'NEW.b.c': 2, 'NEW.b.d': 5,
    'NEW.e.f': 4, 'NEW.e.h': 3, 'NEW.i': 3}

    ~~~
    ### 3. Changing `sep`
    # This string is what will separate key path strings
    flatten_dict(dictionary, sep = "/")

    # Returns
    {'a': 1, 'b/c': 2, 'b/d': 5, 'e/f': 4, 'e/h': 3, 'i': 3}

    """
    if not isinstance(dictionary, dict):
        raise TypeError(
            "`dictionary` must be of type `dict`")
    flat_dict = dict(_flatten_dict_gen(dictionary, parent_key, sep))
    return flat_dict


def get_dict_paths(dictionary: dict, path: list = []):
    """
    Return a generator which iterates over all full
    key paths within `dictionary`.

    Parameters:
    ----------
    - dictionary (dict) : this is the dictionary you'd like to pass
    - path (list) : Typically left as an empty list. If not, the dictionary
        key paths will all append to the provided list.

    Returns:
    ----------
    - generator

    Raises:
    ----------
    - TypeError

    Example:
    ----------

    # Create dictionary
    dictionary = {
        "a" : 1,
        "b" : {
            "c" : 2,
            "d" : 5
        },
        "e" : {
            "f" : 4,
            "g" : 3
        },
        "h" : 3
    }

    # Call get_dict_paths
    print(list(get_dict_paths(dictionary)))

    # Returns
    [['a'], ['b', 'c'], ['b', 'd'], ['e', 'f'], ['e', 'g'], ['h']]

    """
    if not isinstance(path, list):
        raise TypeError("`path` must be of type `list`")

    if not isinstance(dictionary, dict):
        yield path
    else:
        yield from [
            new for key, val in dictionary.items()
            for new in get_dict_paths(val, path + [key])
        ]


def get_dict_val(dictionary: dict, key_list: list = []):
    """
    Return `dictionary` value at the end of the key path provided
    in `key_list`.

    Indicate what value to return based on the key_list provided.
    For example, from left to right, each string in the key_list
    indicates another nested level further down in the dictionary.
    If no value is present, a `None` is returned.

    Parameters:
    ----------
    - dictionary (dict) : the dictionary object to traverse
    - key_list (list) : list of strings indicating what dict_obj
        item to retrieve

    Returns:
    ----------
    - key value (if present) or None (if not present)

    Raises:
    ----------
    - TypeError

    Examples:
    ---------
    # Create dictionary
    dictionary = {
        "a" : 1,
        "b" : {
            "c" : 2,
            "d" : 5
        },
        "e" : {
            "f" : 4,
            "g" : 3
        },
        "h" : 3
    }

    ### 1. Finding an existing value
    # Create key_list
    key_list = ['b', 'c']

    # Execute function
    get_dict_val(dictionary, key_list)

    # Returns
    2

    ~~~

    ### 2. When input key_path doesn't exist

    # Create key_list
    key_list = ['b', 'k']

    # Execute function
    value = get_dict_val(dictionary, key_list)

    # Returns NoneType because the provided path doesn't exist
    type(value)
    NoneType
    """

    if not isinstance(dictionary, dict):
        raise TypeError("`dictionary` must be of type `dict`")

    if not isinstance(key_list, list):
        raise TypeError("`key_list` must be of type `list`")

    retval = dictionary
    for k in key_list:

        # If retval is not a dictionary, we're going too deep
        if not isinstance(retval, dict):
            return None

        if k in retval:
            retval = retval[k]

        else:
            return None
    return retval
