@staticmethod
def to_enum(d):
    """
    Converts a dictionary to an enum member if it contains an "__enum__" key.
    
    Parameters
    ----------
    d
        A dictionary potentially containing an enum reference under the key "__enum__".
    
    Returns
    -------
    :
        The corresponding enum member or the original dictionary if no enum is found.
    
    """
    
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(globals()[name], member)
    else:
        return d