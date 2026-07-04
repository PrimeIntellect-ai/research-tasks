You are a support engineer investigating a severe vulnerability in a legacy logging service. A customer captured a video of their diagnostic monitor right before the system crashed, but the actual logs on their system were partially wiped by the attacker. 

Your goal is to build a Bash classifier script that can scan our entire historical log database to detect if this exploit has been used against other customers. 

You have been provided with the following artifacts:
1. `/app/crash_capture.mp4`: A smartphone recording of the customer's terminal. Exactly one frame during the crash sequence displays a hex Error Code (format: `ERR_CODE: 0x...`). You must extract this code.
2. `/app/system_disk.ext4`: An unmounted loopback ext4 filesystem image. The attacker deleted the temporary mapping file `session_map.txt` from the root of this filesystem. You must recover this deleted file, which maps the `ERR_CODE` you found in the video to a specific `PAYLOAD_ID`.
3. `/app/log_formatter.elf`: The legacy binary service. You need to reverse engineer/inspect this binary to find the exact formatted string it outputs when it encounters the `PAYLOAD_ID` you recovered.

Once you have the final formatted exploit string, you must write a Bash script at `/home/user/classifier.sh` that takes a single file path as an argument.
- The script must exit with status code `1` (reject) if the log file contains the exact formatted exploit string (representing an "evil" log).
- The script must exit with status code `0` (accept) if the log file does NOT contain the exploit string (representing a "clean" log).

Requirements:
- Your script must be written in Bash and be executable.
- It must accept a single argument: the path to the log file to analyze.
- You can use standard Linux tools (e.g., `ffmpeg`, `tesseract-ocr`, `debugfs`, `strings`, `grep`).