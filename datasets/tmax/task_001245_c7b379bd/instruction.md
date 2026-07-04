You are a FinOps analyst tasked with recovering and re-implementing a custom cost-aware reverse proxy script that dynamically routes requests to the cheapest cloud zones.

Unfortunately, the original documentation was lost. All we have is a dashboard screen recording located at `/app/cost_demo.mp4`. This video captures the deployment terminal exactly when the original developer exported three critical environment variables: `ZONE_A_BASE`, `ZONE_B_BASE`, and `ZONE_C_BASE`.

Here are your tasks:

1. **Extract Environment Variables:** 
   Analyze the video `/app/cost_demo.mp4` (you may use `ffmpeg` or any suitable tool to extract frames). Find the three integer values assigned to the zone base variables. Append them as standard `export` statements to `/home/user/.bash_profile`.

2. **Develop the Load Balancer Logic:**
   Create a Python script at `/home/user/lb_proxy.py`. This script serves as the decision engine for our reverse proxy.
   - It must accept exactly one command-line argument: a JSON-formatted string representing an incoming request.
   - The JSON will have the format: `{"req_id": <int>, "size_mb": <int>}`.
   - The script must read the three base variables (`ZONE_A_BASE`, `ZONE_B_BASE`, `ZONE_C_BASE`) from the environment.
   - Calculate the projected cost for each zone for the given request using these formulas:
     - Cost A = `ZONE_A_BASE` * `size_mb` + (`req_id` % 3)
     - Cost B = `ZONE_B_BASE` * `size_mb` + (`req_id` % 5)
     - Cost C = `ZONE_C_BASE` * `size_mb` + (`req_id` % 2)
   - Determine the zone with the lowest cost. In the event of a tie, prioritize Zone A over Zone B, and Zone B over Zone C.
   - Print *only* the routing decision to standard output in this exact format: `ROUTE_TO: ZONE_A` (or `ZONE_B`, `ZONE_C`).

3. **Firewall & Proxy Automation Script:**
   To prepare the environment for the actual proxy daemon (which we will deploy later), write a shell script at `/home/user/setup_proxy.sh`. When executed, this script should:
   - Source the `.bash_profile`.
   - Create a simulated firewall rules file at `/home/user/firewall_rules.txt` containing exactly three lines mimicking port forwarding (one for each zone):
     `FORWARD PORT 80 TO ZONE A COST $ZONE_A_BASE`
     `FORWARD PORT 80 TO ZONE B COST $ZONE_B_BASE`
     `FORWARD PORT 80 TO ZONE C COST $ZONE_C_BASE`
   Make sure `/home/user/setup_proxy.sh` is executable.

We will run an automated test that sources your `.bash_profile` and fuzz-tests your `/home/user/lb_proxy.py` against thousands of simulated JSON requests to ensure identical behavior to our reference oracle.