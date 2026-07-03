You are a network engineer tasked with troubleshooting a series of recurring connectivity drops and replacing a legacy diagnostic tool with a modern Go implementation.

Please complete the following multi-stage workflow:

1. **Video Analysis (Connectivity Diagnostics):**
   You have been provided with a dashboard recording at `/app/router_led.mp4`. This video contains a sequence of frames representing the link status of a core router. A normal state is indicated by green frames, while a dropped connection is indicated by a solid red frame (pure red: RGB 255, 0, 0). 
   Use `ffmpeg` to extract the frames and analyze them. Count the total number of distinct dropped link events (a contiguous sequence of red frames counts as 1 event). Save the total count of drop events as a single integer in `/home/user/link_drops.txt`.

2. **Legacy Parser Replacement (Go & Text Processing):**
   We have a legacy compiled binary at `/app/legacy_analyzer_oracle` that takes a single line of network log text via STDIN and outputs a parsed, canonical log format to STDOUT.
   Write a Go program at `/home/user/net_analyzer.go` and compile it to `/home/user/net_analyzer`. Your Go program must replicate the exact behavior of the legacy oracle for any given input. The oracle expects inputs containing timestamps, IP addresses, and diagnostic messages, and standardizes their formatting. You can test the oracle interactively to infer its formatting rules. 

3. **Automated Router Interaction (Expect Scripting):**
   There is a simulated interactive router CLI tool located at `/app/mock_router`. 
   Write an Expect script at `/home/user/test_router.exp` that:
   - Spawns the `/app/mock_router` process.
   - Waits for the "Username:" prompt and sends "admin".
   - Waits for the "Password:" prompt and sends "neteng_secret".
   - Waits for the "Router#" prompt.
   - Sends the command "show interface status".
   - Waits for the "Router#" prompt again and sends "exit".
   Ensure the script executes cleanly and captures the interface status output.

4. **Monitoring (Scheduled Task):**
   Create a crontab file at `/home/user/monitoring_cron` that schedules your Expect script (`/home/user/test_router.exp`) to run exactly every 5 minutes. The cron expression must be standard and properly formatted.

Ensure all scripts are executable and located exactly at the specified paths.