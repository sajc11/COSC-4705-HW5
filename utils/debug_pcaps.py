from scapy.all import rdpcap

# Load a test .pcap - can replace with any pcap file we want to test
packets = rdpcap("./data/pcaps/amazon-train1.pcap")

# Inspect the first few packets
for pkt in packets[:5]:
    print(pkt.summary())
    if pkt.haslayer("IP"):
        print("IP:", pkt["IP"].src, "→", pkt["IP"].dst)