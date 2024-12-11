from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_tree_topo():
    # Initialize Mininet with a remote controller
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Add a remote controller
    controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Tree topology parameters
    depth = 3  # Depth of the tree
    fanout = 2  # Number of children per switch

    switches = []
    hosts = []
    parent_map = {}  # Map to keep track of parent-child relationships

    # Recursive function to build the tree
    def build_tree(level, parent_switch=None):
        if level > depth:
            return None

        # Create a switch
        switch_id = len(switches) + 1
        switch = net.addSwitch(f's{switch_id}', protocols='OpenFlow13')
        switches.append(switch)

        # Connect the switch to its parent (if any)
        if parent_switch:
            net.addLink(parent_switch, switch)
            parent_map[parent_switch] = parent_map.get(parent_switch, []) + [switch]

        # Add hosts to leaf switches
        if level == depth:
            for i in range(fanout):
                host_id = len(hosts) + 1
                host = net.addHost(f'h{host_id}', ip=f'10.0.{host_id}.1/24')
                hosts.append(host)
                net.addLink(host, switch)
        else:
            # Recursively build children
            for i in range(fanout):
                build_tree(level + 1, switch)

    # Start building the tree from the root
    build_tree(1)

    # Start the network
    net.start()

    # VLAN Configuration
    for i, switch in enumerate(switches):
        vlan_id = 10 if (i % 2 == 0) else 20  # Alternate VLAN IDs
        for intf in switch.intfs.values():
            if 'eth' in str(intf):  # Filter to only physical interfaces
                switch.cmd(f'ovs-vsctl set port {intf} tag={vlan_id}')

    # Testing
    print("Testing connectivity within VLANs...")
    if len(hosts) > 1:
        net.ping([hosts[0], hosts[1]])  # Test VLAN 10
    if len(hosts) > 2:
        net.ping([hosts[2], hosts[3]])  # Test VLAN 20
    print("Testing cross-VLAN connectivity (should fail)...")
    if len(hosts) > 3:
        net.ping([hosts[0], hosts[2]])  # Test VLAN isolation

    # Open CLI for further exploration
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_tree_topo()
