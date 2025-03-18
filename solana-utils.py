import subprocess
import sys
import os

def get_rpc_url(cluster):
    """Returns the primary and backup RPC URLs for a given cluster."""
    rpc_mapping = {
        "um": ["https://api.mainnet-beta.solana.com"],
        "ut": [
            "https://api.testnet.solana.com",  # Primary Testnet
            "https://multi-muddy-model.solana-testnet.quiknode.pro/3c0cfe8cff3f4aa7c0903d2602fe82cba66f2bbd/"  # Backup Testnet
        ]
    }
    return rpc_mapping.get(cluster, [])

def get_addresses(url):
    """Retrieve the public addresses from keypair files."""
    validator_keypair = os.path.expanduser("~/validator-keypair.json")
    vote_keypair = os.path.expanduser("~/vote-account-keypair.json")

    try:
        validator_address = subprocess.check_output(
            ["solana", "address", "--url", url, "-k", validator_keypair], text=True).strip()
        vote_address = subprocess.check_output(
            ["solana", "address", "--url", url, "-k", vote_keypair], text=True).strip()
        return validator_address, vote_address
    except subprocess.CalledProcessError:
        print("Error: Unable to fetch keypair addresses.")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 solana-utils.py <um|ut> <command>")
        sys.exit(1)

    cluster = sys.argv[1]
    command = sys.argv[2]
    rpc_urls = get_rpc_url(cluster)

    if not rpc_urls:
        print("Error: Invalid cluster input. Use 'um' for mainnet or 'ut' for testnet.")
        sys.exit(1)

    for url in rpc_urls:
        validator_address, vote_address = get_addresses(url)

        command_script = f"su-{command}.py"

        try:
            output = subprocess.check_output(["python3", command_script, url, validator_address], text=True)
            print(output)
            break
        except subprocess.CalledProcessError:
            print(f"Command failed on {url}, trying next RPC if available...")
    else:
        print("Error: All RPCs failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
