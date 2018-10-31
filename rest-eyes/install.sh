set -eu

TIMER_FILE=/etc/systemd/system/rest-eyes.timer
SERVICE_FILE=/etc/systemd/system/rest-eyes.service

echo "Installing python dependencies"
pip3 install --user notify2

echo "Installing $TIMER_FILE..."
tmp_timer=$(mktemp)
cat <<EOF > $tmp_timer
[Unit]
Description=Shows a notification every 20m to rest your eyes

[Timer]
OnUnitActiveSec=20m
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "Installing $SERVICE_FILE..."
tmp_service=$(mktemp)
sudo cat <<EOF > $tmp_service
[Unit]
Description=Shows a notification every 20m to rest your eyes

[Service]
Type=simple
User=$USER
Environment="DISPLAY=$DISPLAY" "DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS"
ExecStart=$PWD/notify.py

[Install]
WantedBy=rest-eyes.timer
EOF

echo "Enabling and starting rest-eyes daemon..."
sudo mv $tmp_timer "$TIMER_FILE"
sudo mv $tmp_service "$SERVICE_FILE"
sudo systemctl daemon-reload
sudo systemctl enable rest-eyes.timer
sudo systemctl start rest-eyes.timer
