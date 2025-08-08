def _udp_send(self, data, flags=0):
    """
    Sends data to a specified address and port using UDP.
    
    Parameters
    ----------
    data
        The data to be sent over UDP.
    flags
        Optional flags for the send operation, default is 0.
    
    Returns
    -------
    :
        The number of bytes sent.
    
    """
    
    return self.sock.sendto(data, flags, (self.addr, self.port))