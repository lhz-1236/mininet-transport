import time
import argparse
from testbs import setup_environment
linknum = 0

server_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server","source ~/.profile","go run main0.go 10.0.3.",":4435 > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code//logs/server",".logs 2>&1"]

client_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client","source ~/.profile","go run main-exp-large-file0.go --m=" ," 10.0.3."," > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/logs/client",".logs 2>&1"]


def setup():
    network = setup_environment()
    network.start()
    return network


def exec_test():
    network = setup()
    server = []
    client = []
    server.append(network.get("servermp"))
    client.append(network.get("clientmp"))
    server.append(network.get("server0"))
    client.append(network.get("client0"))
    server.append(network.get("server1"))
    client.append(network.get("client1"))
#    server = network.get("servermp","server0","server1","server2")
#    client = network.get("clientmp","client0","client1","client2")
 
    for i in range(3):
        cmd = server_cmd[2]+str(i+1)+server_cmd[3]+str(i)+server_cmd[4]
    	server[i].sendCmd(server_cmd[0]+"&&"+server_cmd[1]+"&&"+cmd)

    for i in range(3):
    	if i == 0:
        	cmd = client_cmd[2]+"true"+client_cmd[3]+"1"+client_cmd[4]+str(i)+client_cmd[5]
    	else:  
        	cmd = "sleep 7"+"&&"+client_cmd[2]+"false"+client_cmd[3]+str(i+1)+client_cmd[4]+str(i)+client_cmd[5] 
    	client[i].sendCmd("sleep 1"+"&&"+client_cmd[0]+"&&"+client_cmd[1]+"&&"+cmd)        	

    for i in range(3):
      out = client[i].monitor(timeoutms=10000)
    if client[0].waiting:
        for i in range(linknum+1):
        	client[i].sendInt()
        	client[i].waiting = False 
        print(1)
        network.stop()     
        time.sleep(1)
        network.cleanup()
   
    for i in range(3):
      server[i].sendInt()
      server[i].monitor()        
      server[i].waiting = False

if __name__ == '__main__':

    exec_test()
