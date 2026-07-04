You are an ML engineer preparing training data for a neural network designed to learn the dynamics of a coupled oscillator system (described by a system of stiff ODEs). We have a distributed data generation pipeline running locally, but it's currently producing inconsistent data and failing validation. 

The system consists of three cooperating services:
1. A Redis instance acting as a message broker and state store.
2. A Python Flask API orchestrator that dispatches simulation jobs and collects trajectories.
3. A fast C++ simulation worker that numerically solves the ODEs and pushes results to Redis.

First, you need to fix the services. The startup script `/home/user/start_services.sh` launches them, but the pipeline is failing because the services aren't properly connected. Reconfigure the environment variables and configuration files in `/home/user/config/` so that the Flask API (port 5000) can communicate with Redis (port 6379) and the C++ worker can subscribe to the correct Redis job queue.

Second, the C++ simulation engine located in `/home/user/src/sim_engine/` has a severe bug: it produces non-reproducible results across runs due to a floating-point reduction order issue during the spatial integration step. Fix the C++ code to guarantee bit-for-bit deterministic floating-point accumulation regardless of thread scheduling. Compile the engine from source using the provided Makefile.

Finally, because some old, corrupted trajectories are mixed with clean data, you must write a strict data sanitiser/classifier. Create an executable bash script or C++ program at `/home/user/bin/filter_trajectories` that takes a directory path as its only argument. It must analyze the CSV trajectory files in that directory and delete any files that exhibit the non-deterministic reduction artifacts (e.g., energy conservation drift exceeding the strict tolerance of 1e-12). Leave the clean files untouched. 

You must ensure the end-to-end flow works: trigger a job via `curl -X POST http://localhost:5000/generate`, verify the C++ worker processes it, and then run your `filter_trajectories` tool on the output directory `/home/user/data/latest/`. Write a brief summary log to `/home/user/pipeline_status.log` containing "PIPELINE_SUCCESS" when complete.