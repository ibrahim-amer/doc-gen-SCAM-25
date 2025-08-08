def shutdown(self, how=socket.SHUT_RDWR):
    """
    Shuts down the socket connection using the specified method.
    
    Parameters
    ----------
    how
        Specifies how to shut down the socket (default is SHUT_RDWR).
    
    Returns
    -------
    :
        Returns True if shutdown is successful, otherwise returns False.
    
    Raises
    ------
    Exception
        Catches any exception during the shutdown process.
    
    """
    
    try:
        self.sock.shutdown(how)
        return True
    except Exception:
        return False