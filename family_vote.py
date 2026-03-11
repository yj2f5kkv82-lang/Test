#!/usr/bin/env python3
"""Family dinner vote CLI tool."""

import json
import sys
import os

VOTE_FILE = "/home/user/Test/vote.json"
MAX_BAR_WIDTH = 30

# ANSI colour codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"


def load_vote():
    """Load vote data from JSON file, or return None if not found."""
    if not os.path.exists(VOTE_FILE):
        return None
    with open(VOTE_FILE, "r") as f:
        return json.load(f)


def save_vote(data):
    """Save vote data to JSON file."""
    with open(VOTE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def cmd_new(options):
    """Start a new vote with the given meal options."""
    if len(options) < 2:
        print(f"{RED}Error:{RESET} Please provide at least 2 meal options.")
        sys.exit(1)
    if len(options) > 4:
        print(f"{RED}Error:{RESET} Please provide at most 4 meal options.")
        sys.exit(1)

    # Check for duplicate options (case-insensitive)
    lower_opts = [o.lower() for o in options]
    if len(lower_opts) != len(set(lower_opts)):
        print(f"{RED}Error:{RESET} Duplicate meal options are not allowed.")
        sys.exit(1)

    data = {
        "options": options,
        "votes": {}  # name -> option index (1-based)
    }
    save_vote(data)

    print(f"{BOLD}New vote started!{RESET}")
    print(f"Meal options:")
    for i, opt in enumerate(options, 1):
        print(f"  {CYAN}{i}.{RESET} {opt}")
    print(f"\nCast votes with: python family_vote.py vote \"<name>\" <number>")


def cmd_vote(name, choice_str):
    """Cast a vote for a family member."""
    data = load_vote()
    if data is None:
        print(f"{RED}Error:{RESET} No active vote. Start one with: python family_vote.py new \"<option1>\" \"<option2>\" ...")
        sys.exit(1)

    try:
        choice = int(choice_str)
    except ValueError:
        print(f"{RED}Error:{RESET} Choice must be a number, got: {choice_str!r}")
        sys.exit(1)

    num_options = len(data["options"])
    if choice < 1 or choice > num_options:
        print(f"{RED}Error:{RESET} Choice must be between 1 and {num_options}.")
        sys.exit(1)

    # Overwrite if already voted
    existing = data["votes"].get(name)
    if existing is not None:
        old_meal = data["options"][existing - 1]
        new_meal = data["options"][choice - 1]
        print(f"{YELLOW}Note:{RESET} {name} already voted for \"{old_meal}\". Changing vote to \"{new_meal}\".")
    else:
        meal = data["options"][choice - 1]
        print(f"{CYAN}{name}{RESET} voted for {BOLD}\"{data['options'][choice - 1]}\"{RESET}.")

    data["votes"][name] = choice
    save_vote(data)


def cmd_results():
    """Show current vote standings as a bar chart."""
    data = load_vote()
    if data is None:
        print(f"{RED}Error:{RESET} No active vote. Start one with: python family_vote.py new \"<option1>\" \"<option2>\" ...")
        sys.exit(1)

    options = data["options"]
    votes = data["votes"]
    num_voters = len(votes)

    # Count votes per option (1-based index)
    counts = [0] * len(options)
    for _, choice in votes.items():
        counts[choice - 1] += 1

    total_votes = sum(counts)
    max_count = max(counts) if total_votes > 0 else 0

    # Determine winner
    # A winner is declared if:
    # 1. All family members have voted AND there's a single leader (not a tie), OR
    # 2. One option has strict majority (>50% of total votes cast so far) and leads uniquely
    winner_idx = None

    if total_votes > 0:
        leaders = [i for i, c in enumerate(counts) if c == max_count]
        majority_threshold = total_votes / 2  # strictly more than half

        if len(leaders) == 1 and counts[leaders[0]] > majority_threshold:
            winner_idx = leaders[0]

    print(f"\n{BOLD}=== Dinner Vote Results ==={RESET}")
    print(f"{DIM}Total votes cast: {total_votes}{RESET}\n")

    if total_votes == 0:
        print(f"{DIM}No votes have been cast yet.{RESET}\n")
        for opt in options:
            label = f"{CYAN}{opt:<20}{RESET}"
            print(f"  {label}  {DIM}[no votes]{RESET}")
        print()
        return

    # Determine bar scaling
    # max_count maps to MAX_BAR_WIDTH blocks
    for i, opt in enumerate(options):
        count = counts[i]
        is_winner = (i == winner_idx)

        if max_count > 0:
            bar_len = round((count / max_count) * MAX_BAR_WIDTH)
        else:
            bar_len = 0

        bar = "█" * bar_len
        empty = " " * (MAX_BAR_WIDTH - bar_len)

        if is_winner:
            label = f"{GREEN}{BOLD}{opt:<20}{RESET}"
            bar_str = f"{YELLOW}{BOLD}{bar}{RESET}{empty}"
            count_str = f"{GREEN}{BOLD}{count} vote{'s' if count != 1 else ''}{RESET}"
            marker = f"  {GREEN}{BOLD}<-- WINNER{RESET}"
        else:
            label = f"{CYAN}{opt:<20}{RESET}"
            bar_str = f"{YELLOW}{bar}{RESET}{empty}"
            count_str = f"{count} vote{'s' if count != 1 else ''}"
            marker = ""

        print(f"  {label}  [{bar_str}]  {count_str}{marker}")

    print()

    # Status messages
    leaders = [i for i, c in enumerate(counts) if c == max_count]

    if winner_idx is not None:
        meal = options[winner_idx]
        print(f"{GREEN}{BOLD}Winner declared: {meal}!{RESET}")
    elif len(leaders) > 1:
        tied_meals = ", ".join(f'"{options[i]}"' for i in leaders)
        print(f"{YELLOW}It's a tie between: {tied_meals}{RESET}")
        print(f"{DIM}More votes needed to break the tie.{RESET}")
    else:
        leading = options[leaders[0]]
        print(f"{CYAN}\"{leading}\" is currently in the lead.{RESET}")
        print(f"{DIM}No majority yet — keep voting!{RESET}")

    print()


def cmd_reset():
    """Clear the current vote."""
    if not os.path.exists(VOTE_FILE):
        print(f"{YELLOW}No active vote to reset.{RESET}")
        return

    os.remove(VOTE_FILE)
    print(f"{BOLD}Vote has been reset.{RESET}")


def print_usage():
    print(f"""
{BOLD}Family Dinner Vote{RESET}

Usage:
  python family_vote.py new "<option1>" "<option2>" [..."<option4>"]
      Start a new vote with 2-4 meal options.

  python family_vote.py vote "<name>" <number>
      Cast a vote (number corresponds to option from the list).

  python family_vote.py results
      Show current standings as a bar chart.

  python family_vote.py reset
      Clear the current vote.
""")


def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        sys.exit(0)

    command = args[0].lower()

    if command == "new":
        options = args[1:]
        cmd_new(options)

    elif command == "vote":
        if len(args) < 3:
            print(f"{RED}Error:{RESET} Usage: python family_vote.py vote \"<name>\" <number>")
            sys.exit(1)
        name = args[1]
        choice_str = args[2]
        cmd_vote(name, choice_str)

    elif command == "results":
        cmd_results()

    elif command == "reset":
        cmd_reset()

    else:
        print(f"{RED}Error:{RESET} Unknown command: {command!r}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
