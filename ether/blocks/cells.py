import itertools
from collections import defaultdict

from ether.blocks.nodes import create_server_node, create_cloud_server_node
from ether.cell import LANCell, UpDownLink
from ether.qos import latency

counters = defaultdict(lambda: itertools.count(0, 1))


class MobileConnection(UpDownLink):

    def __init__(self, backhaul='internet') -> None:
        super().__init__(125, 25, backhaul, latency.mobile_isp)


class BusinessIsp(UpDownLink):

    def __init__(self, backhaul='internet') -> None:
        super().__init__(500, 50, backhaul, latency.business_isp)


class FiberToExchange(UpDownLink):

    def __init__(self, backhaul='internet') -> None:
        super().__init__(1000, 1000, backhaul, latency.lan)

class CustomConnection(UpDownLink):
    
    def __init__(self, bw_down, bw_up, latency_dist,backhaul='internet'):
        super().__init__(bw_down, bw_up, backhaul, latency_dist)


class IoTComputeBox(LANCell):
    pass


class Cloudlet(LANCell):
    def __init__(self, server_per_rack=5, racks=1, backhaul=None) -> None:
        self.racks = racks
        self.server_per_rack = server_per_rack

        nodes = [self._create_rack] * racks

        super().__init__(nodes, backhaul=backhaul)

    def _create_identity(self):
        self.nr = next(counters['cloudlet'])
        self.name = 'cloudlet_%d' % self.nr
        self.switch = 'switch_%s' % self.name

    def _create_rack(self):
        return LANCell([create_server_node] * self.server_per_rack, backhaul=self.switch)

class Cloud(LANCell):
    def __init__(self, server_per_rack=5, racks=1, backhaul=None) -> None:
        self.racks = racks
        self.server_per_rack = server_per_rack

        nodes = [self._create_rack] * racks

        super().__init__(nodes, backhaul=backhaul)

    def _create_identity(self):
        self.name = 'cloud'
        self.switch = 'switch_%s' % self.name

    def _create_rack(self):
        return LANCell([create_cloud_server_node] * self.server_per_rack, backhaul=self.switch)