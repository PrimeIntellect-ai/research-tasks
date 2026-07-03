You are a site administrator managing a secure environment. As part of a recent security audit, a user's QEMU VM VNC session was recorded. We suspect an unauthorized batch creation of user accounts occurred during a sudden workspace switch, which manifests as a massive visual update on the screen.

Your task is to analyze the video recording of this session and pinpoint the exact moment of this screen wipe. 

You must implement a solution using Shell Scripting and C++ to find the frame where the screen changes the most.

Instructions:
1. The video file is located at `/app/vnc_session.mp4`.
2. Write a shell script `/home/user/analyze_audit.sh` that performs the following steps:
   a. Uses `ffmpeg` to extract the frames of the video into a temporary directory as uncompressed PPM (Portable Pixmap) images.
   b. Compiles a C++ program `/home/user/detector.cpp` to an executable `/home/user/detector`.
   c. Runs the compiled `detector` executable in the background, monitors its process ID, and waits for it to complete.
   d. Cleans up the extracted frames after the C++ program finishes to save disk space.
3. Write the C++ program `/home/user/detector.cpp`. This program must:
   a. Read the sequence of extracted PPM frames.
   b. For every consecutive pair of frames (Frame N and Frame N+1), compute the average pixel-wise absolute difference across all RGB channels. (i.e., sum of absolute differences of all subpixels divided by the total number of subpixels).
   c. Identify the frame index `N` (0-indexed, where the first frame of the video is 0) that yields the maximum average absolute difference with frame `N+1`.
   d. Write only this integer frame index `N` to the file `/home/user/peak_frame.txt`.

Constraints & Notes:
- You do not have `sudo` access to install new packages. Use standard C++ libraries (`<iostream>`, `<fstream>`, `<vector>`, etc.) to parse the PPM files. PPM (P6 format) is simple to parse natively.
- Make sure your script handles environment setup and gracefully monitors the background C++ process.
- The automated verifier will evaluate the numeric value in `/home/user/peak_frame.txt`. Your extracted frame index must be extremely close to the true peak frame.