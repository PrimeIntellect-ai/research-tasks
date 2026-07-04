You are tasked with debugging and fixing a broken audio-processing web stack. 

The stack consists of an Nginx reverse proxy and a Python Flask backend application. Nginx is configured locally in `/home/user/nginx/nginx.conf` and listens on port 8080. The backend code is located in `/home/user/app/main.py` and is meant to be run via a WSGI server like `gunicorn`.

Currently, the system is failing:
1. When Nginx is started, making requests to `http://127.0.0.1:8080` results in a 502 Bad Gateway error. This is due to a mismatch between where Nginx expects the upstream backend to be and how the backend is actually running.
2. The Flask backend exposes a `/process` endpoint. It expects a POST request containing an audio file uploaded as multipart/form-data (with the field name `file`). It is supposed to read the WAV file, convert the audio samples to a normalized float32 array (ranging from -1.0 to 1.0), and compute the Mean Absolute Amplitude (the average of the absolute values of the samples).
3. The backend logic in `/home/user/app/main.py` contains a mathematical bug in how it normalizes or calculates this value.

Your objectives:
1. Fix the Nginx configuration (`/home/user/nginx/nginx.conf`) or the Gunicorn launch parameters so that Nginx successfully proxies requests to the Python backend without returning a 502 error. Nginx should run without root privileges (e.g., `nginx -c /home/user/nginx/nginx.conf -g 'pid /home/user/nginx/nginx.pid; daemon off;'`).
2. Fix the bug in `/home/user/app/main.py` so that it correctly computes the Mean Absolute Amplitude of the uploaded audio file.
3. Write a health-check/test script at `/home/user/check.py`. This Python script must send a POST request with the audio file located at `/app/test_audio.wav` to `http://127.0.0.1:8080/process`. 
4. `/home/user/check.py` must print ONLY the computed floating-point result to standard output (no extra text).

Ensure both Nginx and your Python backend are running in the background before running your script. We will evaluate your success by executing `python3 /home/user/check.py` and checking if the numerical output matches the expected mathematical property of the audio file.