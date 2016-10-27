import logging
import traceback

_id = 0

class Node:
    def __init__(self):
        global _id
        self.log = logging.getLogger('Node')
        self.nodeid = _id
        self.devices = {}
        self.revdev = {}
        self.applications = []
        self.defaultdev = None
        _id += 1
    def addDevice(self, name, dev):
        assert (name not in self.devices), "that device already exists."
        if self.defaultdev == None:
            self.defaultdev = dev
        self.devices[name] = dev
        self.revdev[dev] = name
    def transmit(self, packet, device=None):
        if device == None:
            device = self.defaultdev

        self.log.debug("TRANSMIT@ Node {}.{}.".format(
            self.nodeid,
            self.revdev[device]
        ))

        device.transmit(packet)

    def receive(self, localdev, remotedev, packet):

        # self.log.info('Node {} -> {}: received: {}'.format(
        #     remotedev.node.nodeid,
        #     localdev.node.nodeid,
        #     packet
        # ))
        self.log.debug("RECEIVE @ Node {}.{} from Node {}.{}.".format(
            self.nodeid,
            self.revdev[localdev],
            remotedev.node.nodeid,
            remotedev.node.revdev[remotedev]
        ))
        for a in self.applications:
            try:
                a.receive(remotedev, packet)
            except Exception as x:
                self.log.error(x)

    def addApplication(self, app):
        self.applications.append(app)
