You are a researcher organizing a dataset of 3D printing jobs. You have received an archive containing the logs and instructions for a print job, as well as a video of the print process. However, some of the archives in this dataset were poorly packaged and might contain directory traversal attacks (zip slip / tar slip).

Your task is to write a C program that processes this data and an HTTP server to serve the results. 

Specifically, you need to:
1. Write a C program (e.g., `analyze.c`) that reads a tar file located at `/home/user/dataset/job.tar`.
2. The C program must implement archive integrity verification by scanning the tar headers and **only** extracting files that do not contain `../` in their path. Extract the safe files to `/home/user/extracted/`.
3. Within the extracted files, you will find `print.gcode`. Parse this domain-specific GCode file to calculate the total extrusion (the sum of all `E` values in lines starting with `G1`).
4. Parse the multi-line log file `machine.log` (also in the archive) to find the final "Status:" value (the last time "Status:" appears, followed by its value on the next line).
5. Analyze the video fixture located at `/app/print_video.mp4`. Use `ffmpeg` (which is preinstalled) from within your C program or via a shell script to extract the frames. Count the number of "flash" frames in the video. A flash frame is defined as a frame where the average pixel brightness (grayscale) is greater than 200.
6. The C program should output a JSON file named `result.json` in `/home/user/web/` with the following format:
```json
{
  "total_extrusion": 123.45,
  "final_status": "Complete",
  "flash_frames": 5
}
```
7. Finally, bring up an HTTP server listening on `127.0.0.1:8080` that serves the `/home/user/web/` directory.

The automated verifier will make a `GET` request to `http://127.0.0.1:8080/result.json` to check your work. Ensure the server remains running in the background.

Use C as the primary language for the extraction and parsing logic. You may use shell commands and Python for the web server part.