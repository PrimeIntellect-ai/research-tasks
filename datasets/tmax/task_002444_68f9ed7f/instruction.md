You are a Machine Learning Engineer preparing a dataset for half-precision (fp16) mixed-precision training. We have two tasks to complete to ensure our pipeline is numerically stable and our feature extraction works.

**Task 1: Video Feature Extraction**
We have a source video located at `/app/training_source.mp4`. 
Using standard command-line tools (like `ffmpeg` and python), extract a single frame at exactly the 2-second mark (00:00:02). Convert this frame to grayscale. Calculate the mean pixel intensity of this grayscale frame (on a 0 to 255 scale) and write this single numerical value, rounded to exactly 2 decimal places, into `/home/user/frame_avg.txt`.

**Task 2: fp16 Numerical Sanitizer**
We have scraped thousands of feature files (stored as CSVs with comma-separated floating-point numbers), but some contain numerical outliers that cause overflow/NaN issues when cast to standard IEEE 754 float16, destroying our inference benchmarking and model accuracy. 

Create an executable script at `/home/user/filter_corpus.py` (you can use Python or Bash) that takes a single file path as its first command-line argument. 
- The script must read the CSV file.
- It must exit with status code `0` (accept) if ALL numbers in the file can be safely represented in standard float16 without overflowing to Infinity or -Infinity.
- It must exit with status code `1` (reject) if ANY number in the file exceeds the maximum/minimum finite limits of float16 (i.e., magnitude strictly greater than 65504), or if it contains `inf`, `-inf`, or `nan`.

Your script must handle arbitrary CSV dimensions (multiple rows and columns of floats). Make sure the script is executable (`chmod +x`). Do not rely on external libraries other than standard Python libraries or `numpy`.