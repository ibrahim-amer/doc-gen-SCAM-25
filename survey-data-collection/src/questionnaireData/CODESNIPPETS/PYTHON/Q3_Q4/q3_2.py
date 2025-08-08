def _email_loop(self, queue, result_queue):
    """
    Continuously processes email tasks from a queue and stores results in a result queue.
    
    Parameters
    ----------
    queue
        The queue to receive email tasks and packets.
    result_queue
        The queue to store results of processed email tasks.
    
    Raises
    ------
    Exception
        Catches all exceptions during processing, but does not handle them.
    
    """
    
    if PRCTL_AVAILABLE:
        prctl.set_pdeathsig(signal.SIGKILL)
    while True:
        try:
            cp = mp.current_process()
            if cp.exiting:
                break

            packet, task_id, client_addr = queue.get(True, 2)
            res = self._email_fn(packet, client_addr)
            result_queue.put_nowait((task_id, res,))
        except Exception:
            pass