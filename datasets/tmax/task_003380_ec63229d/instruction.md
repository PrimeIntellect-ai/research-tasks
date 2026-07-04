You have inherited a legacy C++ emergency dispatch system located in `/home/user/dispatch_service`. The system is currently non-functional and has several overlapping issues. Your goal is to debug, repair, and launch the service so it correctly processes incoming dispatch requests.

Here is what you need to fix:

1. **Audio Pipeline Bug:** The system processes incoming audio files to extract dispatch codes. There is an audio file at `/app/dispatch call.wav` and a processing script `/home/user/dispatch_service/process_audio.sh`. The script is currently failing to process the audio file because it improperly handles filenames with spaces. Fix the script and run it on the audio file. The script will output a transcription containing a secret access token. You will need this token for the service.

2. **Database Corruption:** The system relies on an SQLite database of responder locations at `/home/user/dispatch_service/data/responders.db`. The database file is corrupted, but the WAL (Write-Ahead Log) file is intact. You must recover the database so that the C++ service can read the latest responder coordinates. 

3. **Formula Regression:** The C++ service uses a mathematical formula (Haversine distance) to find the closest responder to a dispatch event. A recent commit introduced a regression that calculates the distance incorrectly. The repository in `/home/user/dispatch_service` has a test script `./run_tests.sh`. Use `git bisect` to identify the commit that broke the formula, understand the error, and correct the formula implementation in `src/distance.cpp`.

4. **Service Deployment:** Once the code is fixed and compiled (using `make`), start the C++ HTTP server. It must listen on `127.0.0.1:8080`. 

The service must accept `GET /dispatch?lat=<x>&lon=<y>` requests. When the server receives a request with the `Authorization: Bearer <TOKEN>` header (where `<TOKEN>` is the word extracted from the audio file), it should query the recovered database, calculate the correct closest responder using the fixed C++ code, and return a JSON response: `{"responder_id": "<ID>", "distance": <DIST>}`.

Ensure the server remains running in the background so the automated verification system can issue requests to it.