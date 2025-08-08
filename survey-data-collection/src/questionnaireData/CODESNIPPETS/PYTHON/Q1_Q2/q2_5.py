def send(self, data, flags=0):
    """
    Sends data over a network socket, using TCP or UDP based on socket type.
    
    Parameters
    ----------
    data
        The data to be sent over the network.
    flags
        Optional flags for the send operation, default is 0.
    
    Returns
    -------
    :
        Returns the result of the send operation.
    
    """
    
    if self.soc_type == PacketType.TCP:
        return self._tcp_send(data, flags)
    return self._udp_send(data, flags)