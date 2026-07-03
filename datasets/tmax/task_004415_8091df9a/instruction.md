You are a data engineer tasked with building an ETL pipeline that ingests streaming customer support chat logs, filters out malicious payload injections (like prompt injections or corrupted tokens), and stores the clean data via a REST API.

Your objective has three main components: Infrastructure setup, Model building, and ETL pipeline creation.

**1. Infrastructure Setup**
We have a multi-service setup located in `/app/services/` containing:
- A Redis instance (acting as our message queue on port 6379).
- A Flask API (the data sink on port 5000).
- An Nginx reverse proxy (listening on port 8080, meant to route traffic to the Flask API).

Start the services by running `/app/services/start.sh`. However, the Nginx configuration file (`/app/services/nginx.conf`) has a misconfiguration. It is currently routing traffic to the wrong upstream port. You must fix `nginx.conf` so that requests to `http://127.0.0.1:8080/ingest` correctly reach the Flask API. Once fixed, restart the Nginx service or run the start script again so the changes take effect.

**2. Data Modeling & Adversarial Filtering**
You have been provided a training dataset at `/home/user/data/train.csv`. It contains two columns: `text` and `label` (where `label` is either `clean` or `evil`).
- You must perform text tokenization, cross-validation, and hyperparameter tuning to build a machine learning model that perfectly separates the classes. 
- You may use any Python library you prefer (e.g., `scikit-learn`). 
- Write a module at `/home/user/filter.py` containing a function with the exact signature: `def is_clean(text: str) -> bool:`. 
- This function should tokenize the input text, run it through your trained model, and return `True` if the text is clean, and `False` if it is evil. Our automated grading suite will test your `is_clean` function against hidden adversarial corpora.

**3. ETL Integration**
Write a Python script at `/home/user/etl_worker.py` that continuously performs the following:
- Connects to the local Redis instance on port 6379.
- Pops items from the right of the Redis list named `chat_queue` (using blocking operations if the queue is empty).
- Each item is a JSON string: `{"id": <int>, "text": "<string>"}`.
- Passes the `text` field to your `is_clean()` function from `filter.py`.
- If the text is clean, it sends an HTTP POST request to `http://127.0.0.1:8080/ingest` with the JSON payload `{"id": <int>, "text": "<string>"}`.
- If the text is evil, it is silently dropped.

You must leave `/home/user/etl_worker.py` running in the background or be prepared to run it, but your primary deliverable that will be strictly verified is the `filter.py` module and the corrected system configuration.