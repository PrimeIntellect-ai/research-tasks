You are a network security engineer investigating targeted attacks against an internal web application. The application stack consists of Nginx, a Flask web service, and a Redis backend. 

Your objectives are to analyze the threat, build a protective filter, and secure the application stack.

**Phase 1: Vulnerability and Payload Analysis**
We captured a compiled Python dropper at `/app/dropper.pyc`. Reverse engineer this file to understand how the attacker is encoding their payloads and what exploit signatures they are using. The payloads utilize a custom encoding scheme involving cryptographic hashing and XOR obfuscation.

**Phase 2: Build a Python WAF Service**
Write a Python web service at `/home/user/waf_service.py` that listens on `127.0.0.1:9000`. 
This service must act as an authorization endpoint. It should:
1. Accept HTTP POST requests containing the incoming application traffic.
2. Decode the payloads using the logic you reverse-engineered.
3. Validate the cryptographic checksum.
4. Inspect the decoded payload for the exploit signatures.
5. Return HTTP `200 OK` for benign payloads and HTTP `403 Forbidden` for malicious ones.

**Phase 3: Multi-Service Integration**
The application stack can be started via `/app/testbed/start.sh`.
1. Modify `/app/testbed/nginx.conf` to use the `auth_request` module, routing all incoming traffic on port 8080 to your WAF service on port 9000 for inspection before proxying it to the Flask app on port 5000.
2. Restart Nginx to apply the changes.

**Phase 4: Network Policy**
Currently, the Flask app (port 5000) and Redis (port 6379) are dangerously exposed. Use `iptables` to configure a firewall policy that strictly drops all traffic to ports 5000 and 6379 on all interfaces *except* the loopback interface (`lo`).

**Verification**
A verifier script at `/app/evaluate_waf.sh` will send a series of requests through Nginx on port 8080. It reads requests from an adversarial corpus (`/app/corpus/evil/`) and a benign corpus (`/app/corpus/clean/`). Your setup must block 100% of the evil corpus and allow 100% of the clean corpus. Write the results of your manual testing to `/home/user/integration_test.log`.