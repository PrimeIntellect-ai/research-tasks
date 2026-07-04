You are a penetration tester who recently found a compromised server and an interesting artifact left behind by an attacker. 

There is an image file located at `/app/evidence.png`. This image contains handwritten text (which you can recover using Tesseract or another tool) representing the secret key for an internal service.

Your task is to build a mock authentication server in C to test a vulnerability you suspect the internal service had. The server must simulate a JWT authentication flow that improperly handles the `alg: none` vulnerability.

Requirements for the server:
1. Write a C program, compiled to `/home/user/auth_server`, that starts an HTTP server listening on `127.0.0.1:8080`.
2. The server must expose an endpoint `POST /login` that accepts form data `username` and `password`. If the username is `admin` and the password matches the text recovered from `/app/evidence.png`, it should return a 200 OK with a generic JWT token in the `Authorization` header.
3. The server must expose a protected endpoint `GET /flag`. This endpoint should check the `Authorization` header for a JWT.
4. The JWT validation must be deliberately vulnerable: if a token is presented with `{"alg":"none"}` in the header, the server must accept it without verifying the signature and return the text `ACCESS_GRANTED`.
5. The server must stay running in the background so it can be tested.

Recover the password from the image, build the vulnerable C server, and start it.