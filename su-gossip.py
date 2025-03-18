import subprocess
import sys
import json

def get_gossip_data(url, validator_address):
    """Fetch Solana gossip data in JSON format and filter for the given validator."""
    try:
        result = subprocess.check_output(["solana", "gossip", "--url", url, "--output", "json"], text=True)
        gossip_data = json.loads(result)

        for node in gossip_data:
            if node.get("identityPubkey") == validator_address:
                print(f"\n\033[1;36mSolana Gossip | Cluster: {url}\033[0m\n")
                print(f"{'IP Address:':<15} {node.get('ipAddress', 'N/A')}")
                print(f"{'Identity:':<15} {node.get('identityPubkey', 'N/A')}")
                print(f"{'Gossip:':<15} {node.get('gossipPort', 'N/A')}")
                print(f"{'TPU:':<15} {node.get('tpuPort', 'N/A')}")
                print(f"{'TPU-QUIC:':<15} {node.get('tpuQuicPort', 'N/A')}")
                print(f"{'RPC Address:':<15} {node.get('rpcHost', 'N/A')}")
                print(f"{'Sub Host:':<15} {node.get('pubsubHost', 'N/A')}")
                print(f"{'Version:':<15} {node.get('version', 'N/A')}")
                print(f"{'Feature Set:':<15} {node.get('featureSet', 'N/A')}")
                return

        print("Validator not found in gossip data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch Solana gossip data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse gossip data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-gossip.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_gossip_data(url, validator_address)
