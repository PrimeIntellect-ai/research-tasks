You are tasked with migrating a legacy user database into a new deployment structure. Unfortunately, the only surviving backup of the legacy user list is a screen recording of the old terminal paging through the database, located at `/app/legacy_user_db.mp4`.

Your task is divided into two parts: extraction and provisioning.

Part 1: Extraction
1. Analyze the video `/app/legacy_user_db.mp4`. The video shows a scrolling table with the format: `UID | USERNAME | DEPARTMENT`.
2. Extract the `USERNAME` and `DEPARTMENT` for all visible users. 
3. Save the extracted data to `/home/user/extracted_users.txt` in the exact format: `username:department` (one per line, lowercase).

Part 2: Provisioning Setup
Write and execute a Bash script at `/home/user/deploy_users.sh` that reads `/home/user/extracted_users.txt` and performs the following for each user:
1. Creates a mock home directory at `/home/user/accounts/<username>`.
2. Restricts the directory permissions so that only the owner has read/write/execute permissions, and the group has read/execute permissions (i.e., `750`). (Assume the current test user represents the owner for this mock setup).
3. Generates a shell profile file at `/home/user/accounts/<username>/.bash_profile`.
4. The `.bash_profile` must contain exactly:
   `export DEPT="<department>"`
   where `<department>` is the user's extracted department in uppercase.

To successfully complete this task, you must achieve an extraction and deployment accuracy score of at least 85% (0.85) when compared against the original legacy system's true records. You may use `ffmpeg`, `tesseract-ocr`, or Python for the extraction phase, but the deployment logic must strictly be implemented using Bash (`awk`, `sed`, `chmod`, etc.) in `deploy_users.sh`.