**Ticket #9921 - Urgent: Automated Sensor Recovery Service Offline**

Hello IT Support,

We have a critical outage. Our automated sensor recovery service (`/app/recovery_service.py`) crashed after a power failure corrupted our main sensor database (`/app/sensor_data.db` and its WAL file). 

Right before the crash, the system engineer left an automated diagnostic voicemail located at `/app/voicemail.wav`. This audio contains the spoken "calibration delta" value needed to correct the corrupted data entries.

Currently, the service fails to start because:
1. It cannot parse the database due to corrupted WAL entries.
2. Even when manually bypassing the DB, the service crashes with a `ValueError: Calibration mismatch` due to what looks like a floating-point calculation error when applying the calibration delta across 10,000 iterations.

Your objectives:
1. Listen to or transcribe `/app/voicemail.wav` to find the exact spoken calibration delta (a small decimal number).
2. Fix the numerical instability in `/app/recovery_service.py` so the calibration check passes. You must create a minimal reproducible fix that prevents the loss of precision during the data transformation.
3. Recover the SQLite database `/app/sensor_data.db` from its corrupted state so it can be queried normally.
4. Modify and run `/app/recovery_service.py` so it starts a web service bound to `127.0.0.1:8080`.
5. The web service must respond to an HTTP GET request at `/api/data` and return the latest recovered sensor reading (the row with the highest ID) in the following JSON format:
   `{"id": 105, "calibrated_value": 42.1234}`

Please fix the script, recover the DB, and leave the HTTP service running in the background. Note: You may use any transcription tools like `whisper` or `ffmpeg` available in your environment, and you can write the fix in any language, though the original service is in Python.