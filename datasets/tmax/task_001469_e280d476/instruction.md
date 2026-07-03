A materials researcher needs your help organizing and extracting dataset pairs consisting of CNC toolpaths and corresponding high-speed video frames.

The system has a video recording of a machining job located at `/app/recording.mp4`. 
The toolpath dataset is stored on an unmounted disk image at `/app/cnc_data.ext4`.

Here is what you need to do:
1. **Mount and Restore Data:**
   - Mount the ext4 image `/app/cnc_data.ext4` to the directory `/app/dataset` (create the directory if it doesn't exist).
   - Inside `/app/dataset`, you will find an incremental backup dataset: `base.tar` and a differential update `update.tar`.
   - Reconstruct the final dataset in a new directory `/app/restored` by first extracting `base.tar` and then applying `update.tar` over it. This will yield the final `/app/restored/job.gcode` file.

2. **Networked Extraction Service:**
   - Write a C program at `/app/server.c` and compile it to `/app/server`.
   - The program must act as a TCP server listening on `0.0.0.0:7777`.
   - The server must handle incoming plaintext requests matching the format: `EXTRACT Z=<float>\n` (where `<float>` is a Z-height coordinate, e.g., `EXTRACT Z=2.5\n`).
   
3. **Parsing and Extraction Logic:**
   - Upon receiving a request, the server must parse `/app/restored/job.gcode`.
   - Look for the domain-specific synchronization comment matching the requested Z-height exactly. The format in the file is: `; SYNC T=<hh:mm:ss> Z=<float>`
   - If the Z-height is found, the server must extract the exact frame at that `T=<hh:mm:ss>` timestamp from `/app/recording.mp4` using `ffmpeg`, and save it to `/app/frames/frame_<float>.jpg`. (Make sure `/app/frames` exists).
   - The server must read the file size in bytes of the newly created JPEG image.
   - The server replies to the TCP client with: `SUCCESS T=<hh:mm:ss> BYTES=<size>\n`
   - If the Z-height is not found in the GCode file, the server must reply with: `ERROR NOT_FOUND\n`
   - The server should stay alive to handle multiple sequential requests.

Do not use third-party HTTP or complex socket libraries—standard POSIX C libraries (`<sys/socket.h>`, `<stdio.h>`, etc.) and `system()` or `popen()` calls to `ffmpeg` are fully expected and encouraged. 
Ensure your server is running in the background listening on port 7777 when you are finished.