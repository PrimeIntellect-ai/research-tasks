You are a site administrator managing a multi-tenant environment. We've had a severe network misconfiguration causing some users' isolated network namespaces to lose connectivity, preventing their services from communicating. The monitoring team captured a video of the status dashboard during the incident, located at `/app/dashboard_traffic.mp4`. 

The video displays a 4x4 grid representing 16 user accounts (User00 in the top-left, reading left-to-right, top-to-bottom, ending with User15 in the bottom-right). During the video, the status squares for users who experienced network isolation turn from green to solid red for several seconds. 

Your task is to:
1. Write a Python script using OpenCV (`cv2`) and NumPy to programmatically analyze `/app/dashboard_traffic.mp4` and extract the list of User IDs that experienced the outage.
2. We have a configuration file at `/home/user/network_configs.json` containing the current network definitions for all 16 users. The isolated users were mistakenly assigned to a conflicting subnet. 
3. Write an idempotent Python script that reads `/home/user/network_configs.json`, updates the `subnet` field for the affected users to `10.1.0.0/24`, and saves the updated JSON configuration to `/home/user/fixed_network.json`. Unaffected users must remain unchanged.

Your final output file must be located at `/home/user/fixed_network.json`. An automated test will evaluate the correctness of the fixed network definitions using a quantitative metric threshold based on the exact users that needed modification.