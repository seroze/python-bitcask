import os 
from bitcask_file import BitcaskFile
from keydir import KeyDir

class BitcaskDb:
    # class level attribute
    _instance = None 

    def __new__(cls, dir):
        # singleton design pattern 
        if cls._instance is None:
            cls._instance = super(BitcaskDb, cls).__new__(cls) 
            cls._instance.setup(dir)
        return cls._instance
    
    def setup(self, dir):
        self.dir = dir 
        # create dir if not exists
        os.makedirs(self.dir, exist_ok=True)
        self.active_file = BitcaskFile(self.dir)
        self.filemap = {self.active_file.filename: self.active_file}
        self.keydir = KeyDir() 
        self.populate_keys()

    def populate_keys(self):
        """
        rebuild keydir in memory from existing db by reading through every 
        file 
        """