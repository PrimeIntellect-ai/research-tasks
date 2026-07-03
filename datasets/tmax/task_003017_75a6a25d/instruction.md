You are a performance engineer tasked with optimizing a critical data processing pipeline for our lab. We have a video feed from an older spectrometer (`/app/spectrometer_feed.mp4`) that displays 2D spectral intensity readings. 

Currently, our baseline processing pipeline (`/home/user/process_spectra.sh`) extracts frames from this video, converts the pixel data to 1D signals using a provided Python script (`/home/user/deconvolve.py`), and performs statistical aggregation. 

However, we are facing two major issues:
1. **Numerical Instability:** The `deconvolve.py` script frequently crashes with a `LinAlgError` due to near-singular matrices. This happens when the video frames are completely black (no signal) or saturated. The script attempts a direct matrix factorization without any regularization.
2. **Performance:** The pipeline is far too slow for real-time analysis.

Your task:
1. **Fix the Numerical Instability:** Modify `/home/user/deconvolve.py` to use Tikhonov regularization (Ridge regression) or a stable pseudo-inverse (e.g., SVD with a condition threshold) to prevent the near-singular matrix factorization from failing. Ensure that blank frames output an array of zeros instead of crashing.
2. **Optimize the Pipeline:** Profile and optimize the Bash script `/home/user/process_spectra.sh` and the Python processing steps. You can parallelize the frame processing, optimize the ffmpeg extraction, or vectorize the Python code.
3. **Reproducible Pipeline:** Your final pipeline must be runnable simply by executing `/home/user/run_optimized.sh`. It must process the entire `/app/spectrometer_feed.mp4` video and output the final statistical summary to `/home/user/final_spectra.csv` (Format: FrameID, PeakWavelength, MaxIntensity).

**Success Criteria:**
We will evaluate your `/home/user/run_optimized.sh` script against a rigorous metric threshold. 
- **Correctness:** The output `/home/user/final_spectra.csv` must have a Mean Squared Error (MSE) of less than 1e-3 compared to our golden reference data for the peak intensities.
- **Performance:** Your optimized script must execute at least 3.0x faster than the original sequential processing logic on a standardized test set.