def __str__(self):
    """
    Return a string representation of the EmailClient instance.
    
    Returns
    -------
    :
        A formatted string displaying the email address and port of the client.
    
    """
    
    return "<EmailClient(address={}|port={})>".format(self.address, self.port)
    