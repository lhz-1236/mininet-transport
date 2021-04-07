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
    server = net.get('server0','server1')
    client = net.get('client0','client1')

    servermp.setIP("10.0.3.1", intf="servermp-eth0")
    server[0].setIP("10.0.3.2", intf="server0-eth0")
    server[1].setIP("10.0.3.3", intf="server1-eth0")

    client[0].setIP("10.0.2.1", intf="client0-eth0")
    client[0].cmd("ip rule add from 10.0.2.1 table 10")
    client[0].cmd("ip route add 10.0.0.0/8 dev client0-eth0 scope link table 10")
    client[0].cmd("ip route add default via 10.0.3.2 dev client0-eth0 table 10")

    client[1].setIP("10.0.2.2", intf="client1-eth0")
    client[1].cmd("ip rule add from 10.0.2.2 table 11")
    client[1].cmd("ip route add 10.0.0.0/8 dev client1-eth0 scope link table 11")
    client[1].cmd("ip route add default via 10.0.3.3 dev client1-eth0 table 11")
    for i in range(linknum):
        clientmp.setIP("10.0.1.%s"%(i+1),intf = "clientmp-eth%s"%i)
        clientmp.cmd("ip rule add from 10.0.1.%s table %s"%(i+1,i+1))
        clientmp.cmd("ip route add 10.0.0.0/8 dev clientmp-eth%s scope link table %s"%(i,i+1))
        clientmp.cmd("ip route add default via 10.0.3.1 dev clientmp-eth%s table %s"%(i,i+1))

    
    return net


class DoubleConnTopo(Topo):

    def build(self):
        clientmp = self.addHost("clientmp")
        client = []
        client.append(self.addHost("client0"))
        client.append(self.addHost("client1"))

        servermp = self.addHost("servermp")
        server = []
        server.append(self.addHost("server0"))
        server.append(self.addHost("server1"))

        switch=[]
        for i in range(3):
            switch.append(self.addSwitch('s%s'%(i+1)))

        self.addLink(switch[2], clientmp, bw = 100, delay = '5ms', max_queue_size = 150,loss=0, use_htb = True)
        self.addLink(switch[2], switch[0], bw=20, delay='5ms', max_queue_size=80, loss=0, use_htb = True)
        for i in range(linknum-1):
            self.addLink(switch[0], clientmp, bw = 100, delay = '5ms', max_queue_size = 100,loss=0, use_htb = True)
        self.addLink(switch[0], client[0], bw = 100, delay = '5ms', max_queue_size = 150,loss = 0, use_htb = True)
        self.addLink(switch[2], client[1], bw = 100, delay = '5ms', max_queue_size = 150,loss = 0, use_htb = True)
        self.addLink(switch[0], switch[1], bw = 20, delay = '20ms', max_queue_size = 80,loss = 0, use_htb = True)
        self.addLink(switch[0], server[1], bw = 100, delay = '5ms', max_queue_size = 400,loss = 0, use_htb = True)
        self.addLink(switch[1], servermp, bw=100, delay = '5ms', max_queue_size = 150,loss=0, use_htb = True)
        self.addLink(switch[1],server[0],bw = 100, delay = '5ms', max_queue_size = 150,loss=0, use_htb = True)

if __name__ == '__main__':
    NET = setup_environment()
    
    NET.start()  
    CLI(NET)
    NET.stop()

