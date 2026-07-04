You are a data scientist tasked with cleaning a messy dataset derived from a traffic camera feed. 

You have been provided with two input files:
1. `/app/traffic_feed.mp4`: A 1-minute dashcam video segment. The camera occasionally freezes, producing many duplicated frames.
2. `/app/raw_telemetry.csv`: A large CSV file containing metadata for various frames (including frames not in this video segment). The columns are `frame_md5, location_name, vehicle_count`. 

However, the dataset has several issues:
- The video contains exact duplicate frames due to camera stuttering.
- The `raw_telemetry.csv` file was compiled from different legacy systems, and the `location_name` column suffers from mixed character encodings. While some rows are valid UTF-8, many are encoded in Windows-1252 (CP-1252) which currently appear corrupted when read as standard UTF-8.

Your objective is to write a Go program (and any necessary bash scripts) to build an ETL pipeline that does the following:

1. **Extract and Deduplicate**: Extract frames from `/app/traffic_feed.mp4` at exactly 1 frame per second (fps) as JPEG images. Perform hash-based deduplication (using MD5) to identify the set of *unique* frames present in the video.
2. **Filter**: Read `/app/raw_telemetry.csv` and filter it down so that it *only* contains rows corresponding to the unique frames you extracted from the video.
3. **Cleanse Encodings**: For the filtered rows, fix the character encoding of the `location_name` column. Any invalid UTF-8 sequences should be interpreted as Windows-1252 and properly converted to standard UTF-8. 
4. **Bulk Load**: Bulk import the filtered and cleansed records into a new SQLite database located at `/home/user/cleaned_telemetry.db`.
   - The database must contain a table named `telemetry`.
   - The table schema must be: `frame_md5 TEXT PRIMARY KEY, location_name TEXT, vehicle_count INTEGER`.

Ensure your Go program is efficient. You are expected to use standard CLI tools (like `ffmpeg` for extraction) and write the processing logic in Go. 

Save your Go source code as `/home/user/pipeline.go` and run it to produce the final database.