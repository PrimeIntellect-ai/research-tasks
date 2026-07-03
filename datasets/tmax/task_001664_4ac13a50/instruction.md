You are tasked with replacing a bottleneck in a streaming data pipeline. A data producer publishes high-frequency 3D sensor coordinates to a Redis list, and we need a high-performance Go service to clean, normalize, and load this data into a PostgreSQL database.

Currently, there is a slow Python prototype at `/app/slow_processor.py`. You need to implement its exact logic in Go to achieve massive performance gains, and properly wire up the infrastructure.

**Infrastructure Requirements:**
1. Under `/app/`, there is a `docker-compose.yml` containing a Redis and a PostgreSQL service. You must start these services.
2. The PostgreSQL database requires a table to be created before processing. 
   Database credentials: host=localhost, port=5432, user=postgres, password=secret, dbname=sensors.
   Create this table: `CREATE TABLE cleaned_metrics (id INT PRIMARY KEY, z_score FLOAT);`
3. A producer script `/app/producer.py` will push 200,000 JSON messages to the Redis list `sensor:raw`.

**Go Service Requirements:**
Create a Go program at `/home/user/processor.go` that does the following:
1. Connects to Redis and continuously pops JSON messages from `sensor:raw` (Format: `{"id": int, "x": float, "y": float, "z": float}`).
2. **Distance Filter (Deduplication):** Compute the Euclidean distance between the `(x, y, z)` of the current point and the previous *raw* point. If this distance is strictly less than `0.01`, drop the current point (it is a duplicate/stuck sensor). The very first point is never dropped for distance.
3. **Rolling Statistics & Normalization:** For points that pass the distance filter, calculate their distance from the origin `(0, 0, 0)`.
   - Maintain a rolling window of the last `50` *valid* (non-dropped) distances from the origin.
   - If fewer than 50 valid points have been collected, accept the point but do NOT write it to the database (skip until the window is full).
   - Once the window has 50 points, compute the mean and population standard deviation of these 50 distances.
   - Compute the standard score (z-score) of the *current* point's distance: `z_score = (distance_from_origin - rolling_mean) / rolling_std`.
4. **Anomaly Filter:** If the calculated `z_score` is greater than `3.0` or less than `-3.0`, drop the point (do not add it to the rolling window for future calculations, and do not insert it).
5. **Load:** For points that pass all filters (and where the window had 50 points), insert their `id` and `z_score` into the `cleaned_metrics` PostgreSQL table. Add the accepted point's distance from origin to the rolling window.

**Execution and Benchmarking:**
Your Go program must be compiled to `/home/user/processor`.
When evaluated, the verifier will:
1. Clear Redis and Postgres.
2. Run `/app/producer.py`.
3. Start `/home/user/processor` and measure the time it takes to process all messages and empty the `sensor:raw` queue.

Your solution must complete the processing in **under 2.5 seconds** (the Python script takes >20s) and produce the exact same final database state as the reference implementation.

You may use third-party Go packages (e.g., `github.com/go-redis/redis/v8`, `github.com/lib/pq`) by running `go mod init processor` and `go get ...` in `/home/user/`.