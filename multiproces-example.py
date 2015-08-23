import time
from multiprocessing import Process, Queue

def f(q, somenumber):
    q.put([somenumber,"hello"])
    time.sleep(22)


if __name__ == '__main__':
    q = Queue()	# used for communication. See https://docs.python.org/2/library/multiprocessing.html#exchanging-objects-between-processes

    p1 = Process(target=f, args=(q,1))
    p1.start()
    p2 = Process(target=f, args=(q,2))
    p2.start()

    print "All started"

    print q.get()    # prints "[42, None, 'hello']"
    print q.get()    # prints "[42, None, 'hello']"
    # p.join()
    p1.terminate()
    p2.terminate()
