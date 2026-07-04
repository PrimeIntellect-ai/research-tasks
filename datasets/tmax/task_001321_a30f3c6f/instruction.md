You are an MLOps engineer managing an experiment tracking pipeline. Some of our experiment tracking logs have been corrupted—specifically, the CSV logs containing `event_id` and `frame_idx` occasionally have missing `frame_idx` values. This missing data causes standard data processing libraries (like pandas) to silently cast the entire `frame_idx` column to floats (e.g., `15.0` instead of `15`), which breaks downstream video extraction tools that expect strict integers.

Your task is to write a reproducible bash-based pipeline that safely processes these logs and benchmarks an inference metric (mean brightness) from the corresponding video frames.

Write an executable script at `/home/user/pipeline.sh`.
The script must:
1. Accept the path to a video file as its first positional argument.
2. Read a CSV from standard input containing two columns: `event_id,frame_idx`.
3. Discard any rows where `frame_idx` is empty.
4. Ensure `frame_idx` is treated strictly as an integer (e.g., `15`, not `15.0`).
5. Print a CSV header to standard output: `event_id,frame_idx,mean_brightness`.
6. For each valid row, extract the exact frame matching `frame_idx` from the video using `ffmpeg`. (Select the frame by its index `n`).
7. Calculate the mean brightness of that extracted frame using ImageMagick, specifically using the exact command: `convert <extracted_frame_image> -colorspace Gray -format "%[fx:mean]" info:`
8. Append the result to standard output in the format `event_id,frame_idx,mean_brightness`.

Example stdin:
```csv
event_id,frame_idx
evt_1,5
evt_2,
evt_3,12
```

Example stdout:
```csv
event_id,frame_idx,mean_brightness
evt_1,5,0.41235
evt_3,12,0.61201
```

A sample video artifact is located at `/app/experiment_video.mp4` for you to test your script.
Your script will be verified by a fuzzer that pipes hundreds of randomly generated log snippets to your script and compares the output byte-for-byte against a reference oracle. Make sure there are no trailing spaces or hidden debug outputs on standard output.