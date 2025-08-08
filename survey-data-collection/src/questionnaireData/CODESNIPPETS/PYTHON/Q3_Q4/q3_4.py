def close(self):
    """
    Closes the client connection and releases the associated resources.
    
    Raises
    ------
    RuntimeError
        Raised if the thread cannot be joined within the timeout.
    """
    
    try:
        self.lock.acquire()
        if self.client:
            self.client.shutdown()
            self.client.close()
    finally:
        self.lock.release()

    self.client = None
    try:
        self.thread.join(timeout=5)
    except RuntimeError:
        pass