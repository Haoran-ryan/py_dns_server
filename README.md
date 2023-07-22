# py_dns_server

## DNS uses raw bi codes 

```python3
import socket

port = 53 # DNS operates on port 53 by default 
ip = "127.0.0.1" 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port)) # bind takes 1 parameter 

while True:
    data, addr = sock.recvfrom(512)
    print(data)

```

use the dig in the terminal to mimic a dns query on 127.0.0.1 and the following is the output:
```
dns_server git:(main) ✗ sudo python3 dns.py
b'\x00\xcf\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'
b'\x00\xcf\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'
b'\x00\xcf\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'
```

## DNS header 

                                   1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

1. transactsionID - 16 bits / 2 Bytes | the response received comes from the server requested from
1. flags - 16b/2B in total
    1. QR - 1 bit | 0 query , 1 response 
    1. OPCODE - 4 bit 
        1. 0 standard query, ...
        1. from original `query` and copied into `response` 


## Python位操作和掩码在处理二进制数据中的应用

### 问题
在Python中处理DNS协议消息头部标志字段时，为何要用到位操作和掩码？

### 常见误区
* 误解1: 我们可以直接通过比较操作（如==1）来检查一个字节中特定位置的位的值。
* 误解2: “1”只是一个位的值，没有特殊含义。

### 解答
1. **位操作和掩码的概念：**
   * 在Python等编程语言中，位操作可以直接在二进制级别上处理数据。掩码（Mask）是一种常见的位操作技术，通常用于控制或检查某个数值中的特定位。
2. **为何使用位操作：**
   * 在处理网络协议或其他包含复杂位字段的数据结构时，位操作是一个非常有用的工具。例如，在DNS协议中，头部的"标志"字段中每一位都有特定的含义。因此，我们需要用到位操作来检查或设置这些特定位置的位的值。
3. **为何使用掩码：**
   * 掩码用于生成一个二进制数字，这个数的二进制表示中只有一个位是1（位置由我们自己决定），其余位都是0。然后，我们将这个掩码和目标字节进行位与操作，这样可以检查目标字节在特定位置上的位是否是1。这是一种高效的方式来检查一个字节中特定位置的位的值，无需将整个字节转换为其他格式（如字符串或整数）。
4. **"1"和"0"的含义：**
   * 在处理二进制数据时，"1"和"0"不仅仅是位的值，他们实际上代表了信息。每一位在字节中的位置，都可能有特定的含义。因此，我们需要检查特定位置的位是否为1或0，以解码包含在那个字节中的信息。
