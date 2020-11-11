import socket
import sys


def main():
    serverIP = sys.argv[1]
    serverPort = sys.argv[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        domainName = input()
        s.sendto(domainName.encode(), (serverIP, int(serverPort)))
        data, addr = s.recvfrom(1024)
        IP = data.decode().split(',')[1]
        print(IP)
    
if __name__ == "__main__":
    main()
   

