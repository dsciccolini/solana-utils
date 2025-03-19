import subprocess
import sys
import json
import ipinfo
import pprint

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
                details_all = details.all
                pprint.pprint(details_all)  # Debug print to see the structure of details_all
                print(f"\n\033[1;36mTHW-Utils v0 | IP Info | Cluster: {url}\033[0m\n")
                print(f"{'IP Address:':<15} {ip_address}")
                
                org_info = details_all.get('org', 'N/A')
                asn, org = org_info.split(' ', 1) if ' ' in org_info else ('N/A', org_info)
                country_code = details_all.get('country', 'N/A')
                region = details_all.get('region', 'N/A')
                city = details_all.get('city', 'N/A')
                country_name = details_all.get('country_name', 'N/A')
                
                print(f"{'ASN:':<20} {asn}")
                print(f"{'Organization:':<20} {org}")
                print(f"{'City:':<20} {city}")
                print(f"{'Region:':<20} {region}")
                print(f"{'Country (Code):':<20} {country_name} ({country_code})")
                print(f"{'Location:':<20} {details_all.get('loc', 'N/A')}")
                print(f"{'VA Format:':<20} {asn}-{country_code}-{city}")
                return

        print("Validator not found in gossip data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch IP data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse gossip data.")
    except AttributeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-ip.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_ip_data(url, validator_address)