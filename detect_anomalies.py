import sqlite3
import pandas as pd

def load_data(conn):
    """
    Load voters and votes data from the database and return as Pandas DataFrames.
    """
    voters_df = pd.read_sql_query("SELECT * FROM voters", conn)
    votes_df = pd.read_sql_query("SELECT * FROM votes", conn)
    return voters_df, votes_df

def check_exceeding_votes(voters_df, votes_df):
    """
    Check if the number of votes exceeds the number of registered voters in any precinct.
    """
    anomalies = []
    vote_counts = votes_df.groupby('location').size()
    voter_counts = voters_df.groupby('precinct').size()

    for precinct, voter_count in voter_counts.items():
        vote_count = vote_counts.get(precinct, 0)
        if vote_count > voter_count:
            anomalies.append((precinct, voter_count, vote_count))

    return anomalies

def check_all_anomalies(database_path):
    """
    Connect to the database, load data, perform checks, and return any detected anomalies.
    """
    conn = sqlite3.connect(database_path)
    try:
        voters_df, votes_df = load_data(conn)
        anomalies = check_exceeding_votes(voters_df, votes_df)
        if anomalies:
            return f"Potential fraud detected: {anomalies}"
        else:
            return "No anomalies detected."
    finally:
        conn.close()

