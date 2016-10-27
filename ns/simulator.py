
from collections import deque
import logging
import traceback

class Simulator():
    def __init__(self):
        self.now = 0
        self.worklist = deque()
        self.log = logging.getLogger('Simulator')
        #self.log = logging.LoggerAdapter(
            #logging.getLogger('Simulator'),
            #extra = self.lognow())

    def lognow(self):
        return {'simtime': self.now}

    def scheduleIn(self, time, callback, *args, **kwargs):
        "schedule at a time relative to now"
        return self.scheduleAt(
            self.now + time,
            callback,
            *args,
            **kwargs)
    def scheduleAt(self, time, callback=None, *args, **kwargs):
        "insert the callback at the correct time in the worklist"

        assert (time >= self.now), "cannot schedule events in the past!"
        assert (callback != None), "must specify a callback!"

        i = 0
        atend = True
        for i in range(len(self.worklist)):
            if self.worklist[i]['time'] > time:
                atend = False
                break

        # self.log.debug("insert event at {} in index {}, worklist = {}".format(
        #     time,
        #     i,
        #     [x['time'] for x in self.worklist]
        # ))
        #
        job = { 'time': time,
                'cb': callback,
                'args': args,
                'kwargs': kwargs}

        # use append if possible, should be faster than insert
        if atend:
            self.worklist.append(job)
        elif i == 0:
            self.worklist.appendleft(job)
        else:
            self.worklist.insert(i, job)

        # self.log.debug("                              , worklist = {}".format(
        #     [x['time'] for x in self.worklist]
        # ))
    def run(self):
        "run the simulator until there are no more events"
        while True:

            # self.log.debug("Tick, worklist = {}".format(
            #             [x['time'] for x in self.worklist]))
            try:
                e = self.worklist.popleft()
            except IndexError:
                self.log.info("Simulation over, no more events t={}.".format(self.now))
                break

            self.now = e['time']
            try:
                if len(e['args']) > 0 and len(e['kwargs']) > 0:
                    e['cb'](*e['args'], **e['kwargs'])
                elif len(e['args']) > 0:
                    e['cb'](*e['args'])
                elif len(e['kwargs'])> 0:
                    e['cb'](**e['kwargs'])
                else:
                    e['cb']()
            except Exception as x:
                traceback.print_exc()
