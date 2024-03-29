
""" task scheduler """
# ensure that every task has a chance to run through till completion; the when
# and where of a task's execution, however, is non-deterministic;
import threading
import time
import random

counter = 1

def workerA():
    global counter
    while counter < 1000:
        counter += 1
        print("Worker A is incrementing counter to {}".format(counter))
        sleepTime = random.randint(0, 1)
        time.sleep(sleepTime)

def workerB():
    global counter
    while counter > -1000:
        counter -= 1
        print("Worker B is decrementing counter to {}".format(counter))
        sleepTime = random.randint(0, 1)
        time.sleep(sleepTime)

def main():
    t0 = time.time()
    # can't stop program!!!
    thread1 = threading.Thread(target=workerA)
    thread2 = threading.Thread(target=workerB)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    t1 = time.time()
    print("Execution Time {}".format(t1-t0))


if __name__ == "__main__":
    main()

























# code shows one of the dangers of multiple threads
# accessing shared resources without any form of synchronization;
# There is no accurate way to determine what will happen to our counter,
# and as such, our program could be considered unreliable;
