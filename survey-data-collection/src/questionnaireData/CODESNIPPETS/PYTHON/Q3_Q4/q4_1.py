def send(self, email_address, subject, body, attachment_path=None, reconnect=True):
    """
    Sends an email with optional attachments, handling reconnection if necessary.
    
    Parameters
    ----------
    email_address
        Recipient email address for the message.
    subject
        Subject line of the email.
    body
        Main content of the email.
    attachment_path
        Path(s) to any file attachments (optional).
    reconnect
        Flag to attempt reconnection if the client is not connected.
    
    Returns
    -------
    :
        Tuple containing packet ID and the result of the send operation.
    
    Raises
    ------
    EmailClientException
        Raised when there is an issue with attachments or connection.
    
    """
    
    packet_id = self.incr_id

    attachments = []
    attachments_names = []

    if attachment_path is not None:
        # Turn old attachment_path to list to be compatible with the new versions
        if isinstance(attachment_path, str):  # pragma: no branch
            attachment_path = [attachment_path]

        for att in attachment_path:
            try:
                with open(att, 'rb') as f:
                    compressed = gzip.compress(f.read())
                    compressed_encoded = base64.b64encode(compressed).decode('utf-8')
                    attachments.append(compressed_encoded)
                attachments_names.append(os.path.basename(att))
            except Exception as e:
                raise EmailClientException("Attachment: {}".format(e))
    else:
        attachments = None
        attachments_names = None

    packet = {
        "id": packet_id,
        "type": PacketType.EMAIL.value,
        "email": email_address,
        "subject": subject,
        "payload": body,
        "attachment": attachments,
        "attachment_name": attachments_names
    }

    dumped = "{}\0".format(json.dumps(packet, cls=PacketTypeEncoder))
    encoded = dumped.encode("utf-8")
    if not self.client:
        if reconnect:  # pragma: no branch
            for seconds in range(1, 6):  # pragma: no branch
                try:
                    self.reconnect()
                    if self.client:  # pragma: no branch
                        break
                except EmailClientException:
                    if seconds == 5 and not self.client:
                        raise EmailClientException("Connection is closed.")
                    else:
                        time.sleep(seconds)
                        continue
        else:
            raise EmailClientException("Connection is closed.")

    self.incr_id += 1
    try:
        return (packet_id, self.client.send(encoded))
    except Exception:
        return (packet_id, -1)