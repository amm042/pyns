# """Simple network simulator implementation example
#
# tested on python3.5
# """
#
# from collections import deque
# import logging
# import traceback
#
# from .simulator import Simulator
# from .node import Node
# from .netdev import Lora as Dev
# from .channel import PathLossChannel as Channel
# from .application import Application
# import random
#
# def goodbye(sim):
#     logging.warn("goodbye")
#
# def testCB(sim, *args, **kwargs):
#     #log = SimLogging(sim, logging.getLogger('testCB'))
#     logging.info("testCB ({}, {})".format(args, kwargs))
#     sim.scheduleIn(1, goodbye)
#     #pass
#
# class TestApp(Application):
#     def __init__(self, sim, node, device, **kwargs):
#         Application.__init__(self, "TestApp1", sim, node, device, **kwargs)
#         self.log = logging.getLogger("TestApp")
#
#     def run(self):
#         self.sim.scheduleIn(random.random()*5, self.sayhi)
#
#     def sayhi(self):
#         self.log.info("Node {} saying hi.".format(self.node.nodeid))
#         self.device.transmit('hello')
#     def receive(self, remotedev, packet):
#         self.log.info("{} -> {}: {}".format(
#             remotedev.address,
#             self.device.address,
#             packet))
#
# if __name__=="__main__":
#     sim =  Simulator()
#
#     logging.basicConfig(
#         level = logging.DEBUG,
#         format = '%(simtime)-15s - %(name)-15s - %(levelname)-10s - %(message)-80s')
#     old_factory = logging.getLogRecordFactory()
#     def sim_log_factory(*args, **kwargs):
#         record = old_factory(*args, **kwargs)
#         record.simtime = "{:15.4f}".format(sim.now)
#         return record
#     logging.setLogRecordFactory(sim_log_factory)
#
#     chan = Channel(sim, lossThreshold = 140)
#     nodes = [Node() for i in range(5)]
#     for i, node in enumerate(nodes):
#         d = Dev(chan, node, i)
#         chan.addDevice(d)
#         node.addDevice('lora0', d)
#         node.addApplication(TestApp(sim, node, d))
#
#     for n1 in nodes:
#         for n2 in nodes:
#             if n1 != n2:
#                 chan.setLossDb(n1, n2, random.randint(40, 160))
#
#     sim.run()
