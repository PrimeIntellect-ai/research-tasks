I need a quick testing utility to validate our rate-limiting system by analyzing serialized log data. 

I have a JSON file located at `/home/user/access_log.json` containing a list of request events. Each event is a dictionary with two keys: `"user"` (a string representing the user ID) and `"time"` (an integer representing the epoch timestamp of the request).

Your task is to write a Python script at `/home/user/check_rate.py` that parses this JSON file and acts as a state machine to evaluate the request history for each user. You need to identify any user who has violated our rate limit policy.

The rate limit policy is: **A user is allowed a maximum of 4 requests within any 10-second sliding window.** This means if a user makes 5 or more requests such that the time difference between the first and the last request in that subset is 10 seconds or less, they have violated the policy.

The script should output the IDs of all users who violated this policy to a file named `/home/user/blocked_users.txt`. 
The user IDs in `/home/user/blocked_users.txt` must be written one per line, and they must be sorted alphabetically.

Write the script, execute it, and ensure `/home/user/blocked_users.txt` is created with the correct format.