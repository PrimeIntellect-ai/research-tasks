You are an AI data analyst tasked with building an automated, multi-language CSV filtering pipeline. We receive user feedback in CSV files, but some of the feedback contains spam or malicious prompt injections. You need to build a filter that keeps only the clean feedback.

We have a multi-service architecture running locally to assist you:
1. **Embedding API (Flask, Python)**: Running on `http://127.0.0.1:5000`. You can POST JSON `{"text": "your text here"}` to `/embed` to receive a JSON response `{"embedding": [float, float, ...]}`.
2. **Redis Cache**: Running on `127.0.0.1:6379`. The Embedding API is slow and rate-limited. You MUST cache your embedding results in Redis (using the text as the key and the JSON embedding array as the value) so that repeated texts are processed instantly.
3. **Experiment Tracker (Node.js)**: Running on `http://127.0.0.1:3000`. You can optionally POST metrics to `/track` to keep track of your experiments.

Your goal is to write a bash executable `/home/user/filter.sh` that takes two arguments: an input CSV file and an output CSV file.
Usage: `/home/user/filter.sh <input.csv> <output.csv>`

The script must:
1. Read the input CSV (which has columns `id` and `text`).
2. For each row, get the embedding for `text` (using Redis cache if available, or the Flask API if not).
3. Classify the text as "clean" (0) or "evil" (1).
4. Write ONLY the "clean" rows to `<output.csv>` (including the CSV header).

To help you build your classifier, a labeled training dataset is provided at `/home/user/data/train.csv` (columns: `id,text,label`). You can write a Python or R script to train a lightweight model (e.g., logistic regression on the embeddings) and save it, which your `filter.sh` can then load to make predictions.

Requirements:
- Your solution must start the local services if they aren't running. A startup script is available at `/app/start_services.sh`.
- You must correctly identify and reject 100% of the "evil" rows while preserving 100% of the "clean" rows in our hidden test sets.
- Do not use external APIs; rely only on the local Embedding API.

Good luck!