import struct
import numpy as np

num = (b"R", 128.0, 128.0, 0.0, -64.0)

format_string = f'=1c{len(num)-1}f'

encodedpack = struct.pack(format_string,*num)
print(num)
print("Encoded data: ", encodedpack)
print("Length of encoded data: ", len(encodedpack))

decodedData = struct.unpack(format_string,encodedpack)
print(decodedData)

def Decoder(data):
    header = struct.unpack('1c',data[:1])[0].decode()
    print(header)
    match header:
        case 'R':
            data = struct.unpack('4f',data[1:])
        case 'V':
            data = struct.unpack('1f',data[1:])
        case 'D':
            data = struct.unpack('2f',data[1:])
    
    dataset = np.array(data)
    packet = (header[0], dataset)
    return packet



print(Decoder(encodedpack))
