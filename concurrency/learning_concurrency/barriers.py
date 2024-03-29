
# utilize barriers in order to block the execution of our threads
# until all of the threads have reached a desired point of execution
import threading
import time
import random

class myThread(threading.Thread):
    def __init__(self, barrier):
        threading.Thread.__init__(self)
        self.barrier = barrier

    def run(self):
        print("Thread {} working on something".format(threading.current_thread()))
        time.sleep(random.randint(1, 10))
        print("Thread {} is joining {} waiting on Barrier".format(
            threading.current_thread(),
            self.barrier.n_waiting
        ))


barrier = threading.Barrier(4)
threads = []

for i in range(4):
    thread = myThread(barrier)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()
