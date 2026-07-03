You are tasked with fixing a pipeline that has recently started failing due to a floating-point precision regression. A repository located at `/home/user/repo` contains a script `aggregate.py`. At some point in the last 200 commits, a developer "optimized" the summation logic, inadvertently introducing a catastrophic cancellation bug that affects certain edge-case input data.

We need to build a quarantine filter that detects these adversarial/edge-case inputs before they hit the pipeline.

Your objectives:
1. **Git Forensics**: Inspect `/home/user/repo` to find the exact commit that introduced the floating-point regression in `aggregate.py`. Understand the mathematical difference between the pre-regression (correct) and post-regression (buggy) intermediate states.
2. **Recover Threshold**: An automated alert screenshot was captured when the regression first hit production. It is saved at `/app/alert.png`. You must use OCR or image inspection tools (like `tesseract`, which is pre-installed) to read the exact floating-point tolerance threshold from this image.
3. **Build the Detector**: Write a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument. 
    * The input file will contain a JSON list of floating-point numbers.
    * Your script must compute the difference between the expected result (using the correct logic from before the regression) and the buggy result (using the current HEAD's logic).
    * If the absolute difference is *strictly greater* than the threshold recovered from `/app/alert.png`, print exactly `EVIL` to standard output.
    * Otherwise, print exactly `CLEAN` to standard output.

We will test your script by running:
`python3 /home/user/detector.py <test_file.json>`
It must print only `EVIL` or `CLEAN` (and nothing else) for each test file.