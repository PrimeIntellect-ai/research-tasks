You are acting as a performance engineer for a scientific computing lab. We are analyzing a physical experiment recorded in `/app/experiment.mp4`. The video tracks the motion of a highly reflective particle in a fluid flow network. 

Your task is to:
1. **Video Analysis & Curve Fitting:** Extract frames from `/app/experiment.mp4`. The particle is the brightest spot in the video. Extract its (x, y) coordinates for each frame to reconstruct its trajectory. Perform a polynomial regression (curve fitting) on the x and y coordinates with respect to the frame number. Write the fitted coefficients to `/home/user/fitted_trajectory.json`.
2. **Simulation Profiling & Fixing:** We have a C++ simulation code located in `/home/user/sim_source/` that models this particle using a dynamic mesh and domain decomposition over a directed graph (representing the fluid network). Currently, the simulation's numerical integrator diverges due to an incorrect step-size adaptation logic in `integrator.cpp`. Fix the C++ code so that the simulation remains stable and tracks closely to your fitted trajectory from the video. Compile the software using the provided `Makefile`.
3. **Service Deployment:** Build and start an HTTP server in C++ (using a lightweight library like cpp-httplib, which you will need to install/configure) that serves the corrected simulation results. 
   - The server must listen on `127.0.0.1:8080`.
   - It must expose a `GET /simulate?t=<time_step>` endpoint.
   - It must require an `Authorization: Bearer sim-token-42` header.
   - The response should be a JSON object containing the predicted `x` and `y` coordinates at the requested time step, based on your fixed simulation code.

Start the server in the background and ensure it is robust enough to handle sequential requests.