As a container specialist managing a lightweight custom microservices load balancer, you need to implement a fast dynamic routing script. 

The networking team has finalized the new routing policy, but they only provided a screenshot of the documentation, which I have placed on the server at `/app/policy.png`.

Your task is to:
1. Extract the routing rules from the image located at `/app/policy.png` (you can use `tesseract` or any other tool available).
2. Create an executable script at `/home/user/router.sh`.
3. The script must take exactly one argument: a URI path string (e.g., `/api/v1/users` or `/admin/settings`).
4. The script must output a single line containing exactly the backend port number that the URI should be routed to, based on the rules extracted from the image.
5. The matching logic should be a **simple string prefix match**. If multiple prefixes match, use the longest matching prefix. If the URI does not start with any of the defined prefixes, output the designated DEFAULT port.

Do not output any extra text, logs, or formatting. Just the port number. The script can be written in Bash, Python, or any language of your choice, as long as it handles the logic correctly and efficiently. Make sure it is executable.