# -------------------------------------------------------------------------------
# Name:        threading_pool
# Purpose:
#
# Author:      JCanalsMascorda
#
# Created:     30/08/2022
# Copyright:   (c) JCanalsMascorda 2021
# Licence:
# -------------------------------------------------------------------------------
import random, time
from multiprocessing.pool import ThreadPool
from threading import current_thread, Lock, Semaphore, Thread

MAX_NUM_OF_THREADS_ALLOWED_TO_EXIST = 50
MAX_NUM_OF_THREADS_ALLOWED_RUNNING_AT_SAME_TIME = 13


class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = Lock()

    def activate(self, thread_id):
        with self.lock:
            self.active.append(thread_id)
            print(f"Active Thread list:\t{self.active}")

    def deactivate(self, thread_id):
        with self.lock:
            self.active.remove(thread_id)


def function_to_execute(semaphore, pool):
    print(f"Thread {current_thread().name} waiting to join the pool...")
    with semaphore:
        pool.activate(current_thread().name)
        time.sleep(random.randint(0, 5))
        pool.deactivate(current_thread().name)


def main():
    pool = ThreadPool()
    s = Semaphore(MAX_NUM_OF_THREADS_ALLOWED_RUNNING_AT_SAME_TIME)
    list_of_threads = list()

    try:
        for i in range(MAX_NUM_OF_THREADS_ALLOWED_TO_EXIST):
            t = Thread(target=function_to_execute, name=f"{i}", args=(s, pool))
            list_of_threads.append(t)
            t.daemon = True
            t.start()
    finally:
        for thread in list_of_threads:
            thread.join()


if __name__ == "__main__":
    main()
