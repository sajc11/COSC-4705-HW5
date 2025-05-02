import os
import pandas as pd
import numpy as np
from scapy.all import rdpcap
from tqdm import tqdm

# === CONFIG ===
PCAP_DIR = "./data/pcaps/"  # Change this to your actual pcap folder if needed
OUTPUT_CSV = "./output/stats.csv"
GUARD_IP = "138.201.121.103"  # Replace with your Guard Relay IP as a string

def extract_features(pcap_path):
    try:
        packets = rdpcap(pcap_path)
    except Exception as e:
        print(f"[!] Failed to read {pcap_path}: {e}")
        return [0]*10

    timestamps_up, sizes_up = [], []
    timestamps_down, sizes_down = [], []

    for pkt in packets:
        if pkt.haslayer("IP"):
            ip = pkt["IP"]
            src_ip = ip.src
            dst_ip = ip.dst

            if src_ip == GUARD_IP:
                timestamps_down.append(float(pkt.time))
                sizes_down.append(len(pkt))
            elif dst_ip == GUARD_IP:
                timestamps_up.append(float(pkt.time))
                sizes_up.append(len(pkt))

    def compute_stats(timestamps, sizes):
        if len(timestamps) < 2:
            return [0, 0, 0, 0, 0]
        inter = np.diff(sorted(timestamps))
        return [
            len(sizes),
            sum(sizes),
            np.mean(inter),
            np.median(inter),
            np.std(inter)
        ]

    up_stats = compute_stats(timestamps_up, sizes_up)
    down_stats = compute_stats(timestamps_down, sizes_down)
    return up_stats + down_stats

def main():
    rows = []
    for fname in tqdm(sorted(os.listdir(PCAP_DIR))):
        if not fname.endswith(".pcap"):
            continue
        label = fname.split("-")[0]
        fpath = os.path.join(PCAP_DIR, fname)
        features = extract_features(fpath)
        rows.append([fname, label] + features)

    columns = ["file", "label",
               "up_count", "up_bytes", "up_mean", "up_median", "up_std",
               "down_count", "down_bytes", "down_mean", "down_median", "down_std"]
    
    df = pd.DataFrame(rows, columns=columns)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[✓] Saved features to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
