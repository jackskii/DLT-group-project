import hashlib
import json
from datetime import datetime

#init difficulty
difficulty = 5
#previous block time
prev_time = datetime.now()

class block:
    def __init__(self, seq_no=0, prev_hash=None, data=None):
        self.seq_no = seq_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = datetime.now()


    #finds the hash of a block
    def nonce_hash(nonce, block):
        global difficulty
        global prev_time
        print(prev_time)
        hash1 = hashlib.md5(str(block).encode('utf-8')).hexdigest()
        for i in range(10000000):
            hash2 = hashlib.md5((str(nonce) + str(hash1)).encode('utf-8')).hexdigest()
            comp = ['0'] * difficulty
            if (hash2[:difficulty] == ''.join(comp)):
                print('hash2', hash2)
                print('yes')
                break
            else:
                nonce += 1
        this_time = datetime.now()
        #change difficulty
        delta = this_time - prev_time
        print(difficulty, delta.total_seconds())
        if (delta.total_seconds() < 5):
            difficulty += 1
        if (delta.total_seconds() > 15):
            difficulty -= 1
        return hash2

def main():
    #b tries to mine block
    b = block(data='abdasfd')
    hash = block.nonce_hash(1, b)

if __name__ == "__main__":
    main()
