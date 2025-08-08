def _check_http_port(self, address):
    """
    Checks if the HTTP port of the given address is within the allowed ranges.
    
    Parameters
    ----------
    address
        The URL or address to check the HTTP port for.
    
    Returns
    -------
    :
        Returns True if the port is valid, otherwise returns False.
    
    Raises
    ------
    Exception
        Catches all exceptions that may occur during execution.
    
    """
    
    try:
        if not self.ranges_are_set:
            return True

        parsed = urlparse(address)
        port = parsed.port
        if not port:
            port = 443 if parsed.scheme == 'https' else 80

        return port in self.ranges
    except Exception:
        return False