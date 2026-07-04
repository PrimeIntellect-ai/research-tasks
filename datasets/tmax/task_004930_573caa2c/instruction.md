You are a data analyst investigating a financial network. Your manager left you a voicemail with specific instructions, but you only have the audio file and some raw data exports. 

Here is what you need to do:
1. **Transcribe the Voicemail**: Listen to (transcribe) the audio file located at `/app/voicemail.wav` to understand the exact filtering criteria and the graph metric you need to calculate. You may install any Python transcription library (e.g., `openai-whisper`) to extract the text.
2. **Data Ingestion & Indexing**: You have a large dataset of transactions at `/home/user/data/transactions.csv` (columns: `tx_id`, `sender_id`, `receiver_id`, `amount`, `timestamp`, `tx_type`). Start a local MongoDB instance. Write a Python script to ingest this CSV into a MongoDB database called `fin_network` in a collection called `transactions`. Design and apply an optimal index strategy to support fast queries on `tx_type`, `amount`, and `timestamp`.
3. **NoSQL Aggregation & Windowing**: Based on the criteria in the voicemail, write a MongoDB aggregation pipeline (in Python) to filter the transactions and calculate the total aggregated amount sent between any two unique pairs of users. 
4. **Graph Projection**: Materialize this aggregated data into a directed graph using Python (e.g., `networkx`), where nodes are users and directed edges are the aggregated transactions (with the aggregated amount as the edge weight).
5. **Metric Calculation**: Calculate the specific network centrality metric requested in the voicemail for all nodes. 
6. **Output**: Save the final node metrics as a JSON file at `/home/user/final_metrics.json` in the format `{"node_id": metric_value, ...}`. 

Your final solution must be automated in a script named `/home/user/process_network.py` that executes the full pipeline from data loading to JSON generation. An automated test will evaluate the numerical accuracy of your calculated metrics.