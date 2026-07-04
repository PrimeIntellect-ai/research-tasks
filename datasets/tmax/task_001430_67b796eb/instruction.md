You have recently inherited an unfamiliar codebase for a video testing utility. The tool, located in `/home/user/analyzer/main.c`, is a C program designed to analyze test run videos. It uses `ffmpeg` to extract frames and then processes them using multiple pthreads to calculate the average pixel intensity of each frame.

The previous developer reported that the output data is highly erratic. When running the analyzer on a video, the resulting `output.csv` has missing frames, garbled lines, and incorrect intensity values. We suspect there is a race condition in how the threads write to the shared output file or shared memory buffers.

Your task:
1. Examine `/home/user/analyzer/main.c`.
2. Identify and fix the concurrency bug(s) causing the data corruption.
3. Compile the fixed C program (ensure you link `pthread`).
4. Run your fixed analyzer on the test video located at `/app/test_run.mp4`.
5. Ensure the tool produces a cleanly formatted `/home/user/analyzer/output.csv` containing two columns: `frame_number,intensity`.

The test video is a 10-second clip at 30 fps (300 frames). The final `output.csv` must contain exactly 300 lines (one for each frame, 0-indexed) with the correctly computed intensities. 

Our automated test will compute the Mean Absolute Error (MAE) of the intensities in your `output.csv` against a ground-truth dataset. Make sure your concurrency fixes do not alter the core intensity calculation logic, just the synchronization and data integrity.