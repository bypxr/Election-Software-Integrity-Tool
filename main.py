#version 3 
import tkinter as tk
import sqlite3
import pandas as pd
from sqlite3 import Error
from blockchain import Blockchain, Block  # Make sure to import your blockchain classes correctly

def create_connection(db_file="voting_system.db"):
    """Create a database connection to the SQLite database specified by db_file"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def load_data(conn):
    """Load voters and votes data from the database and return as Pandas DataFrames"""
    voters_df = pd.read_sql_query("SELECT * FROM voters", conn)
    votes_df = pd.read_sql_query("SELECT * FROM votes", conn)
    return voters_df, votes_df

def check_exceeding_votes(voters_df, votes_df):
    """Check if the number of votes exceeds the number of registered voters in any precinct"""
    anomalies = []
    vote_counts = votes_df.groupby('location').size()
    voter_counts = voters_df.groupby('precinct').size()
    for precinct, voter_count in voter_counts.items():
        vote_count = vote_counts.get(precinct, 0)
        if vote_count > voter_count:
            anomalies.append(f"More votes ({vote_count}) than registered voters ({voter_count}) in {precinct}.")
    return anomalies

def initialize_blockchain():
    """Initialize the blockchain with some data"""
    blockchain = Blockchain()
    transactions1 = [{'voter_id': 1, 'candidate_id': 101}, {'voter_id': 2, 'candidate_id': 102}]
    transactions2 = [{'voter_id': 3, 'candidate_id': 103}, {'voter_id': 4, 'candidate_id': 104}]
    
    new_block1 = Block(index=1, transactions=transactions1, previous_hash=blockchain.chain[-1].hash)
    proof1 = blockchain.proof_of_work(new_block1)
    blockchain.add_block(new_block1, proof1)

    new_block2 = Block(index=2, transactions=transactions2, previous_hash=blockchain.chain[-1].hash)
    proof2 = blockchain.proof_of_work(new_block2)
    blockchain.add_block(new_block2, proof2)
    return blockchain

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Election System Analysis with Blockchain')
        self.text_area = tk.Text(root, height=40, width=80)
        self.text_area.pack()

        self.blockchain = initialize_blockchain()
        
        tk.Button(root, text="Load Data and Check Anomalies", command=self.load_and_check_data).pack()
        tk.Button(root, text="Voter's/Candidate ID", command=self.display_blockchain_transactions).pack()

    def load_and_check_data(self):
        conn = create_connection()
        if conn is not None:
            voters_df, votes_df = load_data(conn)
            anomalies = check_exceeding_votes(voters_df, votes_df)
            display_text = "Voters:\n" + voters_df.to_string() + "\n\nVotes:\n" + votes_df.to_string() + "\n\n"
            if anomalies:
                display_text += "Voter,Canditate ID's:\n" + "\n".join(anomalies)
            else:
                display_text += "No anomalies detected."
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, display_text)
            conn.close()

    def display_blockchain_transactions(self):
        display_text = "Voter/Canditate Id's:\n\n"
        for block in self.blockchain.chain:
            display_text += f"Block {block.index}: {block.hash}\n"
            for transaction in block.transactions:
                display_text += f"  Voter ID: {transaction['voter_id']}, Candidate ID: {transaction['candidate_id']}\n"
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

