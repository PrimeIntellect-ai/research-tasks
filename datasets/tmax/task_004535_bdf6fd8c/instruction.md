You are assisting a developer in organizing legacy project assets and exposing them via a simple Go service.

Your task has three parts:

1. **Video Frame Extraction & Atomic Write**
   We have a project demo video located at `/app/demo.mp4`. Extract exactly one frame at the `00:00:03` mark as a JPEG image. To ensure no partial reads occur if another process watches the directory, you must write the frame to a temporary file first, and then atomically move (rename) it to `/home/user/assets/thumb_raw.jpg`.

2. **Nested Archive Extraction & Symlinking**
   There is a nested archive at `/app/bundle.tar.gz`. It contains a zipped file, which in turn contains a file named `project_data.txt`. 
   - Extract `project_data.txt` and place it in `/home/user/assets/`.
   - Create a symbolic link at `/home/user/public/thumb.jpg` that points to `/home/user/assets/thumb_raw.jpg`.
   (Ensure all necessary directories are created).

3. **Go HTTP Server**
   Write a Go program at `/home/user/server.go` and run it in the background. The server must listen on `0.0.0.0:8080` and implement the following HTTP GET endpoints:
   - `GET /data`: Serves the exact text contents of `/home/user/assets/project_data.txt`.
   - `GET /video-thumb`: Serves the image file by resolving and serving the symlink `/home/user/public/thumb.jpg`.

Leave the server running in the background when you complete your task.