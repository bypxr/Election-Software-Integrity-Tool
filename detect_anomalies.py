import pandas as pd
import sqlite3

def load_data(conn):
    """
    Load voters and votes data from the database and return as Pandas DataFrames
    """
    voters_df = pd.read_sql_query("SELECT * FROM voters", conn)
    votes_df = pd.read_sql_query("SELECT * FROM votes", conn)
    return voters_df, votes_df

def check_exceeding_votes(voters_df, votes_df):
    """
    Check if the number of votes exceeds the number of registered voters in any precinct
    """
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

# detect_anomalies.py might need an addition like this
def check_manual_anomalies(votes, registered_voters, previous_votes):
    # Mock-up function: this should implement similar checks as check_all_anomalies but directly use the arguments passed.
    if votes > registered_voters:
        return [f"More votes ({votes}) than registered voters ({registered_voters})."]
    if votes - previous_votes > 50:  # Arbitrary threshold for sudden spike
        return [f"Sudden spike detected: Previous votes {previous_votes}, current votes {votes}."]
    if votes == 0:
        return ["No votes cast - potential issue."]
    return []
