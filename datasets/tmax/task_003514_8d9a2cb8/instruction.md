As a capacity planner, you need to analyze historical server load to configure future container deployments and health checks. You have been provided with a time-lapse video `/app/server_load.mp4` which records a server rack's diagnostic load LED matrix. 

Your goal is to process this video to determine the overall average server load, and prepare a monitoring script that would run via cron.

Perform the following tasks:
1. **Timezone Configuration:** Configure the user's local timezone to `Etc/UTC` by ensuring the `TZ` environment variable is set appropriately in `/home/user/.bashrc`.
2. **Video Analysis (C Programming):** The video `/app/server_load.mp4` has a resolution of 640x480. The actual load indicator is located in the center 100x100 pixel region (x from 270 to 369, y from 190 to 289). 
   Write a C program at `/home/user/analyzer.c` and compile it to `/home/user/analyzer`. The program should read raw 8-bit grayscale 640x480 frames from standard input (`stdin`), extract the center 100x100 region, and compute the average pixel intensity for that region across all frames. 
   The server load percentage is calculated as `(average_intensity / 255.0) * 100`.
3. **Execution & Metric:** Run your compiled C program by piping raw grayscale video data from `ffmpeg`. (Hint: use `ffmpeg -i /app/server_load.mp4 -f image2pipe -pix_fmt gray -vcodec rawvideo -`).
   Save the final computed average server load percentage as a single floating-point number (e.g., `45.67`) to `/home/user/average_load.txt`.
4. **Scheduled Task Setup:** Create a bash script at `/home/user/monitor.sh` (ensure it is executable) that contains the exact `ffmpeg | ./analyzer` pipeline command you used. Then, create a cron-formatted file at `/home/user/monitor.cron` that would execute `/home/user/monitor.sh` every day at 2:30 AM.

Ensure your C program handles the EOF correctly to average across the entire video.