from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_torus_topo():
    # Initialize Mininet with a remote controller
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Add a remote controller
    controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Number of switches per ring and number of rings
    n = 4  # Number of switches in one ring
    m = 3  # Number of rings

    switches = []
    hosts = []

    # Create switches and hosts
    for i in range(1, n * m + 1):
        switch = net.addSwitch(f's{i}', protocols='OpenFlow13')
        switches.append(switch)

        # Each switch connects to one host
        host = net.addHost(f'h{i}', ip=f'10.0.{i}.1/24')
        hosts.append(host)
        net.addLink(host, switch)

    # Connect switches in a torus topology
    for ring in range(m):
        for i in range(n):
            # Current switch
            curr = ring * n + i
            # Connect horizontally
            net.addLink(switches[curr], switches[ring * n + (i + 1) % n])
            # Connect vertically
            net.addLink(switches[curr], switches[(curr + n) % (n * m)])

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
    net.ping([hosts[0], hosts[2]])  # Should succeed (VLAN 10)
    net.ping([hosts[1], hosts[3]])  # Should succeed (VLAN 20)
    print("Testing cross-VLAN connectivity (should fail)...")
    net.ping([hosts[0], hosts[1]])  # Should fail (different VLANs)

    # Open CLI for further exploration
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_torus_topo()
