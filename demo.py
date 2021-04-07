import time
import argparse
from basicTopo1 import setup_environment


server_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server","source ~/.profile","go run main0.go 10.0.0.2",":4435 > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server",".logs 2>&1"]

client_cmd = ["cd /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client","source ~/.profile","go run main-exp-large-file0.go --m=" ," 10.0.0.2"," > /home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client",".logs 2>&1"]


def setup():
    network = setup_environment()
    network.start()
    return network


def exec_test():
    network = setup()
    server = network.get("server0","server1","server2")
    client = network.get("client0","client1","client2")
    for i in range(3):
    	if i == 0:
        	cmd = server_cmd[2]+str(i+1)+server_cmd[3]+str(i)+server_cmd[4]
    	else:
        	cmd = server_cmd[2]+str(i+1)+server_cmd[3]+str(i)+server_cmd[4]
    	server[i].sendCmd(server_cmd[0]+"&&"+server_cmd[1]+"&&"+cmd)
    	server[i].waiting = False 
    	server[i].sendCmd("cd /home/lhz/mininet/D-ITG/D-ITG-2.8.1-r1023/bin"+"&&"+"./ITGRecv")
    for i in range(3):

    	if i == 0:
        	cmd = client_cmd[2]+"true"+client_cmd[3]+str(i+1)+client_cmd[4]+str(i)+client_cmd[5]
    	else:
        	cmd = client_cmd[2]+"false"+client_cmd[3]+str(i+1)+client_cmd[4]+str(i)+client_cmd[5] 	
    	client[i].sendCmd("sleep 1"+"&&"+client_cmd[0]+"&&"+client_cmd[1]+"&&"+cmd)
    for i in range(3):
    	client[i].waiting = False
    	client[i].cmd('sleep 2')
    	client[i].sendCmd("cd /home/lhz/mininet/D-ITG/D-ITG-2.8.1-r1023/bin"+"&&"+"./ITGSend -a 10.0.0.2%s -sp 9400 -rp 9500 -C 4500 -c 1000 -t 3000 -x recv_log_file%s"%(i+1,i))
        
    for i in range(3):
    	client[i].monitor()
    	server[i].monitor()
    	server1[i].monitor()
    if client[0].waiting&client[1].waiting&client[1].waiting:
        delta = 20
        client.sendInt()
        for i in range(3):
        	client[i].sendInt()
        	server[i].sendInt()
        	client[i].waiting = False
        	server[i].waiting = False      
        time.sleep(1)
        network.cleanup()
   


if __name__ == '__main__':

    exec_test()
