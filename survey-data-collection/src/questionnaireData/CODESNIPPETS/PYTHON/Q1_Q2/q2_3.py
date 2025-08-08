def default(self, obj):
    """
    Custom JSON encoder for handling Enum objects.
    
    Parameters
    ----------
    obj
        The object to encode as JSON.
    
    Returns
    -------
    :
        A JSON-serializable representation of the object.
    
    """
    
    if isinstance(obj, Enum):
        return {"__enum__": str(obj)}
    return json.JSONEncoder.default(self, obj)