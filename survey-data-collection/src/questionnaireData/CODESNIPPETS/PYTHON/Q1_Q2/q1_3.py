def __str__(self):
    """
    Return a string representation of the Client object with its address, port, and type.
    
    Returns
    -------
    :
        A formatted string containing the client's address, port, and type.
    
    """
    
    return "Client<addr={}|port={}|type={}>".format(self.addr, self.port, self.soc_type)