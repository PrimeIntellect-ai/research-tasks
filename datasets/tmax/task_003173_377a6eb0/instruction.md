We have a multi-language video tracking pipeline that processes surveillance footage to track a moving object. Recently, we noticed a severe degradation in the tracking accuracy. The bounding boxes start fine but drift significantly over time, suggesting a cumulative precision loss regression.

The source code for the pipeline is located in a Git repository at `/home/user/tracker_repo`. 
- The commit tagged `v1.0` is known to be good.
- The `HEAD` of the `main` branch (which has about 200 new commits) is known to be bad.

The pipeline consists of a Bash orchestrator (`run_pipeline.sh`), a C++ frame extractor, and a Python tracker. You can run the pipeline on a test video using:
`./run_pipeline.sh /app/test_video.mp4 output.csv`

Your task:
1. Perform a git bisection between `v1.0` and `HEAD` to identify the exact commit that introduced the precision loss regression.
2. Analyze the faulty commit to understand how the numerical error (precision loss) was introduced.
3. Fix the bug in the current `HEAD` of the `main` branch.
4. Run the fixed pipeline on `/app/test_video.mp4` to generate the final bounding boxes.
5. Save the final tracking results to `/home/user/final_output.csv`. The CSV must have the columns `frame_id,x,y,w,h`.

You must ensure that your fix fully resolves the precision loss. We will evaluate your `/home/user/final_output.csv` against our hidden ground truth by computing the Mean Squared Error (MSE) of the bounding box coordinates.