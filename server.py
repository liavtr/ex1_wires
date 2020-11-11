import time
import sys
import socket

def getDataFromFileAccordingToClientReq(fileName, clientReq):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.split(',')[0] == clientReq: #line.split(',')[0] = domain name
                return line
    return None

def leranNewData(fileName, data):
    #data = "domainName,IP,TTl"
    if data.endswith('\n'):
        data = data[:-1]
    timeOfLearning = str(time.time())
    data += ",dynamic," + timeOfLearning #data = "domainName,IP,TTl,dynamic,time"
    with open(fileName, "r+") as file:
        lines = file.readlines()
        lastLine = lines[-1]
        if not lastLine.endswith('\n'):
            file.write("\n")
            file.write(data)
        else:
            file.write(data)
    
def isTTLofDataPassed(TTL, timestamp):
    now = time.time()
    timePast = now - timestamp
    if timePast > TTL:
        return True
    return False

def deleteDataFromFile(ipsFileName, lineToDelete):
    with open("ips.txt", "r") as file:
        lines = file.readlines()
    with open("ips.txt", "w") as file:
        for line in lines:
            if line.split(",")[0] != lineToDelete.split(",")[0]:
                file.write(line)
                       
def getDataFromParentServer(parentIP, parentPort, clientReq):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(clientReq.split(',')[0].encode(), (parentIP, int(parentPort))) #clientReq.split(',')[0] = domain name
    data, addr = s.recvfrom(1024)
    s.close()
    return data

def main():
    myPort = sys.argv[1]
    parentIP = sys.argv[2]
    parentPort = sys.argv[3]
    ipsFileName = sys.argv[4]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind(('', int(myPort)))
    while True:
        clientReq, clientAddr = s.recvfrom(1024)
        clientReq = clientReq.decode()
        data = getDataFromFileAccordingToClientReq(ipsFileName, clientReq)
        if data != None: #client req is on file
            listOfData =  data.split(',')
            if len(listOfData) > 3: #data is dynamic      
                if isTTLofDataPassed(TTL=float(listOfData[2]), timestamp=float(listOfData[4])): 
                    deleteDataFromFile(ipsFileName, data)
                    dataFromParentServer = getDataFromParentServer(parentIP, parentPort, clientReq)
                    leranNewData(ipsFileName, dataFromParentServer.decode())
                    s.sendto(dataFromParentServer, clientAddr)
                    continue
                else:
                    s.sendto(data.encode(), clientAddr)   
            else: #data is static
                s.sendto(data.encode(), clientAddr)
        else: #client req is not on file
            dataFromParentServer = getDataFromParentServer(parentIP, parentPort, clientReq)
            leranNewData(ipsFileName, dataFromParentServer.decode())
            s.sendto(dataFromParentServer, clientAddr)


if __name__ == "__main__":
    main()
