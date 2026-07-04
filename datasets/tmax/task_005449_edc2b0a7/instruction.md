You are tasked with fixing a broken Nginx reverse proxy configuration and implementing a security classifier to protect the backend.

1. **Fix the Nginx 502 Bad Gateway**
There is a local Nginx configuration file at `/home/user/nginx/nginx.conf`. When Nginx is started using this config, requests to `http://127.0.0.1:9090/` return a 502 Bad Gateway error. A simple backend service is running on `127.0.0.1:8080`. Fix the `nginx.conf` file so that requests are correctly proxied to the backend, returning a 200 OK. Ensure Nginx is running with your fixed config before finishing. Nginx must be run as the `user` without `sudo`.

2. **Create a Request Classifier**
The backend has been crashing due to malicious requests. The previous administrator left a voice memo detailing the exact criteria for identifying these malicious requests. The audio file is located at `/app/admin_note.wav`.

You must write a Python script at `/home/user/classifier.py` that takes a single command-line argument: the path to a text file containing a raw HTTP request (headers and body).
The script must evaluate the request based on the criteria in the audio recording.
- If the request is **malicious** (evil), the script must exit with status code `1`.
- If the request is **clean**, the script must exit with status code `0`.

To help you test your logic, you have been provided with two corpora of raw HTTP request files:
- `/app/corpus/clean/`: Contains known safe requests.
- `/app/corpus/evil/`: Contains known malicious requests.

Your solution will be evaluated against a hidden test set of similar requests. You must achieve 100% accuracy on both the clean and evil evaluation corpora.

**Instructions:**
- Fix the Nginx configuration and leave the Nginx process running.
- Transcribe or listen to `/app/admin_note.wav` to understand the security rules.
- Write your classifier in Python at `/home/user/classifier.py`.
- Ensure your script handles standard raw HTTP request parsing correctly.