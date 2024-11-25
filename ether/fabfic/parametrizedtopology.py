import matplotlib.pyplot as plt
from srds import ParameterizedDistribution as PDist
import random

from ether.qos import latency
import ether.blocks.nodes as nodes
from ether.blocks.cells import *
from ether.cell import *
from ether.core import Node
from ether.topology import Topology
from ether.fabfic.vis import draw_basic

#Connection type between the Cloud and the first-layer clusters
CLOUD_CLUSTER_CONNECTION: UpDownLink = FiberToExchange()
#Number of edge clusters connected to the Cloud
GEOCELL_SIZE: int = 6
#Number of nodes per cluster
NUM_NODES_PER_CLUSTER: int = 3
#Type of node
DEFAULT_NODE_TYPE: Node = nodes.rpi3
#Max range of nodes
NODE_RANGE: int = 12
#Max range of clusters
CLUSTER_RANGE: int  = 10
#Specify if the number of nodes varies from cluster to cluster
RAND_NUM_NODES: bool = True

def main():
    topology = Topology()
    
    ########################################

    #Custom connection and latency

    #Use pre-existent latency distribution
    #latency_distribution = latency.mobile_isp

    #Use custom latency distribuion
    latency_distribution = PDist.lognorm((0.40, 1.40, 0.60))

    #Download bandwidth
    bw_dw = 385
    #Upload bandwidth
    bw_up = 125
    #Backhaul name, it must start with 'internet'
    backhaul = 'internet_custom'

    CLOUD_CLUSTER_CONNECTION: UpDownLink = CustomConnection(bw_dw, bw_up, latency_distribution, backhaul)
    
    ########################################

    #Node with custom resources

    cpus = 4
    arch = 'x86'
    mem = '8G'
    labels = {
        'ether.edgerun.io/type': 'sbc',
        'ether.edgerun.io/model': 'rpi4',
        'locality.skippy.io/type': 'edge'
    }

    neighborhood = lambda size: Cluster(
        nodes= [nodes.create_custom_node(cpus,mem,arch,labels) for _ in range(size)],
        backhaul=CLOUD_CLUSTER_CONNECTION
    )

    ########################################
    
    # #Fixed type of node
    # neighborhood = lambda size: Cluster(
    #     nodes= [DEFAULT_NODE_TYPE] * size,
    #     backhaul=CLOUD_CLUSTER_CONNECTION
    # )

    ########################################

    #Custom node list

    neighborhood = lambda size: Cluster(
        nodes=[nodes.rpi3, nodes.nuc, nodes.tx2] * size,
        backhaul=CLOUD_CLUSTER_CONNECTION
    )

    ########################################

    # #Fixed number of node and clusters
    # city = GeoCell(
    #     GEOCELL_SIZE, 
    #     nodes=[neighborhood], 
    #     density = NUM_NODES_PER_CLUSTER
    #     )
    
    ########################################
    
    # #Variable range of nodes and clusters

    # city = GeoCell(
    # size = random.randint(1, CLUSTER_RANGE),
    # nodes = [neighborhood],
    # density = random.randint(1, NODE_RANGE),
    # rand_nodes = RAND_NUM_NODES
    # )

    ########################################

    #Variable range of nodes and FIXED number of clusters

    city = GeoCell(
    size = GEOCELL_SIZE,
    nodes = [neighborhood],
    density = random.randint(1, NODE_RANGE),
    rand_nodes = RAND_NUM_NODES
    )

    ########################################

    #Comment this out if you're using unique clusters down below
    topology.add(city)

    ########################################

    # #Setup unique clusters -> Each cluster has a unique type and number of nodes

    # #Cluster with fixed type of nodes
    # neighborhood = lambda size: Cluster(
    #     nodes= [DEFAULT_NODE_TYPE] * size,
    #     backhaul=CLOUD_CLUSTER_CONNECTION
    # )
    # city = GeoCell(
    #     size = 1,
    #     nodes = [neighborhood],
    #     density = random.randint(1, NODE_RANGE),
    #     rand_nodes = RAND_NUM_NODES
    # )
    # topology.add(city)

    # #Cluster with custom type of nodes (scaled by size)
    # neighborhood = lambda size: Cluster(
    #     nodes=[nodes.rpi3, nodes.rpi4, nodes.tx2] * size,
    #     backhaul=CLOUD_CLUSTER_CONNECTION
    # )
    # city = GeoCell(
    #     1, 
    #     nodes=[neighborhood], 
    #     density = NUM_NODES_PER_CLUSTER
    #     )
    # topology.add(city)

    # #Cluster with custom type and quantity of nodes
    # neighborhood = lambda size: Cluster(
    #     nodes=[[nodes.nuc]*3, [nodes.rpi4]*2, nodes.tx2],
    #     backhaul=CLOUD_CLUSTER_CONNECTION
    # )
    # city = GeoCell(
    #     1, 
    #     nodes=[neighborhood], 
    #     density = NUM_NODES_PER_CLUSTER
    #     )
    # topology.add(city)

    ########################################

   # topology.add(Cloud(backhaul=FiberToExchange()))

    ########################################

    draw_basic(topology)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.show()  # display

    print('num nodes:', len(topology.nodes))


if __name__ == '__main__':
    main()
