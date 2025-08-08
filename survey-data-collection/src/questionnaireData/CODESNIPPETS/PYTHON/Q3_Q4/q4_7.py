def reconnect(self, address=None, port=None):
    """
    Establishes a connection to a server using the specified address and port.
    
    Parameters
    ----------
    address
        The server address to connect to, defaults to instance address.
    port
        The server port to connect to, defaults to instance port.
    
    Raises
    ------
    ClientError
        Raised when the client fails to connect to the server.
    ProtocolClientException
        Custom exception for protocol client connection errors.
    
    """

    if not self.client or (self.client and self.client._fd() == -1):  # pragma: no branch
        if address is None:  # pragma: no branch
            address = self.address
        if port is None:  # pragma: no branch
            port = self.port
        try:
            if self.client:
                self.client = None
            self.client = Client(address, port, timeout=5)
            self.address = address
            self.port = port
        except ClientError as e:
            raise ProtocolClientException(
                "ProtocolClient: Failed to connect to server. ({})".format(e))
        self._start()