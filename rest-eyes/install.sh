set -eu

TIMER_FILE=/etc/systemd/system/rest-eyes.timer
SERVICE_FILE=/etc/systemd/system/rest-eyes.service

echo "Installing $TIMER_FILE..."
cat <<EOF > "$TIMER_FILE"
[Unit]
Description=Shows a notification every 20m to rest your eyes

[Timer]
OnUnitActiveSec=20m
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "Installing $SERVICE_FILE..."
sudo cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Shows a notification every 20m to rest your eyes

[Service]
Type=simple
ExecStart=$HOME/scripts/rest-eyes/notify.py

[Install]
WantedBy=rest-eyes.timer
EOF

echo "Enabling and starting rest-eyes daemon..."
systemctl daemon-reload
systemctl enable rest-eyes.timer
systemctl start rest-eyes.timer
