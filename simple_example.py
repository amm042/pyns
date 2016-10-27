from ns import *
import logging

class TestApp(Application):
    def __init__(self, sim, node, device, **kwargs):
        Application.__init__(self, "TestApp1", sim, node, device, **kwargs)
        self.log = logging.getLogger("TestApp@{}".format(node.nodeid))

    def run(self):
        self.sim.scheduleIn(random.random()*5, self.sayhi)

    def sayhi(self):
        self.log.info("Node {} saying hi.".format(self.node.nodeid))
        self.node.transmit('hello')

    def receive(self, remotedev, packet):
        self.log.info("{} from Node {}".format(
            packet,
            remotedev.address))

sim =  Simulator()

# fix logging to use simulated time not actual time.
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(simtime)-15s - %(name)-15s - %(levelname)-10s - %(message)-80s')
old_factory = logging.getLogRecordFactory()
def sim_log_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.simtime = "{:15.4f}".format(sim.now)
    return record
logging.setLogRecordFactory(sim_log_factory)
# end logging fix

# create a channel
chan = PathLossChannel(sim, lossThreshold = 140)

# and some nodes
nodes = [Node() for i in range(5)]
for i, node in enumerate(nodes):
    # each node gets a LoraDevice and our TestApp
    d = LoraDev(chan, node, i)
    chan.addDevice(d)
    node.addDevice('lora0', d)
    node.addApplication(TestApp(sim, node, d))

# load dummy path loss values
for n1 in nodes:
    for n2 in nodes:
        if n1 != n2:
            chan.setLossDb(n1, n2, random.randint(40, 160))

# run the simulation
sim.run()
