You are a Database Administrator and Systems Developer. We have a multi-service architecture running locally that serves social graph analytics. 

Your task is to optimize an analytical query and integrate it into a C-based HTTP service that caches results.

**Environment & Setup:**
In `/app/`, you have a script named `start_services.sh`. Run this script first. It will bring up:
1. A PostgreSQL instance on port 5432 (User: `admin`, DB: `graphdb`, Password: `password`).
2. A Redis instance on port 6379.

**Database Schema:**
The `graphdb` database has two tables:
- `users` (id INT, name VARCHAR, category VARCHAR)
- `follows` (follower_id INT, followee_id INT, engagement_score INT)

**The Objective:**
We need an HTTP API that projects a subset of the social graph for a specific category, but only includes the top connections based on engagement.

1. **Write a C Server:** Complete or create the C program at `/app/api_server.c`. It must listen on `0.0.0.0:8080` and handle HTTP GET requests to the endpoint `/api/graph?category=<category_name>`.
2. **Optimize Query (Window Functions):** The C program must query PostgreSQL for the given category. It needs to project a graph mapping where for every user in the requested category, it retrieves their **top 3 followers** (the ones with the highest `engagement_score`). You MUST use a SQL Window Function (`ROW_NUMBER()` or `RANK()`) to aggregate and filter these top 3 followers efficiently inside the database.
3. **Cross-Representation Mapping (JSON):** The C program must parse the relational output and map it to the following JSON document schema:
   ```json
   {
     "category": "<category_name>",
     "nodes": [
       {
         "user_id": 1,
         "user_name": "Alice",
         "top_followers": [
           { "follower_id": 4, "score": 95 },
           { "follower_id": 7, "score": 82 }
         ]
       }
     ]
   }
   ```
   *(Note: The `nodes` array should be sorted by `user_id` ascending, and `top_followers` sorted by `score` descending).*
4. **Caching:** Before querying PostgreSQL, the C server should check Redis for the key `graph:<category_name>`. If it exists, return the cached JSON string. If it does not exist, query PostgreSQL, build the JSON, store it in Redis under `graph:<category_name>` (with no expiration), and then return it to the client.

**Requirements:**
- Write your code in C. You can use `libpq` for PostgreSQL, `hiredis` for Redis, and standard C string manipulation or a JSON library like `json-c` if available on the system.
- Compile your server to an executable named `/app/api_server`.
- Run the server in the background so it listens on port 8080.
- Return a `200 OK` HTTP status with the JSON body and `Content-Type: application/json`.
- Do not use any external web frameworks; raw sockets or basic HTTP parsing in C is required (you may assume standard well-formed HTTP GET requests for testing).