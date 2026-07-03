You are tasked with reviving and migrating a legacy mathematical video analysis pipeline. The previous developer abandoned this project during a Python 2 to Python 3 migration, leaving a broken environment, a malfunctioning C extension, and an unfinished validation server. 

Your objective consists of three parts:

**Part 1: Package Migration (Python/C)**
In `/app/legacy_tracker/`, there is a Python package containing a C extension (`fastmath.c`) and a `setup.py`. 
1. Fix the `setup.py` and C extension to compile and install successfully under Python 3. The C extension calculates Euclidean distances and currently uses deprecated Python 2 `Py_InitModule` syntax.
2. Install the package globally or in a virtual environment.
3. Use `ffmpeg` to extract all frames from the video file located at `/app/experiment.mp4` into a temporary directory.
4. The package provides a script `/app/legacy_tracker/extract.py`. Run this script, passing the directory of extracted frames as an argument. It will use the `fastmath` C extension to analyze the frames and produce a file at `/home/user/video_stats.json`.

**Part 2: The Validation Server (Go)**
The system ingests JSON trajectory payloads from remote sensors. We need a robust ingestion server written in Go.
Create a Go HTTP server at `/home/user/server.go` and run it on port `8080`.
The server must expose a `POST /validate` endpoint that accepts JSON payloads of the form:
`{"id": "string", "points": [{"x": float, "y": float}, ...]}`

Requirements for the server:
1. **Validation (Math)**: The server must calculate the Euclidean distance between consecutive points in the trajectory. If the distance between *any* two consecutive points exceeds `50.0` units, the trajectory is considered physically impossible (an anomaly). 
2. **Response**: If the trajectory is valid (no jumps > 50.0), return HTTP 200 OK. If it is invalid (contains a jump > 50.0), return HTTP 400 Bad Request.
3. **Concurrency & Rate Limiting**: The server must use Go concurrency patterns to handle incoming requests efficiently, but it must enforce a strict rate limit of exactly 10 requests per second globally. Requests exceeding this limit should return HTTP 429 Too Many Requests.

**Part 3: Adversarial Corpus Filtering**
We have provided a dataset of trajectory JSON files in `/app/corpus/`. 
There are two subdirectories:
- `/app/corpus/clean/` contains valid mathematical trajectories.
- `/app/corpus/evil/` contains adversarial, noisy trajectories that violate the velocity threshold.

Once your server is running, you must ensure that if a client POSTs the files from these directories, your server successfully returns `200 OK` for all files in the `clean` directory, and `400 Bad Request` for all files in the `evil` directory. 

Leave your Go server running in the background on port `8080` when you consider the task complete. Make sure `/home/user/video_stats.json` has been successfully generated.