import functools


def coroutine(coro_func):
    @functools.wraps(coro_func)
    def initialized_coroutine(*args, **kwargs):
        coro = coro_func(*args, **kwargs)
        coro.send(None) # initializes the coroutine
        return coro
    return initialized_coroutine

@coroutine
def echo():
    """ Yields all sent values to the caller. """
    
    item = None
    while True:
        item = yield item

@coroutine
def accumulator(target):
    """ Yields a growing list of items to the target. """
    
    items = []
    while True:
        item = yield
        items.append(item)
        target.send(items)

@coroutine
def noop(target):
    """ Yields the value to the next target. """
    
    while True:
        item = yield
        target.send(item)

@coroutine
def broadcast(targets):
    """ Yields the value to collection of targets. """
    
    while True:
        item = yield
        for target in targets:
            target.send(item)

@coroutine
def comap(mapping_func, target):
    """ Yields the application of mapping_func to the item to its target. """
    
    while True:
        item = yield
        target.send(mapping_func(item))

@coroutine
def cofilter(condition_func, target):
    """ Yields the item if it meets condition_func to its target. """
    
    while True:
        item = yield
        if condition_func(item):
            target.send(item)

@coroutine
def dedupe(target):
    """ Yields unique hashable items to its target. """
    
    seen = set()
    while True:
        item = yield
        if item not in seen:
            seen.add(item)
            target.send(item)

@coroutine
def batch(condition_func, target):
    """ Collects items until condition is met, then yields payload. """
    
    while True:
        payload = []
        while True:
            item = yield
            payload.append(item)
            if condition_func(item):
                break
        target.send(payload)