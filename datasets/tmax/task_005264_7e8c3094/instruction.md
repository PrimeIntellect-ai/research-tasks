You are tasked with setting up a data ingestion and cleaning pipeline for machine learning datasets, as well as implementing the core text normalization logic in C.

The pipeline consists of multiple cooperating services:
1. **Nginx**: Acts as a reverse proxy, listening on port 8080 and routing traffic to a Flask API.
2. **Flask API**: An existing app at `/app/api.py` that listens on port 5000. It receives raw text payloads via `POST /ingest` and pushes them into a Redis list named `raw_data`.
3. **Redis**: Runs locally on the standard port (6379) to buffer data.
4. **Data Cleaner Worker**: A script you must write at `/app/worker.sh` that continuously pops items from the `raw_data` Redis list, processes them using your C program, and pushes the output to a Redis list named `clean_data`.

### Part 1: Service Configuration
- Configure Nginx so that requests to `http://localhost:8080/ingest` are forwarded to the Flask app. The Nginx configuration file should be placed at `/app/nginx.conf`.
- Write the `/app/worker.sh` script to bridge Redis and your C program. It should use `redis-cli` to `BLPOP raw_data 0`, pass the raw string to the standard input of your C program `/app/cleaner`, and then use `redis-cli` to `RPUSH clean_data "<output>"`. 
- Ensure all services (Redis, Nginx, Flask, and your worker) can be started together. Create a script `/app/start_all.sh` that launches Redis, Nginx (using `/app/nginx.conf`), Flask (using `python3 /app/api.py`), and `/app/worker.sh` in the background.

### Part 2: Core Data Cleaner in C
You must implement the dataset tokenization and cleaning logic in C. The program will be strictly verified against a reference implementation via a random fuzzer. 
- **Source code**: `/app/cleaner.c`
- **Executable**: `/app/cleaner` (compile with `gcc -O2 /app/cleaner.c -o /app/cleaner`)

**Logic Requirements for `/app/cleaner`:**
1. Read all available text from standard input until EOF.
2. Convert all ASCII alphabetic characters to lowercase.
3. Replace any continuous sequence of non-alphanumeric characters (excluding spaces, tabs, and newlines) with a single underscore `_`.
4. Replace all whitespace characters (spaces, tabs, newlines) with a single space ` `.
5. Strip any leading or trailing spaces from the entire processed string.
6. Print the resulting normalized string.
7. Tokenize the normalized string by spaces. For each token, calculate the number of vowels (`a, e, i, o, u`) and the number of consonants (any other alphabetic character).
8. Compute the sum of the products of (vowel_count * consonant_count) across all tokens.
9. Print a newline, followed by `STATS: ` and the integer sum calculated in step 8.

Example:
Input: `Hello, World!!! 123`
Normalized string: `hello_ world_ 123`
Tokens: `hello_`, `world_`, `123`
- `hello_`: 2 vowels (e,o), 3 consonants (h,l,l) -> 2*3 = 6
- `world_`: 1 vowel (o), 4 consonants (w,r,l,d) -> 1*4 = 4
- `123`: 0 vowels, 0 consonants -> 0*0 = 0
Total sum: 10
Output:
```
hello_ world_ 123
STATS: 10
```

Compile your C code and ensure the pipeline runs correctly. The automated verifier will test your pipeline end-to-end and fuzz your `/app/cleaner` binary for bit-exact equivalence with our oracle.