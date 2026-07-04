We have a proprietary provisioning tool located at `/app/provision_worker` (a stripped binary). This tool simulates provisioning by performing several heavy operations: it clones a Git repository, calculates some routing metrics, and processes data. Currently, it is invoked individually for every provisioning request, which is extremely slow because it initializes its state from scratch each time. 

You need to write a C++ wrapper or proxy service (to be saved at `/home/user/provision_cache_proxy.cpp` and compiled to `/home/user/provision_cache_proxy`) that significantly speeds up this workflow. 

Your tasks:
1. **Analyze the Binary**: The binary `/app/provision_worker` takes a single argument, the path to a local Git repository (e.g., `/home/user/repo`). Investigate its behavior. It typically takes about 2 seconds to run because of repeated initialization.
2. **Setup Git and Hooks**: Create a local bare Git repository at `/home/user/config.git`. Configure a `post-receive` hook that triggers your proxy service to update its cached configuration whenever new commits are pushed.
3. **C++ Proxy Development**: Write a C++ service that supervises the `/app/provision_worker`. It should intercept provisioning requests (simulated via TCP port 8080) and cache the results or pool the binary executions. Your C++ program should handle multiple requests concurrently.
4. **Network and Routing**: Ensure your proxy listens on `127.0.0.1:8080` and routes invalid requests to a default drop bucket. 

Your proxy must achieve a minimum speedup of 3.0x compared to running the binary sequentially for 100 requests.