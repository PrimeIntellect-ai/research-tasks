I need your help organizing a messy research dataset and setting up a data access service. Our previous backup script went rogue and created symlink loops, and some of our data archives got corrupted. 

Here is what you need to do:

1. **Symlink Cleanup**: In `/home/user/dataset/`, there are several files, archives, and directories. Some symlinks point to each other, creating infinite loops. Find and delete ONLY the symlinks that result in infinite loops or are broken.

2. **Archive Verification and Extraction**: Under `/home/user/dataset/archives/`, there are several `.zip` files. 
   - Verify their integrity.
   - Move any corrupted/invalid `.zip` files to `/home/user/dataset/corrupt/` (create this directory).
   - Extract the valid `.zip` files into `/home/user/dataset/extracted/`.

3. **Bulk Renaming**: Inside `/home/user/dataset/extracted/`, you will find text files named with the pattern `raw_data_<ID>.dat`. Bulk rename all of these files to `processed_<ID>.txt` (where `<ID>` is the original identifier). Read the contents of each file and append the string "VERIFIED" on a new line at the end of each file.

4. **Video Processing**: We have an experiment video located at `/app/experiment_video.mp4`. Use `ffmpeg` to extract the frame at exactly 00:00:02 (2 seconds in) and save it as `/home/user/dataset/video_frame.jpg`.

5. **Multi-Protocol Data Service**: Write and run a Python script to expose this organized dataset:
   - **HTTP Service**: Listen on `0.0.0.0:8080`. Serve the entire `/home/user/dataset/` directory so that files can be downloaded via standard HTTP GET requests (e.g., `GET /extracted/processed_123.txt`).
   - **TCP Metadata Service**: Listen on `0.0.0.0:8081`. Accept raw TCP connections. When a client sends the exact string `GET_FRAME_SIZE` (followed by a newline `\n`), the server must respond with the exact file size of `/home/user/dataset/video_frame.jpg` in bytes as a string, followed by a newline (`\n`), and then close the connection.

Keep these servers running continuously in the background once set up. Let me know when the servers are running and the dataset is ready!