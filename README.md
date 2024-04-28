
# Automated Voter Fraud Detection System

## Goal of the Project

This project is designed to enhance the integrity of electoral processes through the development of an automated system that employs blockchain technology, integrated alert systems, and anomaly detection. Our software guarantees that each vote is accurately counted and verifiable, greatly enhancing transparency and trust in elections by safeguarding the voting process against tampering.

## Significance of the Project

Given the growing concerns about election integrity in contemporary times, having a reliable system that ensures the transparency and correctness of elections is paramount. This project offers a vital solution by employing cutting-edge technology to dynamically detect and alert on potential electoral fraud, thereby addressing major concerns in electoral systems worldwide.

## Installation and Instructions to Use

To get this project up and running, please follow these steps:

1. Begin by cloning the repository from GitHub:
   ```
   git clone https://github.com/yourgithub/voter-fraud-detection.git
   ```
2. Install the necessary Python packages using pip:
   ```
   pip install pandas
   ```
   ```
   pip install sqlite3
   ```
   ```
   pip install hashlib
   ```
   ```
   pip install email.mine.multipart
   ```
   
4. To start the system, run the main script:
   ```
   python main.py
   ```

## Structure of the Code

The codebase is organized into several modules:

- `blockchain.py`: Handles the creation and management of the blockchain.
- `alert_system.py`: Contains functions for sending email alerts in case of detected anomalies.
- `detect_anomalies.py`: Functions for detecting voting anomalies from database records.
- `setup_database.py`: Scripts to set up and populate the database with initial data.

## Functionalities and Test Results

### Functionalities

- **Blockchain Management**: Manages a blockchain to store voting records securely.
- **Anomaly Detection**: Detects and reports voting anomalies based on database records.
- **Alert System**: Sends alerts via email when potential fraud is detected.

### Test Results

Testing was conducted to ensure each component functions as expected. Here are some highlights:

- Blockchain integrity checks passed consistently.
- Anomaly detection accurately identified discrepancies in voting data.
- Email alerts were successfully sent upon anomaly detection.

![image](https://github.com/bypxr/Voter-Anomaly-Detection-System/assets/105805753/85db4b51-f421-4bd2-b439-18dcbaa4b40c)


## Discussion and Conclusions

### Challenges Encountered

- Implementing a real-time anomaly detection system posed challenges due to varying data volumes and the need for immediate response.
- Ensuring the blockchain was both secure and efficient required careful optimization.

### Limitations

- Current anomaly detection algorithms may not cover all types of electoral fraud.
- The system assumes the availability of a reliable and secure internet connection.

### Application of Course Learnings

This project allowed the application of theoretical knowledge from our studies in data structures, algorithms, and software engineering to a real-world problem, demonstrating the practical importance of our academic learnings.
