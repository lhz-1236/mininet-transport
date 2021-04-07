from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSBridge, Host,Controller
from mininet.link import TCIntf
from mininet.util import custom
linknum=3
def setup_environment():
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge,intf=custom(TCIntf),controller=Controller)

    c0 = net.addController('c0')
    servermp = net.get("servermp")
    clientmp = net.get("clientmp")
    server = net.get('server0')
    client = net.get('client0')

    servermp.setIP("10.0.3.1", intf="servermp-eth0")
    server.setIP("10.0.3.2", intf="server0-eth0")

    client.setIP("10.0.2.1", intf="client0-eth0")
    client.cmd("ip rule add from 10.0.2.1 table 10")
    client.cmd("ip route add 10.0.0.0/8 dev client0-eth0 scope link table 10")
    client.cmd("ip route add default via 10.0.3.2 dev client0-eth0 table 10")
    for i in range(linknum):
        clientmp.setIP("10.0.1.%s"%(i+1),intf = "clientmp-eth%s"%i)
        clientmp.cmd("ip rule add from 10.0.1.%s table %s"%(i+1,i+1))
        clientmp.cmd("ip route add 10.0.0.0/8 dev clientmp-eth%s scope link table %s"%(i,i+1))
        clientmp.cmd("ip route add default via 10.0.3.1 dev clientmp-eth%s table %s"%(i,i+1))

    
    return net


class DoubleConnTopo(Topo):

    def build(self):
        clientmp = self.addHost("clientmp")
        client = self.addHost("client0")
        servermp = self.addHost("servermp")
        server = self.addHost("server0")
        switch=[]
        for i in range(2):
            switch.append(self.addSwitch('s%s'%(i+1)))
        
        for i in range(linknum):
            self.addLink(switch[0], clientmp, bw = 100, delay = '5ms', max_queue_size = 1000,loss=0)
        self.addLink(switch[0], client, bw = 100, delay = '5ms', max_queue_size = 1000,loss = 0)
        self.addLink(switch[0], switch[1], bw = 20, delay = '20ms', max_queue_size = 80,loss = 0)
        self.addLink(switch[1], servermp, bw=100, delay = '5ms', max_queue_size = 1000,loss=0)
        self.addLink(switch[1], server, bw=100, delay = '5ms', max_queue_size = 1000,loss=0)
if __name__ == '__main__':
    NET = setup_environment()
    
    NET.start()  
    CLI(NET)
    NET.stop()

