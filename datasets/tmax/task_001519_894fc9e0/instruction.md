You are an expert data analyst investigating suspicious transaction patterns. 

We have a system that sometimes experiences transaction deadlocks due to circular money transfers occurring in very tight time windows. These circular transfers are suspected to be part of a fraudulent graph structure.

First, you need to understand the data model. The schema for our transaction logs is documented in an image file located at `/app/schema.png`. You must extract the table name and exact column names from this image to construct your data model.

Your task is to write a Python script `/home/user/detector.py` that takes a path to a CSV file as its first command-line argument and prints exactly `SUSPICIOUS` or `OK` to standard output.

The script must:
1. Dynamically load the provided CSV file into a temporary SQLite database using the schema you reverse-engineered from the image.
2. Use parameterized SQL queries with window functions or graph pattern matching (via recursive CTEs or self-joins) to analyze the transactions.
3. Print `SUSPICIOUS` if the CSV contains a circular money transfer loop involving exactly 3 distinct accounts (e.g., A -> B -> C -> A) where:
   - All 3 transactions in the loop occur within a 60-second window (the difference between the maximum and minimum timestamp in the loop is <= 60).
   - The total amount transferred within this specific 3-hop loop exceeds 5000.
4. Print `OK` if no such pattern exists.

We will test your script against two corpora of CSV files:
- An "evil" corpus containing transactions with these fraudulent loops.
- A "clean" corpus containing normal transactions (which may include loops that take longer than 60 seconds, or involve fewer/more accounts, or have lower amounts).

Ensure your script is robust and correctly handles edge cases. You may use standard Python libraries and `sqlite3`.