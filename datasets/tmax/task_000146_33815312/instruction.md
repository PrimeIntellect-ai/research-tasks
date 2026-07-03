You are a monitoring specialist tasked with setting up a new alert webhook receiver on this server. We received the configuration specifications as an image, but the original text document was lost.

Your tasks are:
1. Extract the configuration from `/app/alert_config.png`. The image contains two key pieces of information: the port the webhook should listen on, and the secret authentication token required to access it. (You can use `tesseract` to read the image).
2. Create an idempotent Python script at `/home/user/webhook.py` that runs a basic HTTP server.
3. The server must listen on `127.0.0.1` on the exact port specified in the image.
4. It should only accept `GET` requests to the `/alert` endpoint.
5. It must check for an `Authorization` header in the format `Bearer <TOKEN_FROM_IMAGE>`. If the token is missing or incorrect, return a `401 Unauthorized` status.
6. If the request is authorized, the server must:
   - Idempotently ensure the directory `/home/user/alert_logs` exists.
   - Enforce strict ACL/permissions on `/home/user/alert_logs` so that ONLY the owner has any permissions (equivalent to `chmod 700`).
   - Append a line `Alert received` to `/home/user/alert_logs/alerts.txt`.
   - Respond with a `200 OK` status and the plain text body `Alert Logged`.
7. Start your Python webhook server in the background so it is actively listening.

Please execute the necessary commands to read the image, write the Python server, and leave it running in the background. Do not wrap the background process in any complex supervisors, just run it via standard shell backgrounding (e.g., `python3 /home/user/webhook.py &`).