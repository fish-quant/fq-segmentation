# Imports
from pathlib import Path
import re


# Log message
def log_message(msg, callback_fun=None):
    """ Display log, either terminal or any callback accepting a string as input.

    Parameters
    ----------
    msg : [string]
        [description]
    callback_fun : [type], optional
        [description], by default None
    """
    if callback_fun:
        callback_fun(msg)
    else:
        print(msg)


# Create new output path
def create_output_path(path_orig, str_replace, subfolder=None, create_path=True, callback_log=None):
    """ Allows to create new path object by replacing a string in a provided path object.

    Parameters
    ----------
    path_orig : pathlib object
        Original file-name.
    str_replace : str
        str defining the replacement operation: 'str_orig>>str_new',
        where 'str_orig' is the orginal string, 'str_new' is the new string.
        For example, 'acquisition>>analysis'.
    subfolder : str or pathlib object
        Subfolder that should be added to new file-name
    create_path : bool
        Create new path if it doesn't exist.
    callback_log : str
        Callback function to be used. If None, then system print will be used.

    Returns
    -------
    pathlib object
        New path.
    """

    log_message("Creating name to path to store data.", callback_fun=callback_log)

    if (re.search(">>", str_replace)):
        str_orig = re.search(r'^(.*)>>(.*)$', str_replace).group(1)
        str_rep = re.search(r'^(.*)>>(.*)$', str_replace).group(2)

        path_replace = Path(str(path_orig).replace(str_orig, str_rep))

        if subfolder:
            path_replace = path_replace / subfolder

        log_message(f'Replacement parameters found: original string: {str_orig}, replacement string: {str_rep}', callback_fun=callback_log)
        log_message(f'Output path: {path_replace}', callback_fun=callback_log)

    else:
        log_message("No match", callback_fun=callback_log)
        return None

    # Create default folder to save data if none was defined by the user
    if create_path:
        if not path_replace.is_dir():
            path_replace.mkdir(parents=True)

    return path_replace