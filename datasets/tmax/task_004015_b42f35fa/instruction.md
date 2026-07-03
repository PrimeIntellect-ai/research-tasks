I have a video file located at `/app/video.mp4` containing a recording of a physics experiment. I need you to build a Bash-based data processing pipeline that extracts information from this video and filters out corrupted datasets based on a specific data leakage anomaly.

First, extract the frames from `/app/video.mp4` at 10 frames per second using `ffmpeg` into a directory called `/home/user/frames/`. Then, write a Bash script `/home/user/compute_stats.sh` that calculates the mean brightness of each frame (using `convert` from ImageMagick) and outputs a CSV file `/home/user/frame_stats.csv` with columns: `frame_number,mean_brightness`.

Second, I have an issue with some of my pre-processed datasets where data leaked between train and test sets during dimensionality reduction (PCA), resulting in exact duplicate feature rows across the split boundaries. 
There are two directories containing CSV datasets:
- `/app/corpus/clean/`: Contains datasets with proper test/train splits.
- `/app/corpus/evil/`: Contains datasets where test data leaked into the train set, identifiable by identical feature rows appearing in both the first half and the second half of the file.

Write a bash script `/home/user/filter_datasets.sh` that takes a directory path as an argument, evaluates every `.csv` file in that directory, and outputs the filename of any file that contains the data leak anomaly (duplicate rows between the first and second halves of the file).

Finally, run your `filter_datasets.sh` on both `/app/corpus/clean/` and `/app/corpus/evil/` and save the outputs to `/home/user/clean_results.txt` and `/home/user/evil_results.txt` respectively.

Requirements:
- Ensure all scripts are executable.
- Your `filter_datasets.sh` must return exit code 0 if it processes the directory successfully.
- The `frame_stats.csv` must be sorted by frame number.