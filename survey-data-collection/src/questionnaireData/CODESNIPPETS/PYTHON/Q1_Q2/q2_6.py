def _start(self):
    """
    Starts a new thread to run the _recv method for handling incoming data.
    """
    
    self.thread = threading.Thread(target=self._recv)
    self.thread.deamon = True
    self.thread.start()