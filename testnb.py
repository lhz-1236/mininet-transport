from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSBridge, Host,Controller
from mininet.link import TCIntf
from mininet.util import custom
linknum=3
bw=[20,30,40]
delay=['5ms','10ms','15ms']
#max_queue_size=[80,120,240]
max_queue_size=[50,60,80]
'''
packetsize=100000bit
max queue delay=queuesize*pakcetsize/bw
8000*10000/40 000000
'''
def setup_environment():
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge,intf=custom(TCIntf),controller=Controller)

    c0 = net.addController('c0')
    servermp = net.get("servermp")
    clientmp = net.get("clientmp")
    client = net.get("client0","client1","client2")
    server = net.get("server0","server1","server2")
    servermp.setIP("10.0.3.1", intf="servermp-eth0")

    for i in range(linknum):
#client ip 10.0.2.*
#server ip 10.0.3.*

        client[i].setIP("10.0.2.%s"%(i+1),intf="client%s-eth0"%i)
        client[i].cmd("ip rule add from 10.0.2.%s table %s"%(i+1,i+5))
        client[i].cmd("ip route add 10.0.0.0/8 dev client%s-eth0 scope link table %s"%(i,i+5))
        client[i].cmd("ip route add default via 10.0.3.%s dev client%s-eth0 table %s"%(i+2,i,i+5))

        server[i].setIP("10.0.3.%s"%(i+2),intf="server%s-eth0"%(i))

#clientmp ip 10.0.1.*
        clientmp.setIP("10.0.1.%s"%(i+1),intf="clientmp-eth%s"%i)
        clientmp.cmd("ip rule add from 10.0.1.%s table 1%s"%(i+1,i+1))
        clientmp.cmd("ip route add 10.0.0.0/8 dev clientmp-eth%s scope link table 1%s"%(i,i+1))
        clientmp.cmd("ip route add default via 10.0.3.1 dev clientmp-eth%s table 1%s"%(i,i+1))

    return net


class DoubleConnTopo(Topo):

    def build(self):
        clientmp = self.addHost("clientmp")
        servermp = self.addHost("servermp")
        switch=[]
        client=[]
        server=[]
#s1----s(2*linknum+1)
        for i in range(2*linknum):
            switch.append(self.addSwitch('s%s'%(i+1)))
        switch.append(self.addSwitch('s%s'%(2*linknum+1)))

        for i in range(linknum):
            client.append(self.addHost("client"+str(i)))
            server.append(self.addHost("server"+str(i)))

        for i in range(linknum):
        	self.addLink(switch[i], clientmp, bw = 100, delay = '5ms', max_queue_size = 500,loss=0)
        	self.addLink(switch[i], client[i], bw = 100, delay = '5ms', max_queue_size = 500,loss=0)	
        	self.addLink(switch[i], switch[i+linknum], bw = bw[i], delay = delay[i], max_queue_size = max_queue_size[i],loss=0)
        	self.addLink(switch[i+linknum], switch[2*linknum], bw = 100, delay = '5ms', max_queue_size = 50,loss=0)
        	self.addLink(switch[i+linknum], server[i], bw = 100, delay = '5ms', max_queue_size = 50,loss=0)
        self.addLink(switch[2*linknum], servermp, bw = 500, delay = '5ms', max_queue_size = 2500,loss=0)

if __name__ == '__main__':
    NET = setup_environment()
    NET.start()  
    CLI(NET)
    NET.stop()

