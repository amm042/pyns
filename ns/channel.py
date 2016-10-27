import random
class Channel():
    def __init__(self, sim, delay = 0.1, jitter = 0.01):
        self.sim = sim
        self.devices = []
        self.delay = delay
        self.jitter = jitter

    def addDevice(self, device):
        self.devices.append(device)

    def transmit(self, source, packet):
        "default implementation delivers the packet to all devices on the channel"
        for d in self.devices:
            if d != source:
                self.sim.scheduleIn(
                    self.delay + random.random()*self.jitter,
                    d.receive, source, packet)

class PathLossChannel(Channel):
    def __init__(self, sim, lossThreshold = 100, **kwargs):
        Channel.__init__(self, sim, **kwargs)
        self.lossThreshold = lossThreshold
    #todo override transmit function
    def setLossDb(self, src, dest, loss):
        pass
