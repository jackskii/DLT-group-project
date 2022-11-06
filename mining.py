import hashlib
import json
from datetime import datetime
import random

DIFFICULTY_COUNT = 3

class block(object):
    def __init__(self, index, transactions, timestamp, previous_hash, current_hash, difficulty, proof):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.current_hash = current_hash
        self.difficulty = difficulty
        self.proof = proof

    #change difficulty if needed
    def change_difficulty(self, chain):
        #only change if more than 2*count is no the chain
        if (len(chain) <= DIFFICULTY_COUNT*2):
            return self.difficulty
        #calculate average of last three by curr block's timestamp - prev timestamp
        this_round_time = (self.timestamp - chain[-DIFFICULTY_COUNT].timestamp).total_seconds()
        last_round_time = (chain[-DIFFICULTY_COUNT].timestamp - 
                            chain[-(DIFFICULTY_COUNT*2)].timestamp).total_seconds()
        #if this round time > twice last round time, reduce difficulty
        if (this_round_time > last_round_time*2):
            return self.difficulty-1
        #if this round tiem < half last round time, increase difficulty
        if (this_round_time < last_round_time/2):
            return self.difficulty+1
        return self.difficulty



    #get hash of current block using other data of block
    def hash_block(self):
        t = hashlib.sha256((''.join(map(str, self.transactions))).encode('utf-8')).hexdigest()
        i = hashlib.sha256(str(self.index).encode('utf-8')).hexdigest()
        ts = hashlib.sha256(self.timestamp.strftime("%m%d%Y%H%M%S").encode('utf-8')).hexdigest()
        ph = hashlib.sha256(str(self.previous_hash).encode('utf-8')).hexdigest()
        d = hashlib.sha256(str(self.difficulty).encode('utf-8')).hexdigest()
        p = hashlib.sha256(str(self.proof).encode('utf-8')).hexdigest()
        final_hash = hashlib.sha256((t+i+ts+ph+d+p).encode('utf-8')).hexdigest()
        return final_hash
    

    #mine a block
    def mine(self):
        difficulty = self.difficulty
        start_time = datetime.now()
        hash1 = self.hash_block()
        while True:
            hash2 = hashlib.sha256((str(self.proof)+str(hash1)).encode('utf-8')).hexdigest()
            comp = ['0'] * difficulty
            if (hash2[:difficulty] == ''.join(comp)):
                break
            else:
                self.proof += 1
        this_time = datetime.now()
        return hash2

#print block nicely
def print_block(b):
    print("block nubmer: %s\n  timestamp: %s\n  previous_hash: %s\n  hash: %s\n  difficulty: %s\n  nonce: %s\n  transactions: %s\n" %
            (str(b.index),
            str(b.timestamp.strftime("%H:%M:%S")),
            str(b.previous_hash),
            str(b.current_hash),
            str(b.difficulty),
            str(b.proof),
            str("\n                ".join(map(str, b.transactions))))
            )
def main():
    #hard code blokchain info for now
    chain = []
    #b tries to mine block
    b = block(index=0, 
                transactions=['OwO','UwU','VwV'], 
                timestamp=datetime.now(), 
                previous_hash="", 
                current_hash=None, 
                difficulty=5, 
                proof=0)
    b.current_hash = b.hash_block()
    #hard coding
    chain.append(b)
    print_block(b)
    #loop to mine 10 blocks
    n = 10
    a = [0] * n
    #prev_hash init as hash of first block
    prev_hash = b.current_hash
    for i in range(10):
        #get some random data
        tt = [random.random()]
        temp = block(
            index = len(chain),
            transactions=tt, 
            timestamp=datetime.now(), 
            previous_hash=chain[-1].current_hash, 
            current_hash='',
            difficulty=chain[-1].difficulty, 
            proof=chain[-1].proof+1
        )
        temp.current_hash=temp.mine()
        temp.difficulty = temp.change_difficulty(chain)
        print_block(temp)
        chain.append(temp)

if __name__ == "__main__":
    main()
