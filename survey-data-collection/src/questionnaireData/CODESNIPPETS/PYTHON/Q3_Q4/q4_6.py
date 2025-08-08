def _parse_ports(self, port_str):
    """
    Parses a string of ports and port ranges into a set of individual ports.
    
    Parameters
    ----------
    port_str
        A string containing ports or port ranges to be parsed.
    
    Returns
    -------
    :
        A set of parsed port numbers.
    
    Raises
    ------
    WebhookClientException
        Raised for invalid port ranges or parsing errors.
    
    """
    
    if not port_str:
        return set()

    tokens = port_str.split(',')
    ports = []

    for token in tokens:
        if "-" in token:
            try:
                begin, end = list(map(int, token.split("-", 1)))
                if begin > end:
                    raise WebhookClientException("Invalid port range, begin > end ({} > {})".format(begin, end))
                ports.extend(list(range(begin, end+1)))
            except Exception as e:
                raise WebhookClientException("Error while parsing port ({})".format(e))
        else:
            try:
                ports.append(int(token))
            except Exception as e:
                raise WebhookClientException("Error while parsing port ({})".format(e))
    return set(ports)