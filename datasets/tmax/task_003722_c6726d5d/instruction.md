You need to help organize a messy project directory and extract critical runtime errors from a live application log. 

The project is located at `/home/user/project`. 
There is a simulated background process actively writing logs to `/home/user/project/live.log`. 

Please perform the following operations:
1. **Cleanup**: Find all `.tmp` files in `/home/user/project` (and its subdirectories) that are strictly larger than 10KB and delete them. Do not delete smaller `.tmp` files.
2. **Configuration Update**: The file `/home/user/project/config.ini` currently has a setting `LOG_LEVEL=DEBUG`. Use a command-line text transformation tool (like `sed`) to change this line to `LOG_LEVEL=INFO`.
3. **Live Log Parsing**: Write a Python script at `/home/user/watcher.py` that tails/watches the actively growing `/home/user/project/live.log` file. 
   - The log contains single-line `[INFO]` records and multi-line `[ERROR]` records. 
   - Every log record starts with a bracket `[`. A multi-line record continues until the next line starting with `[` appears.
   - Your Python script must capture exactly the first 3 complete multi-line `[ERROR]` records it sees, write them to `/home/user/project/errors_found.log`, and then exit cleanly. 

Run your Python script so that `/home/user/project/errors_found.log` is generated. You have succeeded once the `.tmp` files are cleaned, the config is updated, and the `errors_found.log` file contains exactly 3 parsed multi-line error blocks.