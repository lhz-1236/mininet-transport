import time
import argparse
from testnb import setup_environment


server_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server","source ~/.profile","go run main0.go 10.0.0.2",":4435 > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server",".logs 2>&1"]

client_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client","source ~/.profile","go run main-exp-large-file0.go --m=" ," 10.0.0.2"," > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client",".logs 2>&1"]


def setup():
    network = setup_environment()
    network.start()
    return network


def exec_test():
    network = setup()
    server = network.get("servermp")
    client = network.get("clientmp")
    for i in range(1):
    	if i == 0:
        	cmd = server_cmd[2]+"2"+server_cmd[3]+str(i)+server_cmd[4]
    	else:
        	cmd = server_cmd[2]+str(i+1)+server_cmd[3]+str(i)+server_cmd[4]
    	server.sendCmd(server_cmd[0]+"&&"+server_cmd[1]+"&&"+cmd)

    for i in range(1):
    	if i == 0:
        	cmd = client_cmd[2]+"true"+client_cmd[3]+"2"+client_cmd[4]+str(i)+client_cmd[5]
    	else:
        	cmd = client_cmd[2]+"false"+client_cmd[3]+str(i+1)+client_cmd[4]+str(i)+client_cmd[5] 	
    	client.sendCmd("sleep 1"+"&&"+client_cmd[0]+"&&"+client_cmd[1]+"&&"+cmd)
 
        
    for i in range(1):
    	client.monitor()
    	server.monitor()

    if client[0].waiting&client[1].waiting&client[1].waiting:
        delta = 20
        client.sendInt()
        for i in range(1):
        	client.sendInt()
        	server.sendInt()
        	client.waiting = False
        	server.waiting = False      
        time.sleep(1)
        network.cleanup()
   


if __name__ == '__main__':

    exec_test()
