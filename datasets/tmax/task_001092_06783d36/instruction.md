Fix the data ingestion pipeline and implement a dataset validator.

Your final goal is to produce a working end-to-end pipeline where clean datasets are processed successfully and corrupted datasets are rejected.

**Background:**
We are a research lab organizing datasets. Our ingestion pipeline consists of an Nginx reverse proxy, a Flask API, and a Redis queue. Recently, the pipeline has been failing. Researchers are uploading datasets containing implicit NaNs in count-based columns, which causes Pandas to silently upcast integer arrays to floats. This silent conversion breaks our downstream linear algebra tools which require strict integer matrices for discrete Markov chain calculations. Nginx and Redis are misconfigured and failing to communicate with the Flask app.

**Requirements:**

1. **Dependency Installation:**
   Setup your environment. The application requires `pandas`, `numpy`, `flask`, `redis`, and `gunicorn`. 

2. **Pipeline Reconfiguration (Multi-Service Compose):**
   The services are located in `/home/user/app/`. 
   - Ensure Redis is configured to listen on port 6379.
   - Nginx (configured via `/home/user/app/nginx.conf`) should proxy requests from port 8080 to the Flask app on port 5000.
   - Fix `/home/user/app/start_services.sh` so it successfully starts Nginx, Redis, and the Flask API (using gunicorn).

3. **Data Sanitizer (Adversarial Corpus Filter):**
   Write a Python module at `/home/user/app/sanitizer.py` containing a function with the following signature:
   `def validate_dataset(df_path: str) -> bool:`
   - This function must read a CSV file.
   - It must return `True` if the dataset is strictly "clean" (all numeric columns must be strictly convertible to integers without any NaN-induced silent upcasting to floats).
   - It must return `False` if the dataset contains any NaNs in otherwise numeric columns, or if it has already been silently converted to floats where integers are expected.

4. **Integration:**
   Modify `/home/user/app/api.py` (the Flask application). 
   - Route: `POST /upload`
   - It will receive a file upload (`file` in `request.files`).
   - Use your `validate_dataset` function. If it returns `True`, push the dataset's raw text to the Redis list `dataset_queue` and return an HTTP 200 status code. If `False`, return an HTTP 400 status code.

To verify, you can test your `sanitizer.py` against the CSV files provided in `/home/user/data_samples/`.