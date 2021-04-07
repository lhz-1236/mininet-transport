from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSBridge, Host,Controller
from mininet.link import TCIntf
from mininet.util import custom
b=[8,16]
d=["15ms","15ms"]
def setup_environment():
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge,intf=custom(TCIntf),controller=Controller)

    server = net.get("server0","server1","server2")
    client = net.get("client0","client1","client2")
    for i in range(3):
    	server[i].setIP("10.0.0.2%s"%(i+1),intf="server%s-eth0"%i)

    for i in range(3):
        client[0].setIP("10.0.1.%s"%(i+1),intf = "client0-eth%s"%i)
        client[0].cmd("ip rule add from 10.0.1.%s table %s"%(i+1,i+1))
        client[0].cmd("ip route add 10.0.0.0/8 dev client0-eth%s scope link table %s"%(i,i+1))
        client[0].cmd("ip route add default via 10.0.0.22 dev client0-eth%s table %s"%(i,i+1))

    for i in range(1,3):
        client[i].setIP("10.0.1.%s"%(i+3),intf = "client%s-eth0"%i)
        client[i].cmd("ip rule add from 10.0.1.%s table %s"%(i+3,i+3))
        client[i].cmd("ip route add 10.0.0.0/8 dev client%s-eth0 scope link table %s"%(i,i+3))
        client[i].cmd("ip route add default via 10.0.0.2%s dev client%s-eth0 table %s"%(i+1,i,i+3))

    return net


class DoubleConnTopo(Topo):

    def build(self):
	#c0 = self.addController('c0')
        client = []
        server = []
        s = []
        for i in range(3):
        	client.append(self.addHost("client"+str(i)))
        	server.append(self.addHost("server"+str(i)))
        for i in range(5):
        	s.append(self.addSwitch('s'+str(i+1)))

        for i in range(2):
            self.addLink(s[i], s[i+2], bw = b[i], delay = d[i], max_queue_size = 350,loss=1)
            self.addLink(s[i+2], s[4], bw=40,delay = '5ms',max_queue_size = 350,loss=0)

        self.addLink(s[0], client[1],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[0], client[0],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[0], client[0],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[1], client[0],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[1], client[2],bw=40,delay = '5ms',max_queue_size = 350,loss=0)

        self.addLink(s[2],server[1],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[4],server[0],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
        self.addLink(s[3],server[2],bw=40,delay = '5ms',max_queue_size = 350,loss=0)
if __name__ == '__main__':
    NET = setup_environment()
    
    NET.start()  
    CLI(NET)
    NET.stop()
