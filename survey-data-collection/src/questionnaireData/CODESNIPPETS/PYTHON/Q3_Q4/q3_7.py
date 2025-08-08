def _protocol_loop(self, queue, result_queue, clients):
    """
    Continuously processes packets from a queue and sends results to a result queue.
    
    Parameters
    ----------
    queue
        Queue to receive packets for processing.
    result_queue
        Queue to send processing results.
    clients
        List of connected clients.
    
    """
    
    if PRCTL_AVAILABLE:
        prctl.set_pdeathsig(signal.SIGKILL)
    while True:
        try:
            cp = mp.current_process()
            if cp.exiting:
                break

            packet, task_id, client_addr = queue.get(True, 2)
            res = self._protocol_fn(packet, clients, client_addr)
            result_queue.put_nowait((task_id, res,))
        except Exception:
            pass