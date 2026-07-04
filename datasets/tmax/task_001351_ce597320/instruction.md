I am a researcher running stochastic simulations, and I've been running into numerical instabilities. I need you to build a robust detector in Rust that can identify these unstable simulation trajectories so I can filter them out of my regression testing pipeline.

My colleague determined the exact statistical threshold for our hypothesis test to detect instability, but they only left a screenshot of the parameter table at `/app/threshold.png`. 

Your task is to:
1. Extract the statistical threshold from `/app/threshold.png`. It contains a threshold value `T` for the maximum allowed Z-score.
2. Create a Rust CLI application in `/home/user/sim_filter`. 
3. The compiled binary at `/home/user/sim_filter/target/release/sim_filter` must take a single file path as its argument.
4. The input files are JSON containing simulation trajectories: `{"time": [float, ...], "values": [float, ...]}`.
5. The application must calculate the mean and standard deviation (population standard deviation) of the `values` array. 
6. It must then check if the absolute Z-score of *any* single value in the trajectory exceeds the threshold `T` found in the image. (Z-score = |value - mean| / std_dev).
7. If any value exceeds the threshold, the simulation is unstable. The program should exit with status code `1`.
8. If no value exceeds the threshold, the simulation is stable. The program should exit with status code `0`.

Please write, compile, and test this Rust tool. It must perfectly separate the stable trajectories from the unstable ones based on this statistical hypothesis comparison. Make sure you compile the final version in release mode.