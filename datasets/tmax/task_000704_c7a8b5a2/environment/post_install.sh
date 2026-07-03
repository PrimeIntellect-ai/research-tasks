apt-get update && apt-get install -y python3 python3-pip netcat-openbsd gawk sed coreutils
    pip3 install pytest

    # Create directories
    mkdir -p /home/user/corpora/clean/ /home/user/corpora/evil/ /home/user/corpora/evil_golden/ /app/services/

    # Create clean corpus
    cat << 'EOF' > /home/user/corpora/clean/test1.log
2023-10-12T10:05:00Z|10.0.0.1|Alice|Hello world
2023-10-12T10:05:01Z|10.0.0.2|Bob|All good here
2023-10-12T10:05:02Z|10.0.0.1|Alice|Status update
EOF

    # Create evil corpus
    cat << 'EOF' > /home/user/corpora/evil/test1.log
2023-10-12T10:05:00|10.0.0.3|C​harlie|My SSN is 123-45-6789
2023-10-12T10:05:01Z|10.0.0.4|Dave|Hello
2023-10-12T10:05:02Z|10.0.0.4|Dave|Spam 1
2023-10-12T10:05:03Z|10.0.0.4|Dave|Spam 2
2023-10-12T10:05:04Z|10.0.0.4|Dave|Spam 3
2023-10-12T10:05:05Z|10.0.0.4|Dave|Spam 4
EOF

    # Create evil_golden corpus
    cat << 'EOF' > /home/user/corpora/evil_golden/test1.log
2023-10-12T10:05:00Z|10.0.0.3|Charlie|My SSN is ***-**-****
2023-10-12T10:05:01Z|10.0.0.4|Dave|Hello
2023-10-12T10:05:02Z|10.0.0.4|Dave|Spam 1
2023-10-12T10:05:03Z|10.0.0.4|Dave|Spam 2
EOF

    # Create services
    cat << 'EOF' > /app/services/receiver.sh
#!/bin/bash
nc -l -p 9090
EOF

    cat << 'EOF' > /app/services/aggregator.sh
#!/bin/bash
cat > /tmp/aggregated.log
EOF

    cat << 'EOF' > /app/services/start_pipeline.sh
#!/bin/bash
./receiver.sh > /dev/null &
./aggregator.sh < /dev/null &
wait
EOF

    chmod +x /app/services/*.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app