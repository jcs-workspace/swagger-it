# ========================================================================
# $File: util.py $
# $Date: 2020-01-20 15:44:44 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

import pathlib

def getFileExtension(path):
    """Return the file PATH extension.

    @param { string } path : Target file path we are going to extract.
    """
    return pathlib.Path(path).suffix

def arrayToString(lst):
    """Convert LST to string.

    @param { Array } lst : List of object.
    """
    str = ""
    for item in lst:
        str += str(item)
        pass
    return str

def containInListEqual(item, lst):
    """Check if ITEM is one of the item in LST.

    @param { string } item : Item to check.
    @param { Array } lst : List of item to check.
    """
    for cur_item in lst:
        if cur_item == item:
            return True
    return False

def containInList(item, lst):
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
