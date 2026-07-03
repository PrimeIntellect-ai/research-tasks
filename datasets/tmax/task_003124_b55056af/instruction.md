You are helping a researcher organize a complex video and archive dataset. Complete the following operations:

1. **Archive Processing**: There is an archive located at `/app/dataset_archive.tar`. Some files inside it contain malicious directory traversal paths (e.g., `../../../etc/malicious`). Safely extract only the valid files that resolve inside `/home/user/extracted_dataset/`. Do not allow any files to be extracted outside this directory. Keep track of the number of valid files extracted.
2. **Video Analysis**: There is a video dataset located at `/app/experiment_feed.mp4`. Use `ffmpeg` to extract the metadata of this video. Count the exact number of frames in this video.
3. **Data Filter Script**: Write a Bash script at `/home/user/filter_dataset.sh`. This script will be executed with a single argument: a string representing a log entry in the format `[TIMESTAMP] STATUS_CODE /path/to/file`. 
   Your script must:
   - Use standard stream redirection to process the input.
   - Output `VALID` if the STATUS_CODE is between 200 and 299.
   - Output `INVALID` if the STATUS_CODE is 400 or above.
   - Output `UNKNOWN` for any other status code.
   - Append the extracted frame count from step 2 to the end of the output (e.g., `VALID 1450`).
   - Implement basic file locking using `flock` on `/tmp/filter.lock` to ensure concurrent accesses do not interleave incorrectly if we run it in parallel.

Make sure `/home/user/filter_dataset.sh` is executable. Automated tests will verify your script by fuzzing it with thousands of random log entries and comparing its output to a strict reference implementation.