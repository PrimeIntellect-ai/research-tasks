You are a bioinformatics analyst evaluating a novel biochemical microarray assay. We have captured a time-lapse video of the fluorescent assay over time, located at `/app/microarray_timelapse.mp4`. 

Your goal is to process the video, perform statistical analysis on the array's quadrants, identify the point of assay convergence, and expose the results via a custom Bash-built HTTP server.

**Requirements:**
1. **Video Extraction:** Use `ffmpeg` to extract exactly 1 frame per second from the video. Output them as grayscale PGM (Portable GrayMap) files in `/home/user/frames/`.
2. **Multi-dimensional Array Processing (Bash/Awk):** Write a bash/awk pipeline to process each PGM frame. The image represents a grid. You must divide the image strictly into 4 equal quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right). Calculate the mean pixel intensity for each quadrant for every extracted frame. 
3. **Convergence Testing:** The assay is considered "converged" when the absolute difference in mean intensity for *all four quadrants* simultaneously changes by less than `2.0` compared to the immediate previous frame. Write a bash script to iteratively test for this convergence. Find the integer frame index (1-based, e.g., 1, 2, 3...) where convergence first occurs.
4. **Notebook-based Orchestration:** Create a master executable script at `/home/user/run_analysis.sh` that automates steps 1-3 sequentially and outputs a log file at `/home/user/analysis.log` detailing the frame-by-frame intensities.
5. **Multi-protocol API Service:** Write a purely Bash-based web server (using `nc` or `socat` inside a loop in a script located at `/home/user/server.sh`) listening on TCP port `8080`. It must handle basic HTTP GET requests:
   - `GET /convergence HTTP/1.1` -> Respond with standard HTTP 200 headers and a body containing *only* the integer frame number where convergence occurred.
   - `GET /intensities HTTP/1.1` -> Respond with standard HTTP 200 headers and a body containing the converged frame's four mean intensities in exactly this format: `TL=<val>,TR=<val>,BL=<val>,BR=<val>` (rounded to 2 decimal places).

Run your analysis pipeline and leave the `/home/user/server.sh` script running in the background so our verification suite can query your API.