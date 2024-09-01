import struct 
from collections import namedtuple

import bitcask_file 

# > denotes big endianness, otherwise systems native endianess would kick in
# q denotes integer of 8 bytes, read more about struct pack() and unpack()
METADATA_FORMAT = ">qqq"
METADATA_BYTE_SIZE = 24 # 3*8 bytes 

def encode(record):
    
    key_size = record.key_size 
    value_size = record.value_size 
    timestamp = record.timestamp 

    key = record.key 
    value = record.value 

    metadata = struct.pack(METADATA_FORMAT, timestamp, key_size, value_size)
    data = key.encode() + value.encode()

def decode_metadata(data):
    (timestamp, keysize, valuesize) = struct.unpack(METADATA_FORMAT, data)
    return (timestamp, keysize, valuesize)

def decode(data):
    (timestamp, keysize, valuesize) = decode_metadata(data[:METADATA_BYTE_SIZE])
    data_str = data[METADATA_BYTE_SIZE:]
    key = data_str[:keysize]
    value = data_str[keysize:]
    return bitcask_file.Record(timestamp, keysize, valuesize, key, value)
