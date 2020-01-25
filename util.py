# ========================================================================
# $File: util.py $
# $Date: 2020-01-20 15:44:44 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

import pathlib

def warn_exists(id, checker):
    """Warn the non-existence for ID without the CHECKER exists."""
    print(f'[WARNING] Defined `{id}` without `{checker}` defined')
    pass

def safe_get_value(lst, index):
    """Safe get the value from a LST with INDEX."""
    if index >= 0 and index < len(lst):
        return lst[index]
    return None

def none_string(vr, def_str, none_str = ""):
    """Return DEF_STR or NONE_STR depends on weather VR is None or empty string.

    @param { any } vr : Any variable you want to check.
    @param { string } def_str : Default string.
    @param { string } none_str : None string.
    """
    if vr is None or vr is "" or vr is False:
        return none_str
    return def_str

def len_zero_string(lst, def_str, zero_str = ""):
    """Return DEF_STR or ZERO_STR depends on LST's length is 0 or not.

    @param { Array } lst : List to get the length.
    @param { string } def_str : Default string.
    @param { string } zero_str : Zero string.
    """
    if len(lst) is 0:
        return zero_str
    return def_str

def dict_get_value(dic, key):
    """Get the key value.

    @param { Dictionary } dic : Dictionary use to get.
    @param { string } key : Key to get value.
    """
    if dict_key_exists(dic, key):
        return dic[key]
    return None

def dict_key_exists(dic, key):
    """Check if the KEY exist in DIC.

    @param { Dictionary } dic : Dictionary use to check.
    @param { string } key : Key to check.
    """
    return key in dic

def get_file_extension(path):
    """Return the file PATH extension.

    @param { string } path : Target file path we are going to extract.
    """
    return pathlib.Path(path).suffix

def array_to_string(lst):
    """Convert LST to string.

    @param { Array } lst : List of object.
    """
    form_str = ""
    for item in lst:
        form_str += str(item)
        pass
    return form_str

def contain_in_list_equal(item, lst):
    """Check if ITEM is one of the item in LST.

    @param { string } item : Item to check.
    @param { Array } lst : List of item to check.
    """
    for cur_item in lst:
        if cur_item == item:
            return True
    return False

def contain_in_list(item, lst):
    """Check if each item in LST inside the ITEM.

    @param { string } item : Path for major check.
    @param { Array } lst : List of string to check.
    """
    for cur_item in lst:
        if cur_item in item:
            return True
    return False

class ArgumentError(LookupError):
    """Argument input error."""
    pass

def mkdir_safe(path):
    """Make directory if not exists.

    @param { string } path : Directory path.
    """
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    pass

def args_input(input):
    """Return the default input path.

    @param { string } input : Default input argument.
    """
    if input is None:
        return os.path.dirname(os.path.abspath(__file__))
    return input
