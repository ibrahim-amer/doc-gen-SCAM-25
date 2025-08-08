def set_ports(self, ports):
    """
    Sets the ports for the instance by parsing the provided ports.
    
    Parameters
    ----------
    ports
        The ports to be set for the instance.
    
    """
    
    self.ranges = self._parse_ports(ports)
    self.ranges_are_set = True
    