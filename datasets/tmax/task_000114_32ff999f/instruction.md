You are an engineer investigating a critical issue in our sensor data pipeline. The system consists of an Nginx reverse proxy, a Flask web application, a Redis queue, and a Python background worker. Recently, the background worker has been experiencing severe memory leaks and numerical instability leading to crashes when processing certain sensor payloads. 

Your objectives are two-fold:

1. **Fix the System Composition:**
   Our services are started via `/app/start.sh`. However, the Flask application is currently failing to connect to Redis. You need to inspect `/app/flask_app/config.py` and the Nginx configuration in `/app/nginx/nginx.conf` to ensure all services can communicate. Nginx listens on port 8080 and should route to Flask on port 5000. Flask needs to push to Redis on port 6379. Fix the configuration files so that submitting a payload via `curl -X POST http://localhost:8080/submit -H "Content-Type: application/json" -d '{"sensor": "A", "value": 1.0, "tz": "UTC"}'` successfully queues the job and returns a 200 OK.

2. **Develop a Payload Filter:**
   By analyzing the worker's traceback logs in `/app/logs/worker_crash.log` and the git repository in `/app/worker_repo/` (you may need to use git bisect or recover deleted debug logs to find when the numerical instability was introduced), determine what specific combination of floating-point values and timezone offsets triggers the memory leak (due to an infinite loop in the precision repair logic). 
   
   Once you understand the root cause, write a Python script at `/home/user/detector.py` that acts as a filter.
   - It must take a single file path as a command-line argument: `python3 /home/user/detector.py <path_to_payload.json>`
   - It should read the JSON payload from the file.
   - It must exit with code `0` if the payload is safe (clean) to process.
   - It must exit with code `1` if the payload will trigger the numerical instability/memory leak (evil).

You must ensure that your detector works perfectly, as it will be integrated into the Nginx Lua filter module to drop malicious payloads before they hit the Flask app.