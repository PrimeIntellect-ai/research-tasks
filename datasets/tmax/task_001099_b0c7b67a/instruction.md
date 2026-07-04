You are an ML engineer tasked with fixing a broken data preparation pipeline. An upstream pandas job has silently corrupted some of our training data by introducing `NaN` values and converting integer token IDs into floats (e.g., `5` became `5.0`). 

You need to accomplish two tasks:

**Task 1: Video Sync Extraction**
We have a diagnostic video of the sensor status at `/app/sync_video.mp4` (10 fps). A frame is considered "corrupt" if its average brightness (luma) is greater than 128 (out of 255). 
Extract the 0-indexed frame numbers of all corrupt frames and save them to `/home/user/corrupted_frames.txt`, one integer per line, sorted in ascending order. You may use `ffmpeg` and any scripts you like to achieve this.

**Task 2: C-based Data Sanitizer**
We need a strict, high-performance filter to check our dataset shards before they reach the model.
Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
The program must take exactly one command-line argument: the path to a CSV file.
The CSV files have three columns with a header row: `id,measurement,category_token`.

Your C program must validate the `category_token` column for every row (skipping the header).
A file is considered **clean** ONLY IF every single row's `category_token` is a strictly positive integer formatted without decimals (e.g., `1`, `42`).
A file is considered **evil** (corrupted) if ANY row's `category_token` contains a decimal point (e.g., `5.0`), is `NaN`, `Inf`, or is less than or equal to `0`.

- If the file is completely clean, your program must exit with status code `0`.
- If the file is evil, your program must exit with status code `1`.

Ensure your C code is robust against standard CSV formatting and accurately identifies the silent type-casting corruptions.