You are a monitoring specialist setting up a custom health-check and alert listener service. The system must be written in C.

We received an automated voicemail from the primary sysadmin team detailing the required timezone configuration and a secret trigger keyword for our alerting system.

Your tasks are:
1. Process the audio file located at `/app/voicemail.wav` to extract the spoken target timezone and the secret alert keyword. You may use any available tool (e.g., Python with speech recognition, or whisper if installed) to transcribe the audio. 
2. Write a C program at `/home/user/monitor.c` and compile it to `/home/user/monitor`.
3. The C program must run as a network service listening on TCP port 8080 on `127.0.0.1`.
4. The service must handle two types of HTTP/1.1 requests (a rudimentary HTTP parser is sufficient):
   - **Health Check**: When the service receives a `GET /health` request, it must respond with an HTTP status of `HTTP/1.1 200 OK\r\n\r\n` followed by the current date and time formatted exactly as `YYYY-MM-DD HH:MM:SS %Z` (e.g., `2023-10-05 14:30:00 CEST`) corresponding to the timezone extracted from the voicemail. You must ensure the C program properly respects this timezone.
   - **Alert Trigger**: When the service receives a `POST /alert` request, it should check the body of the request. If the body exactly matches the secret alert keyword spoken in the voicemail (case-sensitive, ignoring leading/trailing whitespace), the server must respond with `HTTP/1.1 202 Accepted\r\n\r\nTRIGGER_MAIL`. If the keyword does not match or is missing, it must respond with `HTTP/1.1 403 Forbidden\r\n\r\n`.
5. Start your compiled C server and leave it running in the background so that the automated verification system can test it.

Ensure your C code handles socket creation, binding, listening, and basic connection acceptance. Keep the HTTP parsing simple (checking for "GET /health" and "POST /alert" in the received buffer is enough).