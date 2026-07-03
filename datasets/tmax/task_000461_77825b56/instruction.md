You are a data analyst tasked with building a lightweight recommendation service using Bash. 

We have a dataset of item feature vectors in a CSV file located at `/home/user/items.csv`. The format is `item_id,feature1,feature2,feature3`. 
You are provided with a compiled, stripped binary at `/app/score_calc`. This binary takes two comma-separated feature vectors as command-line arguments and outputs a similarity score (e.g., `/app/score_calc "1.0,2.0,3.0" "0.5,1.5,2.5"`).

Your task is to:
1. Write a Bash script `/home/user/recommend.sh` that processes `/home/user/items.csv`.
2. For a given target `item_id`, use the `/app/score_calc` binary to compute the similarity score against all other items.
3. Perform a simple bootstrap sampling (10 iterations) on the resulting scores to estimate the lower bound of a 95% confidence interval for the mean similarity score of the top 3 items. However, to keep it simple for the service, just return the top 3 most similar `item_id`s in descending order of their raw similarity score.
4. Start a TCP server listening on `127.0.0.1:8888` using `nc` (or `socat`).
5. When the server receives an `item_id` string followed by a newline, it should respond with the top 3 recommended `item_id`s, comma-separated, followed by a newline. The server should remain open to handle multiple sequential requests (you can use a `while read` loop with `nc -l -p 8888 -k` or similar).

Ensure your service is running in the background and listening on port 8888 when you complete your task.