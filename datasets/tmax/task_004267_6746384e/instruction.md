You are a Site Reliability Engineer investigating a series of mysterious server downtimes and SSH lockouts. We suspect a compromised SSH daemon is silently rejecting key-based logins and causing the virtualization stack to crash.

You have three objectives to complete:

1. **Video Analysis of VM Console (C++ & FFmpeg)**
We managed to capture a VNC recording of the VM's console during a crash, located at `/app/vnc_capture.mp4`. The crash manifests as a pure red square (RGB: 255, 0, 0) of exactly 20x20 pixels appearing anywhere on the screen.
- Use `ffmpeg` to extract the frames.
- Write a C++ program `/home/user/analyze_frames.cpp` (and compile it to `/home/user/analyze_frames`) that reads these frames and finds the FIRST frame index (0-indexed) where this red square appears.
- Write this single integer to `/home/user/crash_frame.txt`.

2. **Adversarial Log Classifier (C++)**
We need a robust detector to find the silent SSH rejection anomaly. 
- Write a C++ program `/home/user/classifier.cpp` (compiled to `/home/user/classifier`).
- It must accept a single file path as a command-line argument: `./classifier <path_to_log_file>`
- It must return exit code `0` (clean) if the log file represents normal SSH traffic.
- It must return exit code `1` (evil) if the log file contains the anomaly.
- The anomaly is defined as: An `sshd` log line containing `Accepted publickey`, followed by another `sshd` log line containing `Connection closed by authenticating user`, where the timestamps of these two events are exactly identical (down to the second).
- You are provided with two validation datasets:
  - `/app/corpus/clean/`: Contains 50 normal log files.
  - `/app/corpus/evil/`: Contains 50 anomalous log files.
- Your classifier must correctly classify 100% of both corpora.

3. **Process Supervisor (Bash)**
Write a bash script `/home/user/supervisor.sh` that:
- Starts a mock QEMU process (provided at `/app/mock_qemu.sh`).
- Monitors its PID.
- If `/app/mock_qemu.sh` exits with a non-zero exit code, the supervisor must restart it within 1 second.
- The supervisor should run indefinitely and log all restarts (timestamp and "Restarted QEMU") to `/home/user/supervisor.log`.

Ensure all code is compiled and scripts are executable. The automated grading system will run your classifier against a hidden test set of logs and check your extracted frame number.