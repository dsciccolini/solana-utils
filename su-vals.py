import subprocess
import sys
import json

def lamports_to_sol(lamports):
    return lamports / 1_000_000_000 if isinstance(lamports, (int, float)) else lamports

def format_sol(amount):
    return f"{amount:,.2f} SOL"

def format_percentage(value):
    return f"{value:.2f}%" if isinstance(value, (int, float)) else "N/A"

def get_validators_data(url, validator_address):
    """Fetch Solana validators data in JSON format and filter for the given validator."""
    try:
        result = subprocess.check_output(["solana", "validators", "--url", url, "--output", "json", "--sort", "credits"], text=True)
        data = json.loads(result)

        # Convert stake values to SOL
        total_active_stake = lamports_to_sol(data.get('totalActiveStake', 0))
        total_current_stake = lamports_to_sol(data.get('totalCurrentStake', 0))
        total_delinquent_stake = lamports_to_sol(data.get('totalDelinquentStake', 0))

	# Print Header
        print(f"\n\033[1;36mSolana Validators | Cluster: {url}\033[0m")

        # Print Cluster Summary
        print(f"\n\033[92mCluster Summary\033[0m")
        print(f"{'Total Active Stake:':<50} {format_sol(total_active_stake)}")
        print(f"{'Total Current Stake:':<50} {format_sol(total_current_stake)}")
        print(f"{'Total Delinquent Stake:':<50} {format_sol(total_delinquent_stake)}")
        print(f"{'Average Skip Rate:':<50} {format_percentage(data.get('averageSkipRate', 'N/A'))}")
        print(f"{'Average Stake-Weighted Skip Rate:':<50} {format_percentage(data.get('averageStakeWeightedSkipRate', 'N/A'))}\n")

        # Compute total counts for percentage calculations
        stake_by_version = data.get("stakeByVersion", {})
        total_validators = sum(v.get('currentValidators', 0) for v in stake_by_version.values())
        total_active_stake = sum(lamports_to_sol(v.get('currentActiveStake', 0)) for v in stake_by_version.values())

        # Sort versions by validator count (descending)
        sorted_versions = sorted(stake_by_version.items(), key=lambda x: x[1].get('currentValidators', 0), reverse=True)

        # Print Version Summary
        print("\033[92mVersion Summary\033[0m")
        print(f"{'Version':<15} {'Validator Count (%)':<25} {'Active Stake (%)':>30}")
        sum_validators = 0
        sum_validator_percent = 0.0
        sum_active_stake = 0.0
        sum_active_stake_percent = 0.0

        for version, stats in sorted_versions:
            validator_count = stats.get('currentValidators', 0)
            active_stake = lamports_to_sol(stats.get('currentActiveStake', 0))
            validator_percent = (validator_count / total_validators * 100) if total_validators else 0
            active_stake_percent = (active_stake / total_active_stake * 100) if total_active_stake else 0

            sum_validators += validator_count
            sum_validator_percent += validator_percent
            sum_active_stake += active_stake
            sum_active_stake_percent += active_stake_percent

            print(f"{version:<15} {validator_count:>6} ({validator_percent:>6.2f}%) {format_sol(active_stake):>30} ({active_stake_percent:>6.2f}%)")

        # Print the totals
        print(f"{'Total':<15} {sum_validators:>6} ({sum_validator_percent:>6.2f}%) {format_sol(sum_active_stake):>30} ({sum_active_stake_percent:>6.2f}%)")

        # Print Validator Summary
        print("\n\033[92mValidator Summary\033[0m")
        for validator in data.get("validators", []):
            if validator.get("identityPubkey") == validator_address:
                print(f"{'Identity Account:':<30} {validator.get('identityPubkey', 'N/A')}")
                print(f"{'Vote Account:':<30} {validator.get('voteAccountPubkey', 'N/A')}")
                print(f"{'Version:':<30} {validator.get('version', 'N/A')}")
                print(f"{'Active Stake:':<30} {format_sol(lamports_to_sol(validator.get('activatedStake', 0)))}")
                print(f"{'Commission:':<30} {format_percentage(validator.get('commission', 0))}")
                print(f"{'Last Vote:':<30} {validator.get('lastVote', 'N/A')}")
                print(f"{'Root Slot:':<30} {validator.get('rootSlot', 'N/A')}")
                print(f"{'Total Vote Credits:':<30} {validator.get('credits', 'N/A')}")
                print(f"{'Epoch Vote Credits:':<30} {validator.get('epochCredits', 'N/A')}")
                print(f"{'Skip Rate:':<30} {format_percentage(validator.get('skipRate', 0))}")
                print(f"{'Delinquent:':<30} {validator.get('delinquent', 'N/A')}")
                return

        print("Validator not found in validator data.")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch Solana validators data.")
    except json.JSONDecodeError:
        print("Error: Unable to parse validators data.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 su-validators.py <url> <validator_address>")
        sys.exit(1)

    url = sys.argv[1]
    validator_address = sys.argv[2]
    get_validators_data(url, validator_address)
