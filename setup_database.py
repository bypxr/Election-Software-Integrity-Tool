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
                                     vote_id INTEGER PRIMARY KEY,
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




        # Insert test data so that we can check if detect_anomalies.py works 
        voter1_id = insert_voter(conn, ('2024-04-01', 'Precinct 2'))
        voter2_id = insert_voter(conn, ('2024-04-01', 'Precinct 2'))
        insert_vote(conn, (None, voter1_id, 102, '2024-04-24 11:00:00', 'Precinct 2'))
        insert_vote(conn, (None, voter2_id, 103, '2024-04-24 11:05:00', 'Precinct 2'))
        insert_vote(conn, (None, voter1_id, 104, '2024-04-24 11:10:00', 'Precinct 2'))
        insert_vote(conn, (None, voter2_id, 105, '2024-04-24 11:15:00', 'Precinct 2'))
        insert_vote(conn, (None, voter2_id, 106, '2024-04-24 11:20:00', 'Precinct 2'))
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

if __name__ == '__main__':
    main()
