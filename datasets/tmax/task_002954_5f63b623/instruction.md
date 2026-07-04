You are a Linux Systems Engineer responsible for hardening a staged deployment system and optimizing our network routing configuration based on historical reliability data.

We have a dashboard recording of node statuses during our last stress test, located at `/app/traffic_monitor.mp4`. The video is exactly 60 seconds long at 1 frame per second (60 frames total). 
The video displays the status of 3 deployment nodes as three equal horizontal bands of color spanning the entire width of the video:
- Top band (0-33% height): Node 1
- Middle band (33-66% height): Node 2
- Bottom band (66-100% height): Node 3

When a node is online, its band is pure green (RGB: 0, 255, 0). When a node is offline, its band is pure red (RGB: 255, 0, 0). 

Your task consists of three parts:
1. **Analyze the Dashboard Video:** Use `ffmpeg` and ImageMagick (`convert`) or other standard CLI tools to extract the frames and count the exact number of frames each node was "online" (green). 
2. **Generate Routing Configuration:** Write a bash script `/home/user/generate_routes.sh` that produces a routing configuration file at `/home/user/routing.conf`. The config must contain exactly one line formatted as follows:
   `route_weights node1=0.XXX node2=0.YYY node3=0.ZZZ`
   The weights (0.XXX, etc.) must be the proportion of online frames for each node relative to the total online frames across all three nodes, rounded to three decimal places. For example, if Node 1 was online 10 frames, Node 2 for 20, and Node 3 for 10 (Total 40), Node 1's weight is 0.250.
3. **Mock User Deployment Groups:** We are migrating our user access to a staged deployment model. Read the CSV file `/app/team.csv` (Format: `username,team_name`). Create a simulated group file at `/home/user/group_mock` where each team is a group (format: `team_name:x:GID:user1,user2`), starting GIDs at 2000. Create a simulated `/home/user/passwd_mock` assigning each user to their respective primary GID (UIDs starting at 3000, shell `/bin/bash`, home directory `/home/username`).

Execute your steps to produce the final `/home/user/routing.conf`, `/home/user/group_mock`, and `/home/user/passwd_mock` files.