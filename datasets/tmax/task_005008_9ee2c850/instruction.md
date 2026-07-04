You are the release manager for a distributed microservices platform. Recently, a critical deployment pipeline failed because of peer dependency conflicts and the inclusion of unstable versions. 

We have a legacy monitoring dashboard that records the health of our historical deployments, but the raw data was lost—we only have a video recording of the dashboard's status indicator over time. You need to recover the historical deployment health, cross-reference it with our service manifest, and build a resolution API to ensure safe deployments.

Here are your instructions:

**1. Historical Health Extraction (Video Analysis)**
You have been provided a video file at `/app/deploy_logs.mp4`. This video is exactly 30 seconds long at 1 frame per second (30 frames total). 
* Each frame represents the historical deployment status of a specific service version.
* Frame index `i` (from 0 to 29) corresponds exactly to line `i + 1` in the text file `/home/user/versions.txt`.
* The top-left 10x10 pixel region of each frame contains a solid color block indicating the status. 
* If the average Green RGB channel value in that 10x10 region is strictly greater than the Red channel value, the deployment was a **Success**. Otherwise, it was a **Failure**.
* Extract this data to determine which versions are safe (Success).

**2. Manifest Parsing and Sorting**
You have a file at `/home/user/versions.txt`. Each line contains a service name and a semantic version, separated by a space (e.g., `auth-service 1.2.4`).
Filter out all versions that were marked as a **Failure** in the video analysis. Parse and store the remaining (Success) versions.

**3. Deployment Resolution API**
Create a Python-based backend that provides two services:

**Service A: HTTP API (Port 8080)**
Listen on `127.0.0.1:8080`. Implement the following REST endpoint:
* `GET /deploy/resolve`
* Accepts query parameters: `service` (string) and `target` (a semantic version constraint, specifically exact matches or caret `^` ranges, e.g., `^1.2.0`). 
  *(Note: A caret range like `^1.2.0` allows updates that do not modify the left-most non-zero digit. For example, `^1.2.0` matches `1.2.5` and `1.3.0`, but not `2.0.0`. `^0.2.1` matches `0.2.5` but not `0.3.0`)*.
* The endpoint must find all **Successful** versions for the requested `service`, filter them by the `target` constraint, and return the **highest** valid semantic version.
* The response must be a JSON object: `{"service": "<service_name>", "version": "<resolved_version>"}`. If no version satisfies the constraint, return HTTP 404.

**Service B: TCP Status Monitor (Port 8081)**
Listen on `127.0.0.1:8081` with a raw TCP socket.
* When a client connects and sends the exact string `STATUS\n`, the server must respond with `GREEN_COUNT: <N>\n`, where `<N>` is the total number of **Successful** (Green) versions found across the entire video.
* Close the connection immediately after responding.

You may install any necessary Python libraries (like `fastapi`, `flask`, `uvicorn`, `opencv-python`, `pillow`, etc.) and system packages (like `ffmpeg`). Leave your services running in the background so they can be tested.