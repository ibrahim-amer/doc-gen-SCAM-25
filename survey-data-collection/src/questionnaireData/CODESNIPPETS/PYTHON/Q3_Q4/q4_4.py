def send(self, address, port, data, soc_type=PacketType.TCP, reconnect=True):
    """
    Sends a packet to the specified address and port using the specified socket type.
    
    Parameters
    ----------
    address
        The address to send the packet to.
    port
        The port number to send the packet to.
    data
        The data payload to be sent.
    soc_type
        The type of socket (TCP or UDP). Defaults to TCP.
    reconnect
        Flag to indicate if reconnection should be attempted.
    
    Returns
    -------
    :
        A tuple containing the packet ID and the result of the send operation.
    
    Raises
    ------
    ProtocolClientException
        Raised for invalid socket type or closed connection.
    Exception
        General exception during sending the packet.
    
    """
    
    if soc_type not in (PacketType.TCP, PacketType.UDP):
        raise ProtocolClientException(
            "Invalid socket type: '{}'".format(soc_type))

    if not self._check_protocol_port(port):
        raise ProtocolClientException("Port {} outside range".format(port))

    packet_id = self.incr_id
    packet = {
        "id": packet_id,
        "type": soc_type.value,
        "addr": address,
        "port": port,
        "payload": data
    }
    dumped = "{}\0".format(json.dumps(packet, cls=PacketTypeEncoder))
    encoded = dumped.encode("utf-8")
    if not self.client:
        if reconnect:
            for seconds in range(1, 6):  # pragma: no branch
                try:
                    self.reconnect()
                    if self.client:  # pragma: no branch
                        break
                except ProtocolClientException:
                    if seconds == 5 and not self.client:
                        raise ProtocolClientException("Connection is closed.")
                    else:
                        time.sleep(seconds)
                        continue
        else:
            raise ProtocolClientException("Connection is closed.")

    self.incr_id += 1
    try:
        return (packet_id, self.client.send(encoded))
    except Exception:
        return (packet_id, -1)