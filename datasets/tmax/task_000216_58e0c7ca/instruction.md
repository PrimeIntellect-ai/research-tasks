You are a mobile build engineer responsible for maintaining our CI/CD pipeline infrastructure. We have a bottleneck in our build artifact merging step, and some of the configuration is locked in a legacy dashboard screenshot.

Your task is to optimize the pipeline and generate the final merged build manifest.

1. **Extract Build Version**:
   There is a screenshot of our legacy build dashboard at `/app/dashboard.png`. Use OCR (e.g., `tesseract`) to read the text from this image. You are looking for a string in the format `RELEASE_VERSION: <version_string>`.

2. **Optimize the Merging Script**:
   Our build pipeline relies on a Python script located at `/home/user/merge_builds.py` to parse URL routing parameters from build logs and filter out older modules to find the latest build for each module. 
   Currently, the script reads from `/app/routes.json` and runs extremely slowly (it has an O(N^2) complexity). 
   You must refactor `/home/user/merge_builds.py` to be more efficient (e.g., O(N)). It must produce the exact same logical output but execute significantly faster.

3. **Generate Final Artifact**:
   Run your optimized script and save the output to `/home/user/release_<version_string>.json` (replace `<version_string>` with the version you extracted from the image).

Your success will be measured by two things:
- The presence and correctness of `/home/user/release_<version_string>.json`.
- A performance metric: your refactored `/home/user/merge_builds.py` must process the dataset in under 1.0 seconds.

Do not alter the command line signature of `merge_builds.py`. It should still take the output file path as its first argument: `python3 /home/user/merge_builds.py <output_file>`.