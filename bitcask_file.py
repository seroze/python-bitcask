import time 
import uuid 
import codec 
from collections import namedtuple 

"""
A single record in a bitcask file 

---------------------------------------------------------
| timestamp | key_size | value_size | key | value       |
---------------------------------------------------------
Note: we are ignoring crc(checksum) field 

"""

Record = namedtuple("Record", ['timestamp', 'keysize', 'valuesize', 'key', 'value'])

class BitcaskFile:

    """
    Class representing a bitcask file, all storage related operations are performed via this object
    """

    def __init__(self, dir, filename=str(uuid.uuid4()), offset=0):
        self.filename = '/'.join([dir, filename])
        self.offset = offset 

    def _load_next_record(self):
        read_bytes = 0 
        with open(self.filename, 'rb') as f:
            f.seek(self.offset, 0) # 0 indicates the offset is from beginning of the file
            meta_bytes = f.read(codec.METADATA_BYTE_SIZE)
            if meta_bytes: # why do we need this check ? 
                (timestamp, keysize, valuesize) = codec.decode_metadata(meta_bytes)
                key_bytes = f.read(keysize)
                value_bytes = f.read(valuesize)
                key = key_bytes.decode() 
                value = value_bytes.decode() 
                read_bytes += len(meta_bytes) + keysize + valuesize 
                self.offset += read_bytes 
                return Record(timestamp, keysize, valuesize, key, value)
            

    def write(self, key, value):
        """
        Encode the data and append to file 
        """
        keysize = len(key) 
        valuesize = len(value)
        timestamp = time.time() # epoch time 
        record = Record(timestamp, keysize, valuesize, key, value) 
        data = codec.encode(record)
        with open(self.filename, 'ab') as f:
            count = f.write(data)
        # if you do write does the offset change
        curr_offset = self.offset 
        self.offset += count 
        return (timestamp, curr_offset, count)

    def read(self, pos, size):
        """
        read bytes from the file and decode into record 
        """
        data = b'' #empty byte
        with open(self.filename, 'rb') as f: 
            f.seek(pos, 0)
            data = f.read(size)

        return codec.decode(data).value