def _get_worker(self, wtype):
    """
    Retrieves a worker and its associated queues based on the worker type.
    
    Parameters
    ----------
    wtype
        The type of worker to retrieve from the workers dictionary.
    
    Returns
    -------
    :
        A tuple containing the worker, its queue, and the result queue.
    
    """
    
    workers = self.workers[wtype]
    count, max_count = self.wcounts[wtype]
    worker, queue, res_queue = workers[count]
    if count == max_count - 1:
        count = 0
    else:
        count += 1
    self.wcounts[wtype] = [count, max_count]
    return worker, queue, res_queue