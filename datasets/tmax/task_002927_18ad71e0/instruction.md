You are an operations engineer triaging a critical incident in our distributed mathematical calculation engine. Our system consists of three services: a Node.js API gateway, a Redis job queue, and a C++ mathematical worker. 

Currently, two things are broken:
1. The C++ worker is crashing with segmentation faults when processing certain mathematical operations. We have enabled core dumps in `/app/cores/`. 
2. The Node.js API is not successfully communicating with the Redis queue, and the C++ worker is listening on the wrong queue channel.

Your task is to:
1. Diagnose and fix the C++ worker. The source code is located at `/app/worker/math_worker.cpp`. It implements a custom polynomial hashing algorithm. You must analyze the core dump, fix the memory corruption or logic error, and ensure it produces exactly the same output as the slow reference oracle located at `/app/oracle/reference_worker.py`. Recompile the worker to `/app/worker/math_worker`.
2. Fix the service composition. The Node.js API (`/app/api/server.js`) needs to be configured to connect to Redis on the correct port and use the correct channel (`math_jobs`). The C++ worker must also be updated or configured to consume from the `math_jobs` channel.
3. Ensure all services are running and correctly glued together.

Verification:
- The automated system will test the end-to-end flow by submitting calculation requests to the Node.js API on port 3000 and expecting the correct mathematical results.
- The compiled `/app/worker/math_worker` binary will be tested against the reference oracle using fuzz equivalence with thousands of random inputs to ensure bit-exact output.