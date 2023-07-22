import socket

port = 53 # DNS operates on port 53 by default 
ip = "127.0.0.1" 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port)) # bind takes 1 parameter 

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
def buildresponse(data):
    # data in stream of Bytes 
    transactionID = data[0:2]
    TID =""
    for byte in transactionID:
        TID += hex(byte)[2:]  # remove '0x'
    
    # Get the flags
    flags = getflags(data[2:4])
    
    print(flags)
    
while True:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
