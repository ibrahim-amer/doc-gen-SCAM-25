def _fd(self):
    """
    Retrieve the file descriptor for the socket.
    
    Returns
    -------
    :
        Returns the socket file descriptor or -1 if an error occurs.
    
    Raises
    ------
    Exception
        Catches any exception that occurs when accessing the socket file descriptor.
    
    """
    
    try:
        return self.sock.fileno()
    except Exception:
        return -1