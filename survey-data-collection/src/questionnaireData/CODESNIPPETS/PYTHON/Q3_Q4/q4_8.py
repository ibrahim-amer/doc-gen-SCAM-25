def _handle_epoll_errors(self, fd, event):
    """
    Handles errors related to epoll events for a given file descriptor.
    
    Parameters
    ----------
    fd
        File descriptor associated with the event.
    event
        The event type that triggered the error handling.
    
    Raises
    ------
    Exception
        General exception when retrieving client address or during error handling.
    FileNotFoundError
        Raised if the file descriptor is already unregistered.
    
    """
    
    if fd in self.fds:
        client_sock = self.fds[fd][0]
    else:
        client_sock = None

    try:
        client_addr = client_sock.getpeername() if client_sock else "Unknown"
    except Exception:
        client_addr = "Unknown"

    if client_sock:
        self.logger.warning("{} for {} ({})".format(event, fd, client_addr), extra={'err_code': 1005})
    else:
        if event != "EPOLLRDHUP":
            self.logger.warning("{} for {}".format(event, fd), extra={'err_code': 1005})

    try:
        try:
            self.ep.unregister(fd)
        except FileNotFoundError:
            self.logger.warning('{}: fd {} already unregistered & closed'.format(event, fd),
                                extra={'err_code': 1005})
        if client_sock:
            self.logger.warning('Removing client {} ({})'.format(fd, client_addr),
                                extra={'err_code': 1005})
            client_sock.close()
            del self.fds[fd]
    except Exception:
        self.logger.debug('{} handling'.format(event), extra={'err_code': 1005}, exc_info=True)
        pass