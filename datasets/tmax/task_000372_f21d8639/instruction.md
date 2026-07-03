You are tasked with cleaning up and analyzing a set of financial transaction graphs. The previous analyst left a voice memo detailing an issue with the database and the criteria for identifying synthetic (adversarial) transaction data injected into our systems. 

First, listen to the audio briefing located at `/app/briefing.wav`. You can use any tool (e.g., `whisper` or Python libraries) to transcribe it. The audio contains critical instructions regarding a corrupted index in the SQLite database and the exact graph-theoretic rule needed to distinguish clean data from malicious data.

Once you have the parameters from the audio:
1. **Fix the Database:** Connect to the SQLite database at `/app/data/network.db`. The database contains a `transactions` table (`tx_id, sender, receiver, amount, timestamp`). A corrupted index is causing stale rows to be returned. Follow the audio instructions to drop this index.
2. **Perform Window Function Analysis:** After fixing the index, write a query to calculate the cumulative sum of transaction `amount`s per `sender`, ordered by `timestamp`. Save the results (only `sender`, `timestamp`, and the `cumulative_amount`) as a CSV file to `/home/user/cumulative_report.csv`.
3. **Build the Adversarial Classifier:** Write a Python script at `/home/user/classifier.py`. This script must take a single command-line argument: the path to a CSV file representing a transaction subgraph (columns: `source,target,amount`). 
   - The script must calculate the graph metrics specified in the audio briefing.
   - If the graph meets the adversarial criteria, the script must print exactly `EVIL` to standard output.
   - Otherwise, it must print exactly `CLEAN`.
   - Your classifier will be tested against a hidden suite of clean and evil CSV files. It must correctly classify all of them.

Ensure your code handles potential edge cases in the CSVs (like headers and empty lines) and relies on standard graph libraries (like `networkx`) which you may install if needed.