import hashlib
import json
from time import time

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions  # List of dicts, each dict a voting record
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time()  # Set the timestamp at the time of block creation
        self.hash = self.compute_initial_hash()  # Compute and set the initial hash

    def compute_initial_hash(self):
        """
        Compute the initial hash of the block using its initial state.
        """
        block_string = json.dumps(self.prepare_dict(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def prepare_dict(self):
        """
        Prepare the block's data for hashing, ensuring consistent data structure.
        """
        return {
            "index": self.index,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generate the genesis block and append it to the chain.
        """
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        """
        Perform the proof of work algorithm to find a nonce that results in a hash starting with '0000'.
        """
        nonce = 0
        while True:
            block.nonce = nonce
            hash_ = hashlib.sha256(json.dumps(block.prepare_dict(), sort_keys=True).encode()).hexdigest()
            if hash_.startswith('0000'):
                return hash_
            nonce += 1

    def add_block(self, block, proof):
        """
        Add the block to the blockchain after verifying its proof.
        """
        block.hash = proof  # Set the block's hash to the proof that was validated
        self.chain.append(block)
        print(f"Block {block.index} added successfully with hash {block.hash}.")

    def is_chain_valid(self):
        """
        Check if the blockchain is valid by ensuring each block's links and hashes are correct.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != hashlib.sha256(json.dumps(current.prepare_dict(), sort_keys=True).encode()).hexdigest():
                print(f"Invalid block at index {current.index}.")
                return False
            if current.previous_hash != previous.hash:
                print(f"Block {current.index} link mismatch: expected previous hash {current.previous_hash}, got {previous.hash}")
                return False
        print("Blockchain is valid.")
        return True

# Example usage in main function
def main():
    blockchain = Blockchain()
    # Example of adding a block with voter transactions
    transactions = [
        {'voter_id': 1, 'candidate_id': 101},
        {'voter_id': 2, 'candidate_id': 102},
        {'voter_id': 3, 'candidate_id': 103}
    ]
    new_block = Block(index=1, transactions=transactions, previous_hash=blockchain.chain[-1].hash)
    proof = blockchain.proof_of_work(new_block)
    blockchain.add_block(new_block, proof)

    print("Blockchain is valid:", blockchain.is_chain_valid())
    print("Block details:")
    for block in blockchain.chain:
        print(f"Block {block.index}: Transactions: {block.transactions}, Hash: {block.hash}")

if __name__ == "__main__":
    main()
