You are managing a large-scale server infrastructure. The configuration management system logs every configuration item for every server as a continuous stream in a "long" format CSV file. We need to analyze these snapshots to find configuration drift and group similarly configured servers.

Your task is to write a C++ program that streams through a large configuration log, reshapes the data for a specific timestamp, and identifies which server is most similar to a target server based on their configuration profiles.

**Input Data:**
There is a CSV file located at `/home/user/config_stream.csv` (no header).
Format: `Timestamp,ServerID,ConfigKey,ConfigValue`

**Requirements:**
1. Write a C++ program named `/home/user/analyze_config.cpp` and compile it to `/home/user/analyze_config`.
2. **Streaming & Filtering:** The CSV file can be very large. Your program must read the file sequentially. Only process and keep in memory the rows where `Timestamp` is exactly `1700000000`.
3. **Reshaping:** For the filtered rows, reshape the data in memory from its "long" format into a "wide" representation for each server (e.g., mapping each `ServerID` to a set of `ConfigKey=ConfigValue` strings).
4. **Similarity Computation:** Compute the Jaccard Similarity between `server_001` and every other server present at timestamp `1700000000`. 
   - A configuration item is defined as the exact matching pair of `ConfigKey` and `ConfigValue`.
   - Jaccard Similarity = (Number of common items) / (Total unique items across both servers).
5. **Output:** Identify the server (excluding `server_001` itself) with the highest Jaccard Similarity to `server_001`. If there is a tie, choose the server with the lexicographically smallest `ServerID`.
6. Write the result to `/home/user/closest_server.txt` in the following exact format:
   `ServerID,SimilarityScore`
   (Output the score rounded to exactly 4 decimal places, e.g., `server_042,0.8667`).

Complete this task by writing, compiling, and running the C++ code.