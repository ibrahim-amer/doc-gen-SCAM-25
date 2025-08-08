def __init__(self, message):
    """
    Initializes a ClientError instance with a specified error message.
    
    Parameters
    ----------
    message
        The error message to be associated with the ClientError instance.
    
    """
    
    self.message = message
    super(ClientError, self).__init__(message)