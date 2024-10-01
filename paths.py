
import os
from typing import Optional, Union, TypeAlias

Pathname: TypeAlias = Union[str,  bytes, os.PathLike]

def expand_path(path: Pathname, basedir: Optional[Pathname] = None) -> Pathname:
    """Return an absolute pathname, relative to basedir or cwd

    Parameters
    ----------
    path : Pathname
        pathname
        
    basedir : Optional[Pathname], default: :py:func:`os.getcwd()`
        base directory for relative pathnames. If not provided or
        provided as a *falsey* value,then the value of 
        `os.getcwd()` will be applied as the effective `basedir`.

    Returns
    -------
    Pathname
        the absolute pathname
        
    Description
    -------
    
    - If `path` denotes an absolute pathname, returns `path`.
    - if `path` is prefixed with a home directory for an
      existing *username* on the *host*, e.g with prefix `~/` 
      or `~username/`,  returns the path as expanded relative
      to the respective homedir.
    - Lastly, returns the path as expanded for the effective
      `basedir`.
      
    The value of `basedir` may be provided as a user homedir
    pathname, with a prefix such as `"~/"` or `"~username/"`.
    
    Known Limitations
    -------
    
    - If provided with a `path` or a `basedir` in a syntax such
      as `~non/file` and the user `non` does not exist on the 
      *host*, then the `path` value will be interpeted as a 
      relative pathname under the effective `basedir`.
    """
    if os.path.isabs(path):
        return path
    user_path: Pathname = os.path.expanduser(path)
    if os.path.isabs(user_path):
        return user_path
    basepath: Pathname = os.path.expanduser(basedir) if basedir else os.getcwd()
    assert os.path.isabs(basepath)
    return os.path.abspath(os.path.join(basepath, path))
