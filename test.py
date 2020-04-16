from time import time
from time import sleep
from threading import Thread


def my_sleep(init_t, t):
    sleep(t)
    print(time() - init_t)


init_time = time()
t1 = Thread(target=my_sleep, args=(init_time, 3))
t2 = Thread(target=my_sleep, args=(init_time, 5))
t1.start()
t2.start()