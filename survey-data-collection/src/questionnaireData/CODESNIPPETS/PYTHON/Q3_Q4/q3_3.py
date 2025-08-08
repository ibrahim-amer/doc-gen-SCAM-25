
def _webhook_loop(self, queue, result_queue):
    """
    Continuously processes packets from a queue and sends results to a result queue.
    
    Parameters
    ----------
    queue
        A queue to receive packets for processing.
    result_queue
        A queue to send results back after processing.
    
    """
    
    if PRCTL_AVAILABLE:
        prctl.set_pdeathsig(signal.SIGKILL)
    while True:
        try:
            cp = mp.current_process()
            if cp.exiting:
                break

            packet, task_id, client_addr = queue.get(True, 2)
            res = self._webhook_fn(packet, client_addr)
            result_queue.put_nowait((task_id, res,))
        except Exception:
            pass