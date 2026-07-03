You are a backup operator testing a recent restore of an incident response system. The restored files have been dumped into `/app/restored_data/raw/`, but they are disorganized and contain large uncompressed audio logs. 

Your task is to:
1. Reconstruct the directory structure. Create `/home/user/backup_view/` and use standard shell commands (like `find` and `ln`) to create symbolic links for all `.log` and `.wav` files from `/app/restored_data/raw/` into `/home/user/backup_view/`, flattening the hierarchy (all links in one directory).
2. Start a local reverse proxy. Write a simple Python script at `/home/user/proxy.py` that listens on port 8080 and forwards all HTTP requests to a standard Python `http.server` running on port 9000, which serves `/home/user/backup_view/`.
3. Optimize the restored audio. One of the restored files is an incident hotline recording at `/app/restored_data/raw/incidents/audio/alert_001.wav`. Use a Python script with standard libraries (like `wave` and `audioop`) to compress or downsample this file, saving the output to `/home/user/backup_view/alert_001_compressed.wav`. 

The automated test will evaluate your compressed audio file using a Mean Squared Error (MSE) metric against the original file to ensure it hasn't degraded beyond recognition, while also checking that the file size has been reduced by at least 30%.