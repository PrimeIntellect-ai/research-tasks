You are a log analyst investigating suspicious user activity on a web server. You have been provided with a raw log file at `/home/user/raw_logs.csv`. Your objective is to process these logs, compute mathematical similarity to a known "normal" baseline, and generate an anomaly report.

Here are the specific steps you must follow:

1. **Database Bulk Import**:
   Import the contents of `/home/user/raw_logs.csv` into a new SQLite database located at `/home/user/logs.db`. The table should be named `access_logs`.

2. **Feature Extraction**:
   Using Python, query the database to extract a behavior feature vector for each unique `user_id`. The vector must consist of three numerical features, in this exact order:
   - `total_requests`: The count of log entries for the user.
   - `unique_ips`: The count of distinct `source_ip` addresses the user connected from.
   - `avg_bytes`: The average (mean) `bytes_sent` by the user across all their requests.

3. **Similarity Computation**:
   A normal user baseline vector is defined as `[50, 1, 2500]` (representing 50 requests, 1 unique IP, and 2500 avg bytes). 
   For each user, compute the **Cosine Similarity** between their feature vector and the baseline vector.

4. **Database Bulk Export**:
   Identify the top 5 most anomalous users (those with the *lowest* cosine similarity scores). Export a CSV file to `/home/user/top_anomalies.csv` containing the columns: `user_id`, `total_requests`, `unique_ips`, `avg_bytes`, and `similarity_score` (rounded to 4 decimal places). Sort the rows in ascending order of similarity score.

5. **Template-based Text Generation**:
   Use the `Jinja2` Python library to generate an HTML report located at `/home/user/anomaly_report.html`. The template must output an HTML list (`<ul>`) where each list item (`<li>`) is formatted exactly as follows for the top 5 anomalous users:
   `<li>User {user_id} with score {similarity_score}</li>`
   
Ensure all scripts and outputs are saved in `/home/user`.