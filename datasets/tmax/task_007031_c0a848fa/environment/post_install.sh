apt-get update && apt-get install -y python3 python3-pip expect
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/legacy_monitor.py
#!/usr/bin/env python3
import sys
import getpass

def main():
    print("Legacy Monitor v1.0")
    sys.stdout.flush()
    user = input("Username: ")
    pwd = getpass.getpass("Password: ")

    if user != "admin" or pwd != "sre_pass_2024":
        print("Access denied")
        sys.exit(1)

    tz = "LOCAL"

    while True:
        try:
            print("monitor> ", end="")
            sys.stdout.flush()
            cmd = input().strip()
        except EOFError:
            break

        if cmd.startswith("set_tz "):
            tz = cmd.split(" ")[1]
            print(f"Timezone set to {tz}")
        elif cmd == "get_uptime":
            if tz != "UTC":
                print("Error: Uptime can only be reliably calculated in UTC timezone.")
            else:
                print("UPTIME_VALUE: 99.99%")
        elif cmd == "exit":
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
EOF

    chmod +x /home/user/legacy_monitor.py
    chmod -R 777 /home/user