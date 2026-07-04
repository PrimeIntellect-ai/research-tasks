I am a systems researcher organizing a dataset of server log fragments. I want to build a lightweight, Bash-only predictive service that classifies new log entries as malicious or benign using a Naive Bayes approach.

I have a stripped binary at `/app/log_oracle` which is an older, compiled C tool I used to use for labeling. It takes a single string argument and outputs either "MALICIOUS" or "BENIGN". 

Here is what I need you to do:

1. **Environment & Data Setup**:
   - Install `socat` or `netcat` using the package manager.
   - You will find a dataset of raw log snippets at `/home/user/dataset/logs.txt`. Each line is a separate log entry containing alphanumeric words.

2. **Model Training (Bash-based)**:
   - Create a script `/home/user/train.sh`. This script should use the `/app/log_oracle` binary to label every line in `/home/user/dataset/logs.txt`.
   - Calculate the prior probabilities of MALICIOUS and BENIGN.
   - Calculate the likelihood of each unique word appearing given each class (use Laplace smoothing with alpha=1 to avoid zero probabilities). 
   - Save these probabilities in a "model" file at `/home/user/model.txt` in a format of your choosing.

3. **Inference Service**:
   - Create a script `/home/user/serve.sh` that launches a TCP service listening on `127.0.0.1:9090`.
   - The service should accept incoming connections. The expected request format from a client is a single line:
     `AUTH:<token>|LOG:<log_snippet>`
   - If the token is NOT exactly `sysresearch_2024`, the service should immediately respond with `ERROR: UNAUTHORIZED\n` and close the connection.
   - If the token is correct, the service should parse the log snippet, use the model data in `/home/user/model.txt` to calculate the proportional Naive Bayes probability that the log is MALICIOUS, and respond with:
     `RESULT:<probability>\n`
     (Format the probability as a float between 0 and 1, rounded to 4 decimal places). 

Start the service in the background so that it is running when you complete the task. Do not use Python or any other scripting languages for the server or training script—you must build this entirely using Bash, `awk`, `bc`, `jq`, and standard coreutils.