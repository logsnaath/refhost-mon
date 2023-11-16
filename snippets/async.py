#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
##

import asyncio
import time

def background(f):
    def wrapped(*args, **kwargs):
        looper = asyncio.get_event_loop()
        return looper.run_in_executor(None, f, *args, **kwargs)

    return wrapped

@background
def your_function(argument):
    time.sleep(5)
    #asyncio.sleep(5)
    print('function finished for '+str(argument))


for i in range(10):
    your_function(i)


print('loop finished')
