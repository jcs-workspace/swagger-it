# ========================================================================
# $File: util.py $
# $Date: 2020-01-20 15:44:44 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

def containInList(path, lst):
    """Check if each item in LST inside the PATH.

    @param { typename } path : Path for major check.
    @param { typename } lst : List of string that will use to check.
    """
    for item in lst:
        if item in path:
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
