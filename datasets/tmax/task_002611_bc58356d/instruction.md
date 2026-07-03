I am a researcher trying to organize a complex dataset representing a knowledge graph of researchers and their research interests. The data was dumped into an obfuscated SQLite database and I only have a diagram showing what the tables mean.

Please help me build a small querying service.

Here is what you have:
1. `/app/graph_data.db`: A SQLite database containing tables `t1`, `t2`, `t3`, and `t4`.
2. `/app/schema.png`: An image of my notes that maps these obfuscated table names to their actual graph semantics (Nodes and Edges).

I need you to create a TCP server listening on `127.0.0.1:8080`. 
When a client connects and sends a researcher's name (a string followed by a newline, e.g., "Alice\n"), your server should respond with a comma-separated list of the names of the research concepts that are liked by the people known by that researcher. The output concepts must be alphabetically sorted and followed by a newline.

For example, if Alice knows Bob, and Bob likes "Graph Theory" and "Machine Learning", sending "Alice\n" should return "Graph Theory,Machine Learning\n". 

Constraints:
- You must write the server and querying logic primarily in **Bash** (e.g., using `socat` or `nc` and `sqlite3`).
- You will need to use an OCR tool like `tesseract` to read `/app/schema.png` and understand how the tables join.
- Ensure your server forks or handles multiple sequential requests properly. Keep it running in the background.

To complete the task:
1. Extract the schema mapping from the image.
2. Write your bash scripts (e.g., `server.sh` and `handler.sh`).
3. Start your TCP server in the background on port 8080.