import hashlib
import json
from time import time
from detect_anomalies import check_all_anomalies, check_manual_anomalies

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time()
        self.hash = self.compute_initial_hash()

    def compute_initial_hash(self):
        block_string = json.dumps(self.prepare_dict(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def prepare_dict(self):
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
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        nonce = 0
        while True:
            block.nonce = nonce
            hash_ = hashlib.sha256(json.dumps(block.prepare_dict(), sort_keys=True).encode()).hexdigest()
            if hash_.startswith('0000'):
                return hash_
            nonce += 1

    def add_block(self, block, proof):
        block.hash = proof
        self.chain.append(block)
        print(f"Block {block.index} added successfully with hash {block.hash}.")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != hashlib.sha256(json.dumps(current.prepare_dict(), sort_keys=True).encode()).hexdigest():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

def run_database_anomalies():
    database_path = "voting_system.db"
    result = check_all_anomalies(database_path)
    print(result)

def run_manual_anomaly_tests():
    test_cases = [
        {'votes': 120, 'registered_voters': 100, 'previous_votes': 80, 'description': "More votes than registered voters and sudden spike"},
        {'votes': 80, 'registered_voters': 100, 'previous_votes': 50, 'description': "Normal voting scenario"},
        {'votes': 0, 'registered_voters': 100, 'previous_votes': 0, 'description': "No votes cast - potential issue"},
        {'votes': 100, 'registered_voters': 100, 'previous_votes': 70, 'description': "Votes equal to registered voters"},
        {'votes': 200, 'registered_voters': 200, 'previous_votes': 150, 'description': "High turnout but normal increase"},
    ]

    for case in test_cases:
        print(f"\nTesting case: {case['description']}")
        anomalies = check_manual_anomalies(case['votes'], case['registered_voters'], case['previous_votes'])
        if anomalies:
            for anomaly in anomalies:
                print(f"Anomaly detected: {anomaly}")
        else:
            print("No anomalies detected.")

def main():
    blockchain = Blockchain()
    new_block = Block(index=1, transactions={'voter_id': 1, 'candidate_id': 101}, previous_hash=blockchain.chain[-1].hash)
    proof = blockchain.proof_of_work(new_block)
    blockchain.add_block(new_block, proof)

    print("\nBlockchain is valid:", blockchain.is_chain_valid())
    print("\nBlockchain details:")
    for block in blockchain.chain:
        print(f"Block {block.index}: {block.transactions}, Hash: {block.hash}")

    print("\nRunning database-driven anomaly detection:")
    run_database_anomalies()

    print("\nRunning manual anomaly tests:")
    run_manual_anomaly_tests()

if __name__ == "__main__":
    main()

