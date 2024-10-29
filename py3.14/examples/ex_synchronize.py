#
# A test file for the `processing` package
#

import time, sys, random
from queue import Empty

import multiprocess as processing               # may get overwritten
processing.currentProcess = processing.current_process
processing.freezeSupport = processing.freeze_support
processing.activeChildren = processing.active_children


#### TEST_VALUE

def value_func(running, mutex):
    random.seed()
    time.sleep(random.random()*4)
    
    mutex.acquire()
    print('\n\t\t\t' + str(processing.currentProcess()) + ' has finished')
    running.value -= 1
    mutex.release()

def test_value():
    TASKS = 10
    running = processing.Value('i', TASKS)
    mutex = processing.Lock()

    for i in range(TASKS):
        processing.Process(target=value_func, args=(running, mutex)).start()

    while running.value > 0:
        time.sleep(0.08)
        mutex.acquire()
        print(running.value, end=' ')
        sys.stdout.flush()
        mutex.release()

    print()
    print('No more running processes')


#### TEST_QUEUE

def queue_func(queue):
    for i in range(30):
        time.sleep(0.5 * random.random())
        queue.put(i*i)
    queue.put('STOP')

def test_queue():
    q = processing.Queue()

    p = processing.Process(target=queue_func, args=(q,))
    p.start()

    o = None
    while o != 'STOP':
        try:
            o = q.get(timeout=0.3)
            print(o, end=' ')
            sys.stdout.flush()
        except Empty:
            print('TIMEOUT')

    print()


#### TEST_CONDITION

def condition_func(cond):
    cond.acquire()
    print('\t' + str(cond))
    time.sleep(2)
    print('\tchild is notifying')
    print('\t' + str(cond))
    cond.notify()
    cond.release()

def test_condition():
    cond = processing.Condition()

    p = processing.Process(target=condition_func, args=(cond,))
    print(cond)

    cond.acquire()
    print(cond)
    cond.acquire()
    print(cond)

    p.start()

    print('main is waiting')
    cond.wait()
    print('main has woken up')

    print(cond)
    cond.release()
    print(cond)
    cond.release()

    p.join()
    print(cond)


#### TEST_SEMAPHORE

def semaphore_func(sema, mutex, running):
    sema.acquire()

    mutex.acquire()
    running.value += 1
    print(running.value, 'tasks are running')
    mutex.release()

    random.seed()
    time.sleep(random.random()*2)

    mutex.acquire()
    running.value -= 1
    print('%s has finished' % processing.currentProcess())
    mutex.release()

    sema.release()

def test_semaphore():
    sema = processing.Semaphore(3)
    mutex = processing.RLock()
    running = processing.Value('i', 0)

    processes = [
        processing.Process(target=semaphore_func, args=(sema, mutex, running))
        for i in range(10)
        ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


#### TEST_JOIN_TIMEOUT

def join_timeout_func():
    print('\tchild sleeping')
    time.sleep(5.5)
    print('\n\tchild terminating')

def test_join_timeout():
    p = processing.Process(target=join_timeout_func)
    p.start()

    print('waiting for process to finish')

    while 1:
        p.join(timeout=1)
        if not p.is_alive():
            break
        print('.', end=' ')
        sys.stdout.flush()


#### TEST_EVENT

def event_func(event):
    print('\t%r is waiting' % processing.currentProcess())
    event.wait()
    print('\t%r has woken up' % processing.currentProcess())

def test_event():
    event = processing.Event()

    processes = [processing.Process(target=event_func, args=(event,))
                 for i in range(5)]

    for p in processes:
        p.start()

    print('main is sleeping')
    time.sleep(2)

    print('main is setting event')
    event.set()

    for p in processes:
        p.join()


#### TEST_SHAREDVALUES

def sharedvalues_func(values, arrays, shared_values, shared_arrays):    
    for i in range(len(values)):
        v = values[i][1]
        sv = shared_values[i].value
        assert v == sv

    for i in range(len(values)):
        a = arrays[i][1]
        sa = list(shared_arrays[i][:])
        assert list(a) == sa

    print('Tests passed')

def test_sharedvalues():
    values = [
        ('i', 10),
        ('h', -2),
        ('d', 1.25)
        ]
    arrays = [
        ('i', range(100)),
        ('d', [0.25 * i for i in range(100)]),
        ('H', range(1000))
        ]

    shared_values = [processing.Value(id, v) for id, v in values]
    shared_arrays = [processing.Array(id, a) for id, a in arrays]

    p = processing.Process(
        target=sharedvalues_func,
        args=(values, arrays, shared_values, shared_arrays)
        )
    p.start()
    p.join()
    
    assert p.exitcode == 0


####

def test(namespace=processing):
    global processing
    
    processing = namespace
    
    for func in [ test_value, test_queue, test_condition,
                  test_semaphore, test_join_timeout, test_event,
                  test_sharedvalues ]:

        print('\n\t######## %s\n' % func.__name__)
        func()

    ignore = processing.activeChildren()        # cleanup any old processes
    if hasattr(processing, '_debugInfo'):
        info = processing._debugInfo()
        if info:
            print(info)
            raise ValueError('there should be no positive refcounts left')


if __name__ == '__main__':
    processing.freezeSupport()
    
    assert len(sys.argv) in (1, 2)
    
    if len(sys.argv) == 1 or sys.argv[1] == 'processes':
        print(' Using processes '.center(79, '-'))
        namespace = processing
    elif sys.argv[1] == 'manager':
        print(' Using processes and a manager '.center(79, '-'))
        namespace = processing.Manager()
        namespace.Process = processing.Process
        namespace.currentProcess = processing.currentProcess
        namespace.activeChildren = processing.activeChildren
    elif sys.argv[1] == 'threads':
        print(' Using threads '.center(79, '-'))
        import processing.dummy as namespace
    else:
        print('Usage:\n\t%s [processes | manager | threads]' % sys.argv[0])
        raise SystemExit(2)

    test(namespace)
