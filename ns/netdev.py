class Device():
    def __init__(self, channel, node, address):
        self.channel = channel
        self.node = node
        self.address = address
    def transmit(self, packet):
        self.channel.transmit(self, packet)
    def receive(self, srcdev, packet):
        self.node.receive(self, srcdev, packet)

class LoraDev(Device):

    pass
