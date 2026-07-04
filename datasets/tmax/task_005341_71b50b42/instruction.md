You are a Database Reliability Engineer (DBRE) tasked with recovering reporting capabilities after an incident that corrupted our primary SQLite backup tracking database. 

We have an SQLite database at `/app/backup_inventory.sqlite`. This database tracks our device backups. However, the index `idx_backups_ts` on the `backups` table was corrupted during a crash. As a result, querying the `backups` table using the timestamp (which uses the corrupted index) returns stale, ghost rows instead of the actual data on disk.

Furthermore, the schema is incomplete. The original developer left a video recording of their terminal during a post-mortem, saved at `/app/incident_record.mp4`. You must extract frames from this video to find two crucial pieces of information:
1. The exact foreign key relationship needed to join the `backups` table to the `devices` table (the column names don't match conventionally).
2. The secret Authorization token required for the new API.

Your task:
1. Write a Python script to expose a new REST API that provides the correct, aggregated backup data.
2. The server must listen on `127.0.0.1:9090` using HTTP.
3. The server must have a single endpoint: `GET /api/v1/latest-backups`
4. This endpoint must require an `Authorization: Bearer <TOKEN>` header, where `<TOKEN>` is the secret found in the video.
5. The endpoint must return a JSON response containing the *true* latest backup status for every device. The JSON should be a list of dictionaries with keys: `device_name`, `latest_status`, and `timestamp`. 
6. To get the correct data, you must either drop the corrupted index, bypass it (e.g., using `NOT INDEXED`), or recreate it, and then perform a cross-query aggregation using the join condition found in the video.
7. Run your Python server in the background so it remains active. Write your server code to `/home/user/api_server.py` and run it.

Note: You can use `ffmpeg` to extract frames from the video. You can use standard Python libraries or install Flask/FastAPI if needed.