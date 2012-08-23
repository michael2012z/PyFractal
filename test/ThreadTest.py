import time
import threading

def counter ():
    for i in range(0, 32000):
        print i
    return

def sleeper ():
    for i in range(0, 10):
        time.sleep(0.1)
        print "wake up for ", i
    return


counter_thread = threading.Thread(target=counter)
sleeper_thread = threading.Thread(target=sleeper)
counter_thread.start()
sleeper_thread.start()
