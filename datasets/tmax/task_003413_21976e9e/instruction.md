You are acting as a data analyst investigating a tracking system that has suffered data corruption. 

We have a corrupted SQLite database and an exported CSV log (`/home/user/raw_events.csv`) of vehicle checkpoint sightings. Due to a corrupted index during the logging process, the CSV contains many "stale" or duplicate ghost rows. 

Fortunately, we have a raw system dashboard screen recording (`/app/dashboard_sync.mp4`). In this video, the screen flashes pure white (rgb 255,255,255) for exactly one frame every time a *valid* transaction is committed to the main server. 

Your tasks:
1. **Video Analysis**: Use `ffmpeg` to analyze `/app/dashboard_sync.mp4`. Identify the exact frame numbers (0-indexed) where the frame is completely white. These frame numbers correspond exactly to the `sync_id` column of the valid rows in `/home/user/raw_events.csv`. 
2. **Data Cleaning**: Filter the CSV to retain only the rows whose `sync_id` matches the white frame numbers. Extract the `vehicle_id`, `checkpoint_id`, and `timestamp` from these valid rows to construct a clean movement graph.
3. **Query Engine**: Write a Go program at `/home/user/path_query.go` and compile it to `/home/user/path_query`. 
   - The program must accept a single command-line argument: `vehicle_id` (a string).
   - It should load your cleaned data and compute the chronological path of the given vehicle through the checkpoints.
   - It must output the path as a comma-separated list of `checkpoint_id`s, ordered by `timestamp` ascending. If the vehicle is not found, output `NOT_FOUND`.
   - Your Go program should use parameterized queries or efficient struct mappings to execute this graph path traversal quickly, as it will be heavily tested.

The final executable must be located at `/home/user/path_query`. The correctness of your program will be evaluated by rigorously fuzzing it with thousands of random vehicle IDs and comparing the output to a reference implementation.