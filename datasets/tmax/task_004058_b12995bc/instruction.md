You are assisting a researcher in organizing an experimental dataset.

We have a video artefact of the experiment located at `/app/experiment.mp4`. 
We also have a binary metadata file at `/app/metadata.bin` that contains annotations for the first 100 frames of the video.

The binary file `/app/metadata.bin` has a 16-byte global header:
- Magic bytes: `0x44 0x41 0x54 0x41` ("DATA")
- Version: 32-bit unsigned integer (little-endian)
- Record count: 64-bit unsigned integer (little-endian)

Following the global header, there are exactly 100 records, each 16 bytes long:
- Frame Number: 32-bit unsigned integer (little-endian)
- Event Code: 32-bit unsigned integer (little-endian)
- Sensor Value: 64-bit IEEE 754 double precision float (little-endian)

Your task consists of the following steps:

1. **Frame Extraction**: Extract the first 100 frames from `/app/experiment.mp4` as JPEG images into a new directory `/home/user/dataset/frames/`. The initial extraction format should be `frame_%03d.jpg` (e.g., `frame_001.jpg`).

2. **Binary Parsing and Bulk Renaming**: Write a C program at `/home/user/organize.c` that:
   - Reads the directory `/home/user/dataset/frames/`.
   - Parses the `/app/metadata.bin` file to extract the `Event Code` and `Sensor Value` for each frame.
   - Bulk renames the 100 frames in the directory from `frame_%03d.jpg` to the format: `evt<Event Code>_val<Integer part of Sensor Value>_frm<Frame Number>.jpg`. 
   - Compile and execute this program to rename the files.

3. **Incremental/Differential Backups**: 
   - The researcher needs a snapshot system. Create a full `tar` backup of the first 50 frames (frames 001 to 050) located in `/home/user/dataset/` named `base_backup.tar`.
   - Then, create a differential/incremental `tar` archive named `diff_backup.tar` that represents the addition of frames 051 to 100. (Hint: Use GNU `tar`'s listed-incremental feature with a snapshot file at `/home/user/dataset/snapshot.snar`).

4. **Network Service**:
   - Write a C server at `/home/user/server.c` that listens on `127.0.0.1:8080`.
   - The server must implement a basic HTTP/1.0 or HTTP/1.1 service that handles `GET` requests.
   - When receiving `GET /backups/base`, it must respond with a `200 OK` header, `Content-Type: application/x-tar`, and serve the contents of `base_backup.tar`.
   - When receiving `GET /backups/diff`, it must respond similarly but serve the contents of `diff_backup.tar`.
   - The server must run continuously in the background.

Ensure your server is compiled, running, and listening on `127.0.0.1:8080` before you finish. Do not exit until the server is actively serving requests.