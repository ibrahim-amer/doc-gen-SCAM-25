def _check_protocol_port(self, port):
    """
    Check if the given port is within the defined protocol port ranges.
    
    Parameters
    ----------
    port
        The port number to check against the defined ranges.
    
    Returns
    -------
    :
        Returns True if ranges are not set or if the port is in the ranges.
    
    """
    
    if not self.ranges_are_set:
        return True
    return port in self.ranges