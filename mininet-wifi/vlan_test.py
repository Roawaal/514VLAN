from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI

def topology():
    net = Mininet_wifi(controller=Controller)

    info("*** Creating access points\n")
    ap1 = net.addAccessPoint('ap1', ssid="student_network", mode="g", channel="1", position="10,20,0")
    ap2 = net.addAccessPoint('ap2', ssid="faculty_network", mode="g", channel="6", position="50,50,0")

    info("*** Creating stations\n")
    student1 = net.addStation('sta1', ip="10.0.10.1/24", position="0,0,0")
    student2 = net.addStation('sta2', ip="10.0.10.2/24", position="0,10,0")
    faculty1 = net.addStation('sta3', ip="10.0.20.1/24", position="60,60,0")
    faculty2 = net.addStation('sta4', ip="10.0.20.2/24", position="70,70,0")

    info("*** Configuring wireless network\n")
    net.configureWifiNodes()

    info("*** Adding links\n")
    net.addLink(ap1, student1)
    net.addLink(ap1, student2)
    net.addLink(ap2, faculty1)
    net.addLink(ap2, faculty2)

    info("*** Starting network\n")
    net.build()
    net.start()

    info("*** Configuring mobility\n")
    # Start mobility
    net.startMobility(time=0)

    # Define movement for station sta1
    net.mobility('sta1', 'start', time=1, position='10,10,0')
    net.mobility('sta1', 'stop', time=5, position='50,50,0')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
