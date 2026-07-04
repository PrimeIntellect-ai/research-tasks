You are an ML Engineer tasked with preparing a high-quality tokenized dataset for training. You have a microservice architecture provided in `/home/user/app` that processes raw text. 

The architecture consists of three components:
1. **Redis**: Used as a message queue.
2. **Node.js Data Ingestor** (`/home/user/app/data_ingest`): Reads raw documents from `/home/user/app/raw_texts.json` and pushes them to a Redis list called `doc_queue`.
3. **Python Scoring Service** (`/home/user/app/scoring_service`): A FastAPI application that tokenizes text, calculates a quality score for the document, and provides an endpoint to process documents.

Your tasks:
1. **Fix and Start the Services**: 
   - Start a local Redis server on the default port.
   - The Node.js ingestor has a misconfigured Redis connection URL in its `index.js`. Fix it and run the ingestor to populate the queue.
   - The Python scoring service in `main.py` is configured to run on port 3000, which conflicts. Change it to run on port 8000 and start it.
2. **Dataset Generation and Bootstrapping**:
   - Write a script (in Python or Node.js) that pulls all available documents by continuously calling the Python Scoring Service's endpoint `GET http://localhost:8000/process_next`. This endpoint pops a document from Redis, tokenizes it, and returns `{"id": doc_id, "tokens": [...], "score": float}`.
   - Collect all processed documents.
   - From this collected pool, use bootstrap sampling (sampling with replacement) to create a final dataset of exactly **1000** samples.
   - **Requirement**: Your sampling strategy must ensure that the mean `score` of the 1000 sampled documents is **greater than or equal to 0.80**.
   - Save the final dataset to `/home/user/final_dataset.jsonl`, where each line is a valid JSON object: `{"id": "...", "tokens": [...], "score": ...}`.

Ensure all services are running and your final JSONL file is correctly formatted.