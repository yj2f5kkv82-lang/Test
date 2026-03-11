#!/usr/bin/env python3
"""
meal_planner.py — A CLI tool for families to plan their weekly meals.

Usage:
    python meal_planner.py set <day> "<meal>" --who "<name>"
    python meal_planner.py show
    python meal_planner.py clear <day>
"""

import argparse
import json
import os
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PLAN_FILE = "/home/user/Test/meal_plan.json"

DAYS_ORDERED = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAY_ALIASES = {d.lower(): d for d in DAYS_ORDERED}

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

RESET  = "\033[0m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
DIM    = "\033[2m"
YELLOW = "\033[33m"
RED    = "\033[31m"


def cyan(text: str) -> str:
    return f"{CYAN}{text}{RESET}"


def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


def green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


def yellow(text: str) -> str:
    return f"{YELLOW}{text}{RESET}"


def red(text: str) -> str:
    return f"{RED}{text}{RESET}"


def dim(text: str) -> str:
    return f"{DIM}{text}{RESET}"


# ---------------------------------------------------------------------------
# Plan I/O helpers
# ---------------------------------------------------------------------------

def load_plan() -> dict:
    """Load the meal plan from disk.  Returns an empty plan if file is absent."""
    if not os.path.exists(PLAN_FILE):
        return {}
    try:
        with open(PLAN_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            print(red("Warning: plan file has unexpected format — starting fresh."),
                  file=sys.stderr)
            return {}
        return data
    except json.JSONDecodeError as exc:
        print(red(f"Warning: could not parse plan file ({exc}) — starting fresh."),
              file=sys.stderr)
        return {}


def save_plan(plan: dict) -> None:
    """Persist the meal plan to disk."""
    try:
        with open(PLAN_FILE, "w", encoding="utf-8") as fh:
            json.dump(plan, fh, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(red(f"Error: could not save plan file: {exc}"), file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Day normalisation
# ---------------------------------------------------------------------------

def normalise_day(raw: str) -> str:
    """Return the canonical day abbreviation, or raise ValueError."""
    key = raw.strip().lower()
    if key not in DAY_ALIASES:
        valid = ", ".join(DAYS_ORDERED)
        raise ValueError(
            f"'{raw}' is not a recognised day.  Valid options: {valid}"
        )
    return DAY_ALIASES[key]


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_set(day_raw: str, meal: str, who: str) -> None:
    """Assign a meal (and requester) to a given day."""
    try:
        day = normalise_day(day_raw)
    except ValueError as exc:
        print(red(f"Error: {exc}"), file=sys.stderr)
        sys.exit(1)

    meal = meal.strip()
    who  = who.strip()

    if not meal:
        print(red("Error: meal name cannot be empty."), file=sys.stderr)
        sys.exit(1)
    if not who:
        print(red("Error: --who name cannot be empty."), file=sys.stderr)
        sys.exit(1)

    plan = load_plan()
    plan[day] = {"meal": meal, "who": who}
    save_plan(plan)

    print(
        f"  {cyan(day)}: {bold(meal)} "
        f"(requested by {green(who)}) — saved."
    )


def cmd_show() -> None:
    """Print the full week's plan as a formatted table."""
    plan = load_plan()

    # Column widths (minimum enforced so headers always fit)
    w_day  = max(3,  max((len(d)                        for d in DAYS_ORDERED), default=3))
    w_meal = max(4,  max((len(plan[d]["meal"])           for d in DAYS_ORDERED if d in plan), default=4))
    w_who  = max(12, max((len(plan[d]["who"])            for d in DAYS_ORDERED if d in plan), default=12))

    # Build header
    h_day  = "Day".ljust(w_day)
    h_meal = "Meal".ljust(w_meal)
    h_who  = "Requested by".ljust(w_who)

    sep = f"+-{'-' * w_day}-+-{'-' * w_meal}-+-{'-' * w_who}-+"

    header = f"| {bold(h_day)} | {bold(h_meal)} | {bold(h_who)} |"

    print()
    print(sep)
    print(header)
    print(sep)

    for day in DAYS_ORDERED:
        if day in plan:
            entry = plan[day]
            meal_val = entry.get("meal", "")
            who_val  = entry.get("who",  "")

            col_day  = cyan(day.ljust(w_day))
            col_meal = bold(meal_val.ljust(w_meal))
            col_who  = green(who_val.ljust(w_who))
        else:
            col_day  = cyan(day.ljust(w_day))
            col_meal = dim("—".ljust(w_meal))
            col_who  = dim("—".ljust(w_who))

        print(f"| {col_day} | {col_meal} | {col_who} |")

    print(sep)
    print()


def cmd_clear(day_raw: str) -> None:
    """Remove the meal entry for a given day."""
    try:
        day = normalise_day(day_raw)
    except ValueError as exc:
        print(red(f"Error: {exc}"), file=sys.stderr)
        sys.exit(1)

    plan = load_plan()

    if day not in plan:
        print(yellow(f"  {day} has no meal assigned — nothing to clear."))
        return

    del plan[day]
    save_plan(plan)
    print(f"  {cyan(day)}: meal cleared.")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meal_planner",
        description="Family weekly meal planner.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # --- set ---
    p_set = sub.add_parser("set", help="Assign a meal to a day.")
    p_set.add_argument("day",  help="Day abbreviation (Mon/Tue/…/Sun)")
    p_set.add_argument("meal", help='Meal name (quote if it contains spaces)')
    p_set.add_argument(
        "--who",
        required=True,
        metavar="NAME",
        help="Who requested this meal",
    )

    # --- show ---
    sub.add_parser("show", help="Print the full week's meal plan.")

    # --- clear ---
    p_clear = sub.add_parser("clear", help="Clear the meal for a day.")
    p_clear.add_argument("day", help="Day abbreviation (Mon/Tue/…/Sun)")

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "set":
        cmd_set(args.day, args.meal, args.who)
    elif args.command == "show":
        cmd_show()
    elif args.command == "clear":
        cmd_clear(args.day)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
