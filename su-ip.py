import subprocess
import sys
import json
import ipinfo

access_token = '118ed2d59487de'
handler = ipinfo.getHandler(access_token)

def get_ip_data(url, validator_address):
    """Fetch IP data in JSON format and print IP info."""
    try:
        result = subprocess.check_output(["solana", "gossip", "--url", url, "--output", "json"], text=True)
        gossip_data = json.loads(result)

        for node in gossip_data:
            if node.get("identityPubkey") == validator_address:
                ip_address = node.get('ipAddress', 'N/A')
                details = handler.getDetails(ip_address)
                print(f"\n\033[1;36mTHW-Utils v0 | IP Info | Cluster: {url}\033[0m\n")
                print(f"{'IP Address:':<15} {ip_address}")
                print(f"{'ASN:':<15} {details.asn}")
                print(f"{'Hostname:':<15} {details.hostname}")
                print(f"{'Organization:':<15} {details.org}")
                print(f"{'City:':<15} {details.city}")
                print(f"{'Region:':<15} {details.region}")
                print(f"{'Country:':<15} {details.country}")
                print(f"{'Location:':<15} {details.loc}")
                return

        print("Validator not found in gossip data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch IP data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse gossip data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-ip.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_ip_data(url, validator_address)