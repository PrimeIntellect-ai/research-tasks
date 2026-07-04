You are an AI assistant helping a researcher organize their dataset catalog. We need to build an internal search service that retrieves dataset recommendations based on text queries, incorporating both semantic relevance and usage statistics.

We have two sources of data:
1. A PostgreSQL database running locally on port 5432 containing dataset metadata. The database `catalog` has a table `datasets` with columns: `id` (integer), `name` (text), and `description` (text).
2. A CSV file located at `/app/stats.csv` containing usage statistics. It has columns: `dataset_id` (integer) and `downloads` (integer).

Your task is to implement and run an HTTP API service (using Python, e.g., Flask or FastAPI) that listens on `127.0.0.1:8000`.

Requirements for the API:
- Endpoint: `GET /search`
- Query parameters: 
  - `q` (string): The search query.
  - `limit` (integer): Maximum number of results to return (default 5).
- Logic:
  1. Fetch all dataset descriptions from the Postgres database.
  2. Compute TF-IDF vectors for the dataset descriptions (you can use `scikit-learn`). Use standard English stop words.
  3. Transform the incoming query `q` using the same TF-IDF vectorizer.
  4. Compute the cosine similarity between the query and all dataset descriptions.
  5. Join the similarity scores with the download statistics from `/app/stats.csv` using the dataset ID.
  6. Calculate a final ranking score for each dataset using the formula: `final_score = similarity * log10(downloads + 1)`.
  7. Return the top `limit` datasets ranked by `final_score` in descending order.
- Response Format:
  ```json
  {
    "results": [
      {
        "id": 1,
        "name": "Dataset Name",
        "final_score": 0.453
      }
    ]
  }
  ```

Setup instructions:
- A script to start and seed the PostgreSQL database is provided at `/app/setup_db.sh`. You must run it to start the database service. It sets up the `catalog` DB with user `postgres` and password `postgres`.
- Write your API code in `/home/user/api.py`.
- Run your API as a background process so that it remains active.
- Write a log file of all incoming queries to `/home/user/search_logs.txt`, appending the query string `q` on a new line for each request.

Start the API on port 8000 and ensure it is fully functional.