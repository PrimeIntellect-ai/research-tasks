As a site administrator managing user accounts, you are tasked with fixing a provisioning script. We've been getting 502 Bad Gateway errors because our user accounts were pointing to the wrong upstream socket path, and timestamps were being logged in the wrong timezone.

A previous admin left the correct socket path and timezone text in an image file located at `/app/diagram.png`. 

Your task is to:
1. Read the correct timezone and socket path from the image at `/app/diagram.png`. (You may use OCR tools like `tesseract`).
2. Write a Go program at `/home/user/user_setup.go` and compile it to `/home/user/user_setup`.
3. The Go program must take exactly one command-line argument (a username).
4. The program must convert the provided username to ALL CAPS (simulating a text processing step).
5. The program must print exactly the following string to standard output (no trailing newline is required, but a standard newline is fine as long as it consistently formats):
`[<TIMEZONE>] Configuring <USERNAME_UPPERCASE> to use <SOCKET_PATH>`

Where `<TIMEZONE>` and `<SOCKET_PATH>` are the exact values extracted from the image.

For example, if the image contained timezone "Europe/London" and socket "/tmp/sock", and the program was invoked as `./user_setup alice`, it should print:
`[Europe/London] Configuring ALICE to use /tmp/sock`

Ensure your Go program compiles successfully and the binary is executable at `/home/user/user_setup`.