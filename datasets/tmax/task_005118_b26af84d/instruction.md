You are tasked with analyzing a corrupted security camera feed and deploying a secure, authenticated API to report the findings. A previous version of an alerting service may be running, and you need to perform a staged deployment of your new solution.

There is a video file located at `/app/camera_01.mp4`. 
Perform the following steps:

1. **Video Analysis**: Use `ffmpeg` to analyze `/app/camera_01.mp4` and determine the exact number of completely black frames (blackouts) in the video. 
2. **Permission Management**: The video file contains sensitive information. Modify its permissions and Access Control Lists (ACLs) so that the owning `user` has read-write access, but the group and other permissions are strictly empty (i.e., `---`). 
3. **API Implementation**: Create an HTTP API server (you may use Python, Node.js, or any standard tool) that listens on `127.0.0.1:9042`. 
4. **Endpoint Requirements**: The API must serve a `GET` request at the path `/api/v1/status`.
5. **Authentication**: The endpoint must require an Authorization header exactly matching: `Bearer sec-token-8819`. If this is missing or incorrect, return a 401 Unauthorized status.
6. **Payload Format**: On a successful authenticated request, return a JSON response with the exact count of black frames found in step 1, formatted exactly like this: `{"status": "ok", "black_frames": <COUNT>}`
7. **Deployment**: Write a deployment script at `/home/user/deploy.sh` that automates this: it must gracefully terminate any existing process holding port 9042, apply the secure ACLs to the video file, and launch your API service in the background so it remains running.

Ensure your service is running and actively listening on port 9042 before completing the task.