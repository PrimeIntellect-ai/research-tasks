You are an AI assistant helping a data researcher organize a massive web of interrelated datasets. 

The researcher has been using a proprietary, undocumented compiled tool located at `/app/compute_relevance` to calculate the "relevance score" between pairs of datasets. However, this tool is slow, batch-processing is impossible, and the license is expiring. The researcher needs you to reverse-engineer its behavior and write an efficient Python-based replacement.

Environment Details:
- Database: `/app/datasets.db` (SQLite 3). This contains the underlying dataset metadata and relationship graph. The schema is undocumented.
- Oracle Binary: `/app/compute_relevance`. It is a stripped binary. Usage: `/app/compute_relevance <dataset_id_A> <dataset_id_B>`. It prints a floating-point score to stdout.

Your objective:
1. Reverse-engineer the data model in `/app/datasets.db`.
2. Determine how the oracle binary calculates the relevance score between two dataset IDs based on the graph structure in the database. (Hint: It relates to graph traversal, path aggregation, and properties of the nodes/edges).
3. Write a highly optimized Python script at `/home/user/batch_score.py`.
   - Your script must take two arguments: an input CSV file and an output CSV file.
   - Example usage: `python3 /home/user/batch_score.py input_pairs.csv output_scores.csv`
   - The input CSV will have no header and contain two columns: `dataset_id_A,dataset_id_B`.
   - The output CSV must have no header and contain three columns: `dataset_id_A,dataset_id_B,predicted_score`.
4. Your script must efficiently chain queries or use an in-memory graph (like NetworkX) to process thousands of pairs quickly.

The automated verification system will test your script against a hidden set of 1,000 dataset pairs. Your script's predicted scores will be compared to the actual scores produced by `/app/compute_relevance` using Mean Squared Error (MSE). 

You must achieve an MSE of less than 0.001 to pass.