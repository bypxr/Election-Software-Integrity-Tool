
#4
import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established.")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully.")
    except Error as e:
        print(e)

def insert_voter(conn, voter):
    """Insert a new voter into the voters table"""
    sql = ''' INSERT INTO voters(registration_date, precinct)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, voter)
    conn.commit()
    return cur.lastrowid

def insert_vote(conn, vote):
    """Insert a new vote into the votes table"""
    sql = ''' INSERT INTO votes(vote_id, voter_id, candidate_id, timestamp, location)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, vote)
    conn.commit()
    return cur.lastrowid

def load_data(conn):
    """Load voters and votes data from the database and return as Pandas DataFrames"""
    voters_df = pd.read_sql_query("SELECT * FROM voters", conn)
    votes_df = pd.read_sql_query("SELECT * FROM votes", conn)
    return voters_df, votes_df

def check_exceeding_votes(voters_df, votes_df):
    """Check if the number of votes exceeds the number of registered voters in any precinct"""
    # Count votes per precinct
    vote_counts = votes_df.groupby('location').size()

    # Count voters per precinct
    voter_counts = voters_df.groupby('precinct').size()

    anomalies = []
    for precinct, voter_count in voter_counts.items():
        vote_count = vote_counts.get(precinct, 0)
        if vote_count > voter_count:
            anomalies.append((precinct, voter_count, vote_count))

    return anomalies

def main():
    database = "voting_system.db"
    sql_create_voters_table = """ CREATE TABLE IF NOT EXISTS voters (
                                        voter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        registration_date TEXT,
                                        precinct TEXT
                                    ); """
    sql_create_votes_table = """ CREATE TABLE IF NOT EXISTS votes (
                                     vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     voter_id INTEGER NOT NULL,
                                     candidate_id INTEGER,
                                     timestamp TEXT,
                                     location TEXT,
                                     FOREIGN KEY (voter_id) REFERENCES voters (voter_id)
                                 ); """
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_voters_table)
        create_table(conn, sql_create_votes_table)

        # Expanded data insertion
        voters = [
            ('2024-04-01', 'Precinct 1'),
            ('2024-04-02', 'Precinct 1'),
            ('2024-04-03', 'Precinct 2'),
            ('2024-04-04', 'Precinct 2'),
            ('2024-04-05', 'Precinct 3')  # Add more precincts as needed
        ]
        for voter in voters:
            voter_id = insert_voter(conn, voter)
            # Insert votes for each voter with varying candidates and times
            votes = [
                (None, voter_id, 100 + voter_id % 5, '2024-04-24 10:00:00', voter[1]),
                (None, voter_id, 100 + (voter_id + 1) % 5, '2024-04-24 11:00:00', voter[1])
            ]
            for vote in votes:
                insert_vote(conn, vote)

        # Load data and check for anomalies
        voters_df, votes_df = load_data(conn)
        anomalies = check_exceeding_votes(voters_df, votes_df)
        if anomalies:
            print("Potential fraud detected:")
            for precinct, voter_count, vote_count in anomalies:
                print(f"More votes ({vote_count}) than registered voters ({voter_count}) in {precinct}.")
        else:
            print("No anomalies detected.")
    else:
        print("Error! cannot create the database connection.")
    conn.close()



# main.py 
from alert_system import alert_system

votes = 105
registered_voters = 100

# Check and alert on anomalies
alert_system(votes, registered_voters)
