from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSBridge, Host,Controller
from mininet.link import TCIntf
from mininet.util import custom
def setup_environment():
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge,intf=custom(TCIntf),controller=Controller)
    #server1 = net.get("server1")
    #client1 = net.get("client1")
    c0 = net.addController('c0')
    servermp = net.get("servermp")
    clientmp = net.get("clientmp")
    #server3 = net.get("server3")
    #client3 = net.get("client3")
    s1 = net.get("s1")
    s2 = net.get("s2")
    s3 = net.get("s3")
    s4 = net.get("s4")
    s5 = net.get("s5")

    #client1.setIP("10.0.0.1", intf="client1-eth0")
    clientmp.setIP("10.0.0.2", intf="clientmp-eth0")
    clientmp.setIP("10.0.0.3", intf="clientmp-eth1")
    clientmp.setIP("10.0.0.4", intf="clientmp-eth2")
    #client3.setIP("10.0.0.4", intf="client3-eth0")
    #server1.setIP("10.0.0.21", intf="server1-eth0")
    servermp.setIP("10.0.0.22", intf="servermp-eth0")
    #server3.setIP("10.0.0.23", intf="server3-eth0")
    clientmp.cmd("./scripts/clientmp.bash")
    #clientmp.cmd("./scripts/tc_client.bash")
    #s1.cmd("./scripts/s1.bash")

    return net


class DoubleConnTopo(Topo):

    def build(self):
	#c0 = self.addController('c0')
	#client1 = self.addHost("client1")
        #server1 = self.addHost("server1")
        
        clientmp = self.addHost("clientmp")
        servermp = self.addHost("servermp")
        #client3 = self.addHost("client3")
        #server3 = self.addHost("server3")
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        #self.addLink(s1, client1)
        self.addLink(s1, clientmp,bw=100,delay = '5ms',max_queue_size = 500)
        self.addLink(s1, clientmp,bw=100,delay = '5ms',max_queue_size = 500)
        #self.addLink(s3, client3)
        self.addLink(s3, clientmp,bw=100,delay = '5ms',max_queue_size = 500)
        self.addLink(s1,s2,bw=15,delay = '15ms',max_queue_size = 500)
        self.addLink(s3,s4,bw=10,delay = '5ms',max_queue_size = 500)
        self.addLink(s2,s5,bw=200,delay = '5ms',max_queue_size = 500)
        self.addLink(s4,s5,bw=100,delay = '5ms',max_queue_size = 500)
        #self.addLink(s2,server1)
        self.addLink(s5,servermp,bw=30,delay = '5ms',max_queue_size = 10)
        #self.addLink(s4,server3)
if __name__ == '__main__':
    NET = setup_environment()
    
    NET.start()  
    CLI(NET)
    NET.stop()
