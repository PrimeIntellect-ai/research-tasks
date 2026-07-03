You are a data engineer tasked with building a real-time ETL pipeline for a mathematical research aggregator. You need to filter incoming mathematical paper submissions. We have been receiving adversarial/spam submissions (e.g., gibberish equations, out-of-domain text) that must be rejected before ingestion.

Our system relies on two microservices:
1. **Embedding Service (`model_api`)**: Performs dimensionality reduction on paper abstracts, converting text into a 10-dimensional mathematical vector.
2. **Vector DB (`vector_db`)**: Performs a similarity search, returning the Euclidean distance from the input vector to our trusted centroid of valid mathematical papers.

**Part 1: Service Configuration (Multi-Service Compose)**
The microservices are located in `/app/`. However, they are currently misconfigured and fail to communicate. 
1. Review `/app/config.env`. The Embedding Service must output 10 dimensions, but the configuration might be mismatched. 
2. The Vector DB is listening on the wrong port. Update `/app/config.env` so that `model_api` uses port 8001 and `vector_db` uses port 8002.
3. Start the services by running `/app/start.sh`. Ensure both services are running and healthy.

**Part 2: The ETL Filter (Adversarial Corpus)**
You must write a Bash script at `/home/user/filter.sh` that acts as the gatekeeper for our ETL pipeline. 
The script must take exactly one argument: the path to a JSON file containing a paper submission. 

The JSON format is:
`{"id": "...", "abstract": "...", "metadata": {"source": "..."}}`

Your `/home/user/filter.sh` script must perform the following pipeline using `curl` and `jq`:
1. Extract the `abstract` text from the JSON file.
2. POST the abstract to the Embedding Service: `http://127.0.0.1:8001/embed` with JSON payload `{"text": "<abstract>"}`. It returns `{"vector": [float, float, ...]}`.
3. POST the resulting vector to the Vector DB: `http://127.0.0.1:8002/distance` with JSON payload `{"vector": [float, float, ...]}`. It returns `{"distance": float}`.
4. Apply the rejection rules. Your script must EXIT with code `1` (Reject) if ANY of the following are true:
   - The similarity `distance` is greater than `5.0` (indicating it is out-of-domain or adversarial).
   - The `metadata.source` is EXACTLY `"predatory_journal_x"`.
   - The Embedding Service returns an error or a vector with length other than 10.
5. If the submission passes all checks, your script must EXIT with code `0` (Accept).

There are two datasets for you to test against:
- `/home/user/corpora/clean/` (Valid papers that MUST exit 0)
- `/home/user/corpora/evil/` (Spam/Adversarial papers that MUST exit 1)

Ensure your script is executable (`chmod +x /home/user/filter.sh`) and uses pure Bash and standard CLI utilities (`jq`, `curl`, `awk`, etc.). Do not write the filter in Python.