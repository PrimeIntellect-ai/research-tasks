You are an ML engineer preparing training data. We need to associate asynchronous event timestamps with video frames from our experiment recordings. We found that our previous Python/Pandas pipeline was silently corrupting integer features by introducing NaNs during a `merge_asof` operation when timestamps were out of bounds, so we are rewriting the matching component in C for strict control and speed.

Your task is to write a highly efficient C program that performs a "latest-frame" lookup for a stream of timestamps.

1. Analysis Environment Setup:
The video file is located at `/app/experiment_video.mp4`. Use `ffprobe` to extract the presentation timestamps (`pkt_pts_time`, as floats) and packet sizes (`pkt_size`, as integers) for all video streams.

2. C Implementation:
Write a C program at `/home/user/fast_query.c` and compile it to `/home/user/fast_query`.
The program should first load/index the frame metadata (timestamps and sizes) from the video (you may generate an intermediate file in your setup script and read it in C, or invoke a parser, but the query response must be fast).
Then, it should enter an interactive loop reading float timestamps from `stdin` (one per line).
For each queried timestamp `T`:
- Find the video frame whose `pkt_pts_time` is the largest value less than or equal to `T`.
- If `T` is smaller than the very first frame's timestamp, output `NaN`.
- If `T` is greater than or equal to the last frame's timestamp, use the last frame.
- Print the matching frame's size to `stdout` in this exact format: `[T] -> [size]` (e.g., `1.2345 -> 14500`). For `NaN` cases, print `[T] -> NaN`. Format `T` with exactly 4 decimal places.
- Flush `stdout` after each response.

3. Optimization:
The program will be tested against millions of random queries, so scanning the file sequentially per query will fail. Load the metadata into an array and use binary search.

Compile your program with `gcc -O3 /home/user/fast_query.c -o /home/user/fast_query`.