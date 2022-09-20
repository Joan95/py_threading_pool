# -------------------------------------------------------------------------------
# Name:        MyThreadPool
# Purpose:
#
# Author:      JCanalsMascorda
#
# Created:     30/08/2022
# Copyright:   (c) JCanalsMascorda 2022
# Licence:
# -------------------------------------------------------------------------------

from threading import Lock


class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = Lock()

    def activate(self, thread_id):
        with self.lock:
            if thread_id not in self.active:
                self.active.append(thread_id)
                print(f"\tActive connection list: {self.active}")

    def deactivate(self, thread_id):
        with self.lock:
            if thread_id in self.active:
                self.active.remove(thread_id)
                if self.active:
                    print(f"\tActive connection list: {self.active}")
                else:
                    print(f"\tNo current connections available at this moment! :(")
