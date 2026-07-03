apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/cron.log
2023-10-27T03:00:05Z cron-cleanup INFO: Starting daily cleanup tasks.
2023-10-27T03:01:12Z cron-cleanup INFO: Scanning for old config files.
2023-10-27T03:01:15Z cron-cleanup WARNING: Deleted /home/user/config.json.
2023-10-27T03:01:20Z cron-cleanup INFO: Cleanup tasks finished.
EOF

    cat << 'EOF' > /home/user/payment.log
2023-10-27T03:00:00Z payment-service INFO: Starting service.
2023-10-27T03:00:01Z payment-service INFO: Loaded config from /home/user/config.json.
2023-10-27T03:01:16Z payment-service ERROR: Config file not found during dynamic reload.
2023-10-27T03:01:18Z payment-service CRITICAL: Segmentation fault. Process terminated.
EOF

    cat << 'EOF' > /home/user/crash.log
Fatal Python error: Segmentation fault

Current thread 0x00007f8b9c123456 (most recent call first):
  File "/home/user/payment.py", line 42 in process_payment
  File "/home/user/payment.py", line 85 in run_loop
  File "/home/user/payment.py", line 102 in main
EOF

    dd if=/dev/urandom of=/home/user/memory_dump.bin bs=1K count=10 status=none
    echo -n "API_KEY_SECRET=sk_live_9a8b7c6d5e4f3g2h1i0j" >> /home/user/memory_dump.bin
    dd if=/dev/urandom bs=1K count=10 status=none >> /home/user/memory_dump.bin

    chmod -R 777 /home/user