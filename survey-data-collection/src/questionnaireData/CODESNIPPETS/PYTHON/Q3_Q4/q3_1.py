def set_soc_type(self, soc_type):
    """
    Sets the socket type for the connection and reinitializes the socket if changed.
    
    Parameters
    ----------
    soc_type
        The socket type to be set (TCP or UDP).
    
    """
    

    if soc_type != PacketType.TCP and soc_type != PacketType.UDP:
        return

    if soc_type == self.soc_type:
        return

    self.shutdown()
    self.sock.close()
    self.soc_type = soc_type
    self._sock = socket.socket(socket.AF_INET, self.socket_types[soc_type])
    if soc_type == PacketType.TCP:
        self._tcp_connect()