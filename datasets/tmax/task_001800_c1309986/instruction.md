You are a capacity planner and systems administrator analyzing SAN resource usage and deploying a new self-service storage allocation system.

Your task is divided into three stages:

**Stage 1: Historical Usage Analysis (Video Fixture)**
A timelapse video of our SAN monitoring dashboard is located at `/app/san_monitoring.mp4`. The video flashes a bright red indicator on the dashboard during the system's peak usage hour.
1. Extract the frames of this video using `ffmpeg` (e.g., to PPM format).
2. Write a short C program to analyze these frames and find the 1-indexed frame number that contains the maximum number of "pure red" pixels (defined strictly as Red > 200, Green < 50, Blue < 50).
3. The frame number where this peak occurs represents our `PEAK_USAGE_OFFSET`. You will need this integer for the next stage.

**Stage 2: Quota Checker Implementation (Adversarial Corpus)**
Users submit storage requests in a specific `.alloc` format:
```
USER: <username>
MOUNT: <path>
SIZE: <number_in_tb>
```
Write a C program located at `/home/user/quota_checker`. It must take a single command-line argument (the path to an `.alloc` file) and determine whether the request is valid.
Rules for a valid request:
1. `USER` must be listed exactly on a line in the ACL file `/app/acl.txt`.
2. `MOUNT` must begin with `/mnt/storage/` and must NOT contain any directory traversal (`..`).
3. `SIZE` must be less than or equal to `100 - PEAK_USAGE_OFFSET` (using the integer you found in Stage 1).

The program must exit with status `0` if the request is valid, and exit with status `1` if it violates any rule. We have provided a set of test corpora at `/app/corpora/clean/` and `/app/corpora/evil/`. Your compiled binary must accept 100% of the clean requests and reject 100% of the evil requests.

**Stage 3: Git Hook & Reverse Proxy Setup**
1. Initialize a bare git repository at `/home/user/allocations.git`.
2. Create a `pre-receive` hook in this repository that extracts the incoming `.alloc` files and runs your `/home/user/quota_checker` on them. If any file fails, the push must be rejected.
3. Configure `nginx` (which is already installed) to act as a reverse proxy on port `8080` forwarding to `git-http-backend`, allowing Git over HTTP pushes to `/home/user/allocations.git`. Ensure the `GIT_HTTP_EXPORT_ALL` and `GIT_PROJECT_ROOT` CGI variables are properly set in the Nginx config. Start the Nginx service.

Leave your compiled `quota_checker` binary at `/home/user/quota_checker`.