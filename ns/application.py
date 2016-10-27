class Application():
    def __init__(self, name, sim, node, device, startAt = 0):
        self.sim = sim
        self.name = name
        self.node = node
        self.device = device
        self.sim.scheduleAt(startAt, self.run)

    def run(self):
        raise NotImplementedError("override in derived class.")

    def receive(self, srcdev, packet):
        raise NotImplementedError("override in derived class.")
