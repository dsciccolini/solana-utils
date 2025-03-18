import subprocess
import sys
import json

def get_block_production_data(url, validator_address):
    """Fetch Solana block production data in JSON format and filter for the given validator."""
    try:
        result = subprocess.check_output(["solana", "block-production", "--url", url, "--output", "json"], text=True)
        data = json.loads(result)

        # Calculate Cluster Skip Rate
        total_slots = data.get('total_slots', 0)
        total_slots_skipped = data.get('total_slots_skipped', 0)
        cluster_skip_rate = (total_slots_skipped / total_slots * 100) if total_slots else 0

        # Print summary information
        print(f"\n\033[1;36mSolana Block Production | Cluster: {url}\033[0m\n")
        print(f"{'Epoch:':<25} {data.get('epoch', 'N/A')}")
        print(f"{'Start Slot:':<25} {data.get('start_slot', 'N/A')}")
        print(f"{'End Slot:':<25} {data.get('end_slot', 'N/A')}")
        print(f"{'Total Slots:':<25} {total_slots}")
        print(f"{'Total Blocks Produced:':<25} {data.get('total_blocks_produced', 'N/A')}")
        print(f"{'Total Skipped Slots:':<25} {total_slots_skipped}")
        print(f"{'Cluster Skip Rate:':<25} {cluster_skip_rate:.2f}%\n")

        # Search for the validator's data
        for leader in data.get("leaders", []):
            if leader.get("identityPubkey") == validator_address:
                leader_slots = leader.get('leaderSlots', 0)
                skipped_slots = leader.get('skippedSlots', 0)
                validator_skip_rate = (skipped_slots / leader_slots * 100) if leader_slots else 0

                print(f"{'Identity:':<25} {leader.get('identityPubkey', 'N/A')}")
                print(f"{'Leader Slots:':<25} {leader_slots}")
                print(f"{'Blocks Produced:':<25} {leader.get('blocksProduced', 'N/A')}")
                print(f"{'Skipped Slots:':<25} {skipped_slots}")
                print(f"{'Skip Rate:':<25} {validator_skip_rate:.2f}%")
                return

        print("Validator not found in block production data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch Solana block production data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse block production data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-blocks.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_block_production_data(url, validator_address)
