import subprocess
import sys
import json

def get_leader_schedule(url, validator_address):
    """Fetch Solana leader schedule data in JSON format and filter for the given validator."""
    try:
        result = subprocess.check_output(["solana", "leader-schedule", "--url", url, "--output", "json"], text=True)
        data = json.loads(result)

        leader_slots = [entry['slot'] for entry in data.get("leaderScheduleEntries", []) if entry.get("leader") == validator_address]
        total_leader_slots = len(leader_slots)
        print(f"\n\033[1;36mSolana Leader Schedule | Cluster: {url}\033[0m\n")
        print(f"\033[1;32mIdentity: {validator_address}\033[0m\n")
        print("\033[1;32mLeader Slots:\033[0m")
        for slot in leader_slots:
            print(f"{slot}")
        print(f"\n\033[1;32mTotal Leader Slots: {total_leader_slots}\033[0m")

    except subprocess.CalledProcessError:
        print("Error: Failed to fetch Solana leader schedule data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse leader schedule data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-leader.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_leader_schedule(url, validator_address)
