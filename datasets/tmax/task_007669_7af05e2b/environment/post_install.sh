apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas

    mkdir -p /home/user

    cat << 'EOF' > /home/user/sensor_logs.txt
[DEBUG] [12-Oct-2023 11:55:00 UTC] System booting up
[INFO] [12-Oct-2023 12:02:30 UTC] Thermal probe reported temp: 40.5C in Zone 1
[INFO] [12-Oct-2023 12:08:15 UTC] Thermal probe reported temp: 41.5C in Zone 1
[WARN] [12-Oct-2023 12:09:59 UTC] Fan speed increased
[INFO] [12-Oct-2023 12:15:00 UTC] Thermal probe reported temp: 45.0C in Zone 1
[INFO] [12-Oct-2023 12:18:45 UTC] Thermal probe reported temp: 45.8C in Zone 1
[ERROR] [12-Oct-2023 12:25:00 UTC] Network timeout
[INFO] [12-Oct-2023 12:35:10 UTC] Thermal probe reported temp: 38.0C in Zone 1
EOF

    cat << 'EOF' > /home/user/server_load.csv
timestamp,load_percentage
1697112100,50.0
1697112400,60.0
1697112650,80.0
1697113000,85.0
1697113300,90.0
1697114100,40.0
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user