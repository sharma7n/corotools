from unittest import TestCase, main

import corotools


@corotools.coroutine
def test_sequence(results):
    for result in results:
        item = yield
        assert item == result
    while True:
        yield
        assert False

class CorotoolsTestCase(TestCase):
    def test_coroutine(self):
        @corotools.coroutine
        def func(*args, **kwargs):
            while True:
                _ = yield
        
        coro = func()
        next(coro)
        coro.send(0)
        
        try:
            coro.throw(ValueError())
        except ValueError:
            pass
        
        coro.close()
        
        try:
            coro.send(0)
        except StopIteration:
            pass
    
    def test_echo(self):
        ec = corotools.echo()
        
        assert ec.send(1) == 1
        assert ec.send("1") == "1"
        assert ec.send([]) == []
        assert ec.send({}) == {}
        assert ec.send(None) is None
        
        obj = object()
        assert ec.send(obj) == obj
        assert ec.send(obj) is obj
    
    def test_accumulator(self):
        this_test = test_sequence([
            [1], 
            [1, 2],
            [1, 2, 3]])

        col = corotools.accumulator(this_test)
        col.send(1)
        col.send(2)
        col.send(3)
    
    def test_noop(self):
        noop = corotools.noop

        acc = corotools.accumulator(noop(noop(test_sequence([
            [1],
            [1, 2],
            [1, 2, 3]]))))
        
        acc.send(1)
        acc.send(2)
        acc.send(3)
    
    def test_broadcast(self):
        noop = corotools.noop
        acc = corotools.accumulator(test_sequence([
            [1],
            [1, 1],
            [1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2, 2]]))
        
        bc = corotools.broadcast([noop(acc), noop(acc), noop(acc)])
        bc.send(1)
        bc.send(2)
    
    def test_comap(self):
        com = corotools.comap(sum, test_sequence([6, 40]))
        com.send([1, 2, 3])
        com.send((x for x in range(20) if x % 4 == 0))
    
    def test_cofilter(self):
        fil = corotools.cofilter(bool, test_sequence([1]))
        fil.send(0)
        fil.send(1)
        fil.send(0)
    
    def test_dedupe(self):
        ded = corotools.dedupe(test_sequence([1, 2, 3]))
        ded.send(1)
        ded.send(1)
        ded.send(2)
        ded.send(1)
        ded.send(3)
        ded.send(2)
        ded.send(3)
    
    def test_batch(self):
        bat = corotools.batch(lambda i: i == 3, test_sequence([[1, 2, 3]]))
        bat.send(1)
        bat.send(2)
        bat.send(3)
        bat.send(1)
        bat.send(2)

if __name__ == '__main__':
    main()