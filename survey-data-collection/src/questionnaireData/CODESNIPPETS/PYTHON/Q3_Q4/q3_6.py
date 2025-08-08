def _tcp_connect(self):
    """
    Establishes a TCP connection to a specified address and port.
    
    Raises
    ------
    socket.timeout
        Raised when the connection attempt times out.
    OSError
        Raised for system-related errors during the connection.
    
    """
    
    try:
        self.sock.settimeout(self.connect_timeout)
        self.sock.connect((self.addr, self.port))
        self.sock.settimeout(None)
    except socket.timeout as t:
        raise ClientError('connect: {}'.format(t))
    except OSError as e:
        self.sock.close()
        code = errno.errorcode.get(e.errno, e.errno)
        raise ClientError('connect: {}: {}'.format(code, e.strerror))