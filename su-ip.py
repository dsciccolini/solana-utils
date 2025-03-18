import subprocess
import sys
import json

def get_ip_data(url, validator_address):
    """Fetch IP data in JSON format."""
    try:
        result = subprocess.check_output(["solana", "gossip", "--url", url, "--output", "json"], text=True)
        gossip_data = json.loads(result)

        for node in gossip_data:
            if node.get("identityPubkey") == validator_address:
                ip_address = node.get('ipAddress', 'N/A')
                return ip_address
        print("Validator not found in gossip data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch IP data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-ip.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    ip_address = get_ip_data(url, validator_address)
    if ip_address:
        print(f"IP Address: {ip_address}")