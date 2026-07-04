I am a technical writer organizing a massive dump of legacy documentation for our new engineering portal. Our system relies on a few microservices: we have a Redis instance (port 6379) tracking document metadata, and a Flask API (running on port 5000) that accepts documentation parsing metrics. 

Currently, I have a directory `/home/user/docs_raw/` containing 10,000 markdown files. 
Each file contains legacy references in the format `<legacy-ref target="DOC_ID">`. These need to be transformed to our new markdown format: `[DOC_ID](/docs/DOC_ID)`.

I have a basic, naive Python script at `/app/processor.py` that processes these files, updates the text, writes them to `/home/user/docs_processed/`, and sends a POST request to `http://127.0.0.1:5000/report` with the JSON payload `{"filename": "...", "replacements": <int>}`. 

However, the current script processes files sequentially, uses naive file operations, and takes over 45 seconds to run. Our CI pipeline requires this step to complete in **under 3.5 seconds**.

Your task:
1. Rewrite `/app/processor.py` (in Python) to be highly concurrent/optimized.
2. Ensure you use **atomic writes** (write to a temporary file in `/home/user/docs_processed/` and rename it) to prevent partial reads by other services.
3. Successfully transform all 10,000 files and ensure they are written to `/home/user/docs_processed/`.
4. Ensure the Flask service correctly registers the metrics for all 10,000 files.

You can start the backend services by running: `/app/start_services.sh`
You should test your script by running `python /app/processor.py`. Ensure your final script is saved at `/app/processor.py` so the automated test can verify its execution time and output correctness.