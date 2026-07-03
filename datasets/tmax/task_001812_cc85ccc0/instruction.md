I am trying to run a background Python service that processes container lifecycle metrics, but the environment is not set up correctly and the script keeps failing. 

I need you to set up the environment and run the service successfully. Here are the requirements based on the system architecture:

1. **Directory and Link Structure**: 
   The service requires a data mount directory. Create the directory `/home/user/data_mount/active`. 
   Then, the service expects a symlink at `/home/user/app/data` that points exactly to `/home/user/data_mount/active`. You will need to create the `/home/user/app` directory as well.

2. **Container Lifecycle Configuration**:
   The service reads the container state from a configuration file. Create a file at `/home/user/config/containers.json` containing valid JSON. It must contain a top-level key `"ingest-worker"` which is an object containing the key `"status"` set to the string `"running"`.

3. **Timezone/Locale Setup**:
   The service strictly requires the timezone to be set to `UTC` via the `TZ` environment variable during execution.

Here is the code for the service (`/home/user/app/ingest.py`). Save this file and run it. You do not need to modify the Python code, just satisfy its environmental requirements:

```python
#!/usr/bin/env python3
import os
import json
import time

def run_service():
    # 1. Check symlink structure
    data_dir = '/home/user/app/data'
    if not os.path.islink(data_dir):
        print("CRITICAL: Data directory is not a symlink")
        exit(1)
    if os.readlink(data_dir) != '/home/user/data_mount/active':
        print("CRITICAL: Data directory symlink destination incorrect")
        exit(1)

    # 2. Check Timezone
    if os.environ.get('TZ') != 'UTC':
        print("CRITICAL: Service must run with TZ=UTC")
        exit(1)

    # 3. Check container lifecycle config
    try:
        with open('/home/user/config/containers.json', 'r') as f:
            config = json.load(f)
            if config.get('ingest-worker', {}).get('status') != 'running':
                print("CRITICAL: Container ingest-worker is not running")
                exit(1)
    except FileNotFoundError:
        print("CRITICAL: /home/user/config/containers.json missing")
        exit(1)

    # Success
    with open('/home/user/app/success.log', 'w') as f:
        f.write("SERVICE_STARTED_SUCCESSFULLY")
    print("Service started successfully.")

if __name__ == '__main__':
    run_service()
```

Your final goal is to have the script run without errors and successfully generate the `/home/user/app/success.log` file.