You are a Cloud Architect migrating a legacy storage monitoring and backup service to a new server. The original configuration files were lost, and the only remaining specification is a scanned architectural diagram located at `/app/legacy_diagram.png`.

Your task is to write and deploy a replacement service in **Rust** that fulfills the requirements embedded in that diagram, combining storage monitoring, backup automation, and process management.

Here are the steps you must take:

1. **Information Extraction**:
   Analyze the image at `/app/legacy_diagram.png` (you can use pre-installed tools like `tesseract`). It contains the exact `PORT` the service must listen on, and the maximum storage `QUOTA` (in MB) it is supposed to monitor.

2. **Service Implementation (Rust)**:
   Create a new Rust application in `/app/service/` (e.g., using `cargo init`).
   Write an HTTP server in Rust that binds to `0.0.0.0:<PORT>` (using the port from the image).
   
   The server must implement the following routes:
   - `GET /api/status`
     Must return a JSON response with the HTTP status 200 containing exactly this structure:
     `{"port": <PORT>, "quota": <QUOTA>, "status": "running"}`
     (Substitute `<PORT>` and `<QUOTA>` with the integer values extracted from the image).

   - `POST /api/backup`
     When this endpoint is hit, the Rust server must programmatically execute a system command to create a compressed tar archive of the `/app/storage/` directory and save it as `/app/backup/archive.tar.gz`.
     Once the backup command completes successfully, return a 200 JSON response: `{"status": "success"}`.

3. **Process Management**:
   Compile the Rust application for release (`cargo build --release`).
   Run the compiled binary in the background so that it continues listening for requests. You may use `nohup`, `&`, or a simple bash script to detach the process, but the service *must* be running and bound to the correct port when you complete the task.

Make sure the directories `/app/storage/` and `/app/backup/` exist (create `/app/backup/` if necessary; `/app/storage/` already exists with data). Do not stop the service once started.