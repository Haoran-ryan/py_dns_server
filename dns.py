import socket, glob

port = 53 # DNS operates on port 53 by default 
ip = "127.0.0.1" 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port)) # bind takes 1 parameter 

def load_zone():
    zonefiles = glob.glob('zones/*.zone')

zonedata = load_zone()
def getflags(flags):
    # NOTE: unit conversion : Byte -> bit 
    '''
       0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    '''
    # 1st Byte : 0 ~ 7bits (8 in totoal)
    byte1 = bytes(flags[:1])
    # 2nd Byte:  8 ~ 15 
    byte2 = bytes(flags[1:2])
     
    rflags = ''
    QR = '1'
    
    OPCODE = ''
    for bit in range(1,5):
        # TODO：review bit shift
        OPCODE += str(ord(byte1)&(1<<bit))
    
    AA = '1'
    TC = '0'
    RD = '0'
    
    RA= '0'
    Z ='000'
    RCODE = '0000'
    
    return int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder='big') + int(RA+Z+RCODE, 2).to_bytes(1, 'big')

def getquestiondomain(data):
    state = 0
    expectedlen = 0 
    domainstring = ''
    domainparts = []
    x = 0 
    y = 0 
    for byte in data:
        if state == 1:
            domainstring += chr(byte)
            x += 1 # x is the length of the domainstring
            if x == expectedlen:
                domainparts.append(domainstring)
                domainparts=''
                state = 0
                x = 0 
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            # 传入的信息格式：信息长度 + 实际信息
            # state = 0 ，则可以提取传入信息的开头，即”信息长度“
            state = 1
            expectedlen = byte 
        x += 1 
        y += 1 # y is the length of the data 
        
    questiontype = data[y+1:y+3] 
    return (domainparts, questiontype)
        

def getrecs(data):
    domain, questiontype = getquestiondomain(data)
    at = ''
    if questiontype == b'\x00\x01':
        qt = 'a'
        
    zone = getzone(domain)
def buildresponse(data):
    # data in stream of Bytes 
    transactionID = data[0:2]
    TID =""
    for byte in transactionID:
        TID += hex(byte)[2:]  # remove '0x'
    
    # Get the flags
    flags = getflags(data[2:4])
    
    # Question count
    QDCOUNT = b'\x00\x01'
    
    # Answer count 
    # NOTE: Header takes 12 bytes in total, therefore the question count starts at 12th byte
    """_DNS protocol format_ 
    +---------------------+
    |   Header (12 bytes) |
    +---------------------+
    |    Question         |  
    +---------------------+
    |    Answer           |
    +---------------------+
    |  Authority          |
    +---------------------+
    |  Additional         |
    +---------------------+
    """
    # getquestiondomain(data[12:])
    
    getrecs(data[12:])
    
while True:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
