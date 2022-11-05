import hashlib
import json
from datetime import datetime

#init difficulty
difficulty = 5
#previous block time
prev_time = datetime.now()

class block(object):
    def __init__(self, index, transactions, timestamp, previous_hash, current_hash, difficulty, proof):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.current_hash = current_hash
        self.difficulty = difficulty
        self.proof = proof

    def change_difficulty(self, delta):
        global difficulty
        if (delta.total_seconds() < 5):
            difficulty += 1
        if (delta.total_seconds() > 15):
            difficulty -= 1

    #get hash of current block using other data of block
    def hash_block(self, transactions, index, timestamp, previous_hash, proof):
        t = hashlib.sha256(transactions.encode('utf-8')).hexdigest()
        i = hashlib.sha256(str(index).encode('utf-8')).hexdigest()
        ts = hashlib.sha256(timestamp.strftime("%m%d%Y%H%M%S").encode('utf-8')).hexdigest()
        ph = hashlib.sha256(previous_hash.encode('utf-8')).hexdigest()
        p = hashlib.sha256(str(proof).encode('utf-8')).hexdigest()
        final_hash = hashlib.sha256((t+i+ts+ph+p).encode('utf-8')).hexdigest()
        return final_hash
    
    #get hash of block+nonce
    def hash_nonce(self):
        return hashlib.sha256((str(self.proof)+self.current_hash).encode('utf-8')).hexdigest()

    #mine a block
    def mine(self):
        difficulty = self.difficulty
        prev_time = datetime.now()
        hash1 = hashlib.sha256(str(block).encode('utf-8')).hexdigest()
        while True:
            hash2 = self.hash_nonce()
            comp = ['0'] * difficulty
            if (hash2[:difficulty] == ''.join(comp)):
                print('hash2', hash2)
                break
            else:
                self.proof += 1
        this_time = datetime.now()
        #change difficulty
        delta = this_time - prev_time
        print('difficulty:', difficulty, '  time took:', delta.total_seconds())
        self.change_difficulty(delta)
        return hash2,difficulty

def main():
    #b tries to mine block
    b = block(index=0, 
                transactions='a', 
                timestamp=datetime.now(), 
                previous_hash="", 
                current_hash=None, 
                difficulty=5, 
                proof=0)
    b.current_hash = b.hash_block(b.transactions, b.index, b.timestamp, b.previous_hash, b.proof)
    hash,dif = b.mine()
    #adds the mined block to chain
    b2 = block(index=b.index+1,
                transactions='OwO',
                timestamp=datetime.now(),
                previous_hash=hash,
                current_hash=None,
                difficulty = dif,
                proof=0)
    print(b2.previous_hash)

if __name__ == "__main__":
    main()
