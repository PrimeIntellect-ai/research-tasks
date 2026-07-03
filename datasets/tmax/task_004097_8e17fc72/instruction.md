You are acting as a DevSecOps engineer to enforce policy as code and secure a multi-service application.

There are two parts to this task.

### Part 1: Credential Leak Detector (Adversarial Classifier)
We have a policy that no secrets should be passed via command-line arguments, as they can be read by any local user via `/proc/PID/cmdline`.
Write a Python script at `/home/user/detector.py` that takes two arguments: an input JSONL file and an output JSONL file.
Invocation: `python3 /home/user/detector.py <input.jsonl> <output.jsonl>`

The input JSONL file will contain objects with a `cmdline` property, which is a list of strings representing the arguments.
Example: `{"id": "1", "cmdline": ["python3", "worker.py", "--secret=foo123"]}`

Your script must evaluate each command line and output a JSONL file with the same `id` and a boolean `leak` property.
Example output: `{"id": "1", "leak": true}`

A command line is considered to leak a secret (i.e., `leak` is true) IF AND ONLY IF it contains an argument meeting AT LEAST ONE of these conditions:
1. It matches the regex pattern for an AWS Access Key ID: exactly starts with `AKIA` followed by 16 uppercase alphanumeric characters.
2. It starts with `--password=` or `--secret=`.
3. An argument is exactly `-p` or `-s`, AND the immediately following argument exists, does not start with `-`, and is not empty.

### Part 2: Multi-Service Configuration and Patching
In `/home/user/app`, there is a multi-service application consisting of an Nginx reverse proxy and a Flask API. 
Currently, the application violates our security policies.
1. The Flask app (`/home/user/app/api.py`) receives a secret via a POST request and passes it to a worker script (`/home/user/app/worker.py`) via the command line (`subprocess.run(...)`).
2. The Flask app binds to `0.0.0.0:5000`, exposing it directly and bypassing Nginx (which listens on `8080`).

You must fix these issues:
- Modify `api.py` and `worker.py` so that the API passes the secret to the worker via an environment variable named `SECRET_TOKEN` instead of command-line arguments. The worker should read `os.environ.get('SECRET_TOKEN')`. Ensure the worker still returns the expected output.
- Modify `api.py` so that Flask only binds to `127.0.0.1` on port 5000, preventing direct external access. Ensure `nginx.conf` properly routes traffic to `127.0.0.1:5000`.

To verify your setup works locally, you can start the services using `bash /home/user/app/start.sh` and test with `curl -X POST -H "Content-Type: application/json" -d '{"secret":"test1234"}' http://127.0.0.1:8080/process`.