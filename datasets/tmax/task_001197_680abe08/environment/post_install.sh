apt-get update && apt-get install -y python3 python3-pip nginx golang curl lftp cron
    pip3 install pytest pyftpdlib

    # Setup FTP directory and initial data
    mkdir -p /tmp/ftp_data/data
    cat << 'EOF' > /tmp/ftp_data/data/initial.csv
TransactionID,Category,Amount,Notes
1,Retail,100,Normal transaction
2,Food,50,"Lunch with
newlines"
3,Retail,200,Another transaction
EOF

    # Create user
    useradd -m -s /bin/bash user || true

    # Permissions
    chmod -R 777 /tmp/ftp_data
    chmod -R 777 /home/user