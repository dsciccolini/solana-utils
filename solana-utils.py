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

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 solana-utils.py <um|ut> <validator_address> <command>")
        sys.exit(1)

    cluster = sys.argv[1]
    validator_address = sys.argv[2]
    command = sys.argv[3]
    rpc_urls = get_rpc_url(cluster)

    if not rpc_urls:
        print("Error: Invalid cluster input. Use 'um' for mainnet or 'ut' for testnet.")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for url in rpc_urls:
        address = validator_address

        command_script = os.path.join(script_dir, f"su-{command}.py")

        try:
            output = subprocess.check_output(["python3", command_script, url, address], text=True)
            print(output)
            break
        except subprocess.CalledProcessError:
            print(f"Command failed on {url}, trying next RPC if available...")
    else:
        print("Error: All RPCs failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
