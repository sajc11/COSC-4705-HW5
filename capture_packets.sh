#!/bin/bash

# === CONFIG ===
GUARD_IP="138.201.121.103"           # Tor Guard Relay IP
INTERFACE="en0"                      # network interface - mac prefers en0...
OUTPUT_DIR="./data/pcaps"
CAPTURE_TIME=15                      # Capture duration (sec)

SITES=("google" "nytimes" "github" "youtube" "amazon" "store.steampowered")

mkdir -p "$OUTPUT_DIR"
echo "📡 Starting full auto-capture for all 30 .pcap files..."

for site in "${SITES[@]}"; do
  echo ""
  echo "🌐 === Site: $site ==="

  # 4 training files
  for i in {1..4}; do
    FNAME="${site}-train${i}.pcap"
    FILE_PATH="$OUTPUT_DIR/$FNAME"

    echo ""
    echo "📁 Preparing: $FNAME"
    echo "👉 Switch to Tor and visit: https://${site}.com (or the right domain)"
    read -p "Press ENTER to start capture..."

    # Start tcpdump
    sudo tcpdump -i "$INTERFACE" -w "$FILE_PATH" -s 100 host "$GUARD_IP" &
    PID=$!

    # Countdown
    for ((j=CAPTURE_TIME; j>0; j--)); do
      printf "\r🕒 Capturing... %2d seconds left" "$j"
      sleep 1
    done

    kill "$PID" 2>/dev/null
    wait "$PID" 2>/dev/null

    echo -e "\n✅ Saved: $FNAME"
  done

  # Test file
  FNAME="${site}-test.pcap"
  FILE_PATH="$OUTPUT_DIR/$FNAME"

  echo ""
  echo "🧪 Test file: $FNAME"
  echo "👉 Switch to Tor and visit: https://${site}.com"
  read -p "Press ENTER to start capture..."

  sudo tcpdump -i "$INTERFACE" -w "$FILE_PATH" -s 100 host "$GUARD_IP" &
  PID=$!

  for ((j=CAPTURE_TIME; j>0; j--)); do
    printf "\r🕒 Capturing test... %2d seconds left" "$j"
    sleep 1
  done

  kill "$PID" 2>/dev/null
  wait "$PID" 2>/dev/null

  echo -e "\n✅ Saved test: $FNAME"
done

echo ""
echo "All 30 captures complete!"
