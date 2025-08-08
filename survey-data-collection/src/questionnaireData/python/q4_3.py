def _recv(self):
    """
    Receives messages from a client socket and processes them into a response dictionary.
    
    Raises
    ------
    Exception
        General exception when registering the socket.
    OSError
        Error during socket operations, e.g., interrupted system call.
    AttributeError
        Attribute error when accessing client methods or properties.
    
    """
    
    msg = []
    selector = selectors.DefaultSelector()
    try:
        selector.register(self.client.sock, selectors.EVENT_READ)
    except Exception:
        self.client = None
        return
    while self.client and self.client._fd() != -1:  # pragma: no branch
        try:
            ready = selector.select(timeout=0.05)
        except OSError as e:
            # For python < 3.5
            if e.errno == errno.EINTR:
                continue
            break
        # self.client might have become None from a close() call after the check but before the try
        except AttributeError:
            break

        if ready:
            try:
                response = self.client.recv(64).decode('utf-8')
            except AttributeError:
                break
        else:
            try:
                if self.client._fd() == -1:
                    break
                continue
            except Exception:
                break
        if not response:
            self.close()
            break
        try:
            msg.append(response)
            ready = "".join(msg).split("\r\n")
            for r in ready[:-1]:
                packet_id, res = r.split("|")
                packet_id, res = int(packet_id), int(res, base=16)
                if packet_id == -1:
                    if self.incr_id - 1 not in self.responses:  # pragma: no branch
                        self.responses[self.incr_id - 1] = self.statuses[2]
                        continue
                self.responses[packet_id] = self.statuses[res]
            msg = [ready[-1]]
        except Exception:
            pass