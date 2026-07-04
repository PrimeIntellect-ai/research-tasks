You are a Machine Learning Engineer preparing a clean training dataset for a Large Language Model. You need to build a robust ETL (Extract, Transform, Load) pipeline using Bash to fetch data from an internal API, deduplicate it using a cache, and filter out low-quality or adversarial text data (e.g., poisoned data injected with hidden characters or anomalous symbol distributions).

Your pipeline involves configuring multiple local services and writing bash scripts for data extraction and classification.

### Phase 1: Service Configuration
There are two services pre-installed in `/app/services/`:
1. A Redis server (used for deduplication).
2. A Flask API (serving the raw text data).

You must configure and start these services:
- Edit the configuration file at `/app/services/flask/.env`. Set `REDIS_HOST=127.0.0.1` and `REDIS_PORT=6379`.
- Start the Redis server in the background using the config provided at `/app/services/redis/redis.conf`.
- Start the Flask API in the background (it binds to port 5000). You can start it by running `python3 /app/services/flask/app.py`.

### Phase 2: ETL Pipeline
Write a Bash script at `/home/user/etl.sh` that performs the following:
- Creates a directory `/home/user/raw_data`.
- Makes 20 GET requests to `http://127.0.0.1:5000/api/data`. Each request returns a JSON object in the format: `{"id": "uuid-string", "text": "document content..."}`.
- For each response, extract the `id` and `text`. (You may use `jq`).
- Save the `text` content to `/home/user/raw_data/<id>.txt`.

### Phase 3: Adversarial Data Filter
Some of the scraped data contains adversarial injections. You must build a classifier in Bash to sanitize the dataset.
Create an executable bash script at `/home/user/filter.sh`. 
- The script will take a single argument: the absolute path to a text file.
- The script must evaluate the text file and **exit with code 0** if the file is "clean", and **exit with code 1** if the file is "evil/poisoned".

**Filtering Rules (Reject / Exit 1 if ANY of these are true):**
1. The file contains any of the following zero-width Unicode characters: `U+200B`, `U+200C`, `U+200D`, or `U+FEFF`.
2. The ratio of punctuation characters (matching the POSIX `[[:punct:]]` class) to alphanumeric characters (matching the POSIX `[[:alnum:]]` class) is strictly greater than `0.5`. (For example, 50 punctuation marks and 90 alphanumeric characters = 50/90 = 0.55 > 0.5 -> Reject). If the file has zero alphanumeric characters but has punctuation, it should also be rejected.

Make sure your `filter.sh` is strictly POSIX compliant or uses standard Bash utilities (e.g., `grep`, `awk`, `wc`, `tr`) to compute these numerical checks.

Ensure both `/home/user/etl.sh` and `/home/user/filter.sh` are executable (`chmod +x`). Note that your `filter.sh` script will be independently verified against a massive hidden corpus of good and bad files.