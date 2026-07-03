You are a Machine Learning Engineer preparing a data extraction pipeline for a recommendation system. You need to glue together some microservices and write a feature extraction script that generates training data vectors.

**System Setup:**
In `/home/user/services/`, there are two Python Flask APIs:
1. `user_service.py` - Runs on port 8081 and serves user embeddings at `/user/<user_id>`.
2. `item_service.py` - Runs on port 8082 and serves item metadata at `/item/<item_id>`.

There is also an Nginx configuration file at `/home/user/nginx.conf`. 

**Step 1: Multi-Service Composition**
1. Modify `/home/user/nginx.conf` so that:
   - It listens on port 8000.
   - Requests to `/user/...` are routed to `127.0.0.1:8081`.
   - Requests to `/item/...` are routed to `127.0.0.1:8082`.
2. Start the services. You can start the Flask apps manually in the background (`python3 user_service.py &`, etc.) and start Nginx using your modified config (`nginx -c /home/user/nginx.conf`). 

**Step 2: Feature Extraction Script**
Write a Python script at `/home/user/feature_extractor.py`. 
- The script must accept a single command-line argument: a JSON string containing a user and item interaction, e.g., `'{"user_id": "u123", "item_id": "i456"}'`.
- It must fetch the user embedding from `http://127.0.0.1:8000/user/<user_id>` which returns JSON like `{"embedding": [0.1, 0.2, 0.3, 0.4, 0.5]}`.
- It must fetch the item metadata from `http://127.0.0.1:8000/item/<item_id>` which returns JSON like `{"category": "electronics", "price": 29.99}`.
- It must construct a 10-dimensional raw feature vector `v`:
  - `v[0:5]`: The 5 floats from the user embedding.
  - `v[5:9]`: A one-hot encoded vector for the item category. The exact vocabulary in alphabetical order is `['book', 'clothing', 'electronics', 'home']`. For example, `book` is `[1, 0, 0, 0]`. If the category is anything else, use `[0, 0, 0, 0]`.
  - `v[9]`: The base-10 logarithm of `(price + 1.0)`.
- Apply Dimensionality Reduction: Read the projection matrix from `/home/user/projection_matrix.csv` (which has 10 rows and 3 columns, no header). Multiply the 1x10 vector `v` by this 10x3 matrix to produce a 1x3 vector.
- Print the resulting 3 floats to standard output, separated by spaces, formatted to exactly 4 decimal places (e.g., `0.1234 -1.2345 0.0000`). Do not print anything else.

Make sure your script is robust and deterministic. Automated tests will fuzz your script with thousands of random inputs and compare its output strictly against a reference implementation.