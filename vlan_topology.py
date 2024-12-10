from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import Link, TCLink
from mininet.topo import Topo
from mininet.cli import CLI

class CampusVLAN(Topo):
    def build(self):
       
        switch = self.addSwitch('s1')

        
        student1 = self.addHost('h1', ip='10.0.10.1/24')
        student2 = self.addHost('h2', ip='10.0.10.2/24')
        faculty1 = self.addHost('h3', ip='10.0.20.1/24')
        faculty2 = self.addHost('h4', ip='10.0.20.2/24')

        
        self.addLink(student1, switch)
        self.addLink(student2, switch)
        self.addLink(faculty1, switch)
        self.addLink(faculty2, switch)

def run():
    
    topo = CampusVLAN()
    net = Mininet(topo=topo, controller=Controller, link=TCLink, switch=OVSSwitch)
    net.start()

    
    switch = net.get('s1')
    switch.cmd('ovs-vsctl add-br br0')
    switch.cmd('ovs-vsctl add-port br0 s1-eth1 tag=10')  # 学生 VLAN
    switch.cmd('ovs-vsctl add-port br0 s1-eth2 tag=10')  # 学生 VLAN
    switch.cmd('ovs-vsctl add-port br0 s1-eth3 tag=20')  # 教师 VLAN
    switch.cmd('ovs-vsctl add-port br0 s1-eth4 tag=20')  # 教师 VLAN

    print("Testing connectivity within VLANs...")
    net.ping([net.get('h1'), net.get('h2')]) 
    net.ping([net.get('h3'), net.get('h4')])  
    print("Testing cross-VLAN connectivity (should fail)...")
    net.ping([net.get('h1'), net.get('h3')])  
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()

