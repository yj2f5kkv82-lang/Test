#!/usr/bin/env python3
"""
shopping_list.py — Generate a shopping list from a family meal plan.
"""

import json
import sys
import os
import argparse
from collections import defaultdict

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
YELLOW = "\033[33m"
GREEN  = "\033[32m"

def yellow_bold(text: str) -> str:
    return f"{BOLD}{YELLOW}{text}{RESET}"

def green_check(text: str) -> str:
    return f"{GREEN}✔ {text}{RESET}"

# ── Ingredient database ───────────────────────────────────────────────────────
# Each meal maps to a list of (ingredient, quantity, category) tuples.
# Categories: Produce, Meat, Dairy, Pantry, Other
INGREDIENT_DB: dict[str, list[tuple[str, str, str]]] = {
    "spaghetti bolognese": [
        ("spaghetti",          "400 g",   "Pantry"),
        ("beef mince",         "500 g",   "Meat"),
        ("tinned tomatoes",    "2 cans",  "Pantry"),
        ("onion",              "1 large", "Produce"),
        ("garlic",             "3 cloves","Produce"),
        ("carrot",             "1",       "Produce"),
        ("celery",             "2 stalks","Produce"),
        ("tomato paste",       "2 tbsp",  "Pantry"),
        ("olive oil",          "2 tbsp",  "Pantry"),
        ("parmesan",           "50 g",    "Dairy"),
        ("red wine",           "100 ml",  "Other"),
    ],
    "roast chicken": [
        ("whole chicken",      "1.8 kg",  "Meat"),
        ("potatoes",           "800 g",   "Produce"),
        ("garlic",             "1 head",  "Produce"),
        ("lemon",              "1",       "Produce"),
        ("rosemary",           "3 sprigs","Produce"),
        ("thyme",              "3 sprigs","Produce"),
        ("olive oil",          "3 tbsp",  "Pantry"),
        ("butter",             "50 g",    "Dairy"),
    ],
    "fish tacos": [
        ("white fish fillets", "600 g",   "Meat"),
        ("corn tortillas",     "8",       "Pantry"),
        ("cabbage",            "1/4",     "Produce"),
        ("avocado",            "2",       "Produce"),
        ("lime",               "2",       "Produce"),
        ("sour cream",         "150 ml",  "Dairy"),
        ("chilli powder",      "1 tsp",   "Pantry"),
        ("cumin",              "1 tsp",   "Pantry"),
        ("coriander",          "1 bunch", "Produce"),
    ],
    "vegetable stir fry": [
        ("broccoli",           "1 head",  "Produce"),
        ("capsicum",           "2",       "Produce"),
        ("carrot",             "2",       "Produce"),
        ("snap peas",          "150 g",   "Produce"),
        ("garlic",             "3 cloves","Produce"),
        ("ginger",             "2 cm",    "Produce"),
        ("soy sauce",          "3 tbsp",  "Pantry"),
        ("sesame oil",         "1 tbsp",  "Pantry"),
        ("rice",               "300 g",   "Pantry"),
        ("vegetable oil",      "2 tbsp",  "Pantry"),
    ],
    "pizza": [
        ("pizza dough",        "1 ball",  "Pantry"),
        ("passata",            "200 ml",  "Pantry"),
        ("mozzarella",         "200 g",   "Dairy"),
        ("capsicum",           "1",       "Produce"),
        ("mushrooms",          "150 g",   "Produce"),
        ("olives",             "50 g",    "Pantry"),
        ("oregano",            "1 tsp",   "Pantry"),
        ("olive oil",          "1 tbsp",  "Pantry"),
    ],
    "lasagne": [
        ("lasagne sheets",     "250 g",   "Pantry"),
        ("beef mince",         "500 g",   "Meat"),
        ("tinned tomatoes",    "2 cans",  "Pantry"),
        ("onion",              "1",       "Produce"),
        ("garlic",             "2 cloves","Produce"),
        ("milk",               "600 ml",  "Dairy"),
        ("butter",             "60 g",    "Dairy"),
        ("plain flour",        "60 g",    "Pantry"),
        ("parmesan",           "80 g",    "Dairy"),
        ("mozzarella",         "150 g",   "Dairy"),
        ("tomato paste",       "2 tbsp",  "Pantry"),
    ],
    "chicken curry": [
        ("chicken thighs",     "700 g",   "Meat"),
        ("tinned tomatoes",    "1 can",   "Pantry"),
        ("coconut milk",       "400 ml",  "Pantry"),
        ("onion",              "1 large", "Produce"),
        ("garlic",             "3 cloves","Produce"),
        ("ginger",             "2 cm",    "Produce"),
        ("curry powder",       "2 tbsp",  "Pantry"),
        ("garam masala",       "1 tsp",   "Pantry"),
        ("rice",               "300 g",   "Pantry"),
        ("spinach",            "100 g",   "Produce"),
        ("vegetable oil",      "2 tbsp",  "Pantry"),
        ("coriander",          "1 bunch", "Produce"),
    ],
    "caesar salad": [
        ("cos lettuce",        "2 heads", "Produce"),
        ("chicken breast",     "400 g",   "Meat"),
        ("parmesan",           "60 g",    "Dairy"),
        ("bread",              "4 slices","Pantry"),
        ("bacon",              "100 g",   "Meat"),
        ("eggs",               "2",       "Dairy"),
        ("lemon",              "1",       "Produce"),
        ("garlic",             "2 cloves","Produce"),
        ("worcestershire sauce","1 tbsp", "Pantry"),
        ("dijon mustard",      "1 tsp",   "Pantry"),
        ("olive oil",          "4 tbsp",  "Pantry"),
    ],
    "beef burgers": [
        ("beef mince",         "600 g",   "Meat"),
        ("burger buns",        "4",       "Pantry"),
        ("lettuce",            "1/2 head","Produce"),
        ("tomato",             "2",       "Produce"),
        ("onion",              "1",       "Produce"),
        ("cheddar cheese",     "4 slices","Dairy"),
        ("pickles",            "8 slices","Pantry"),
        ("ketchup",            "to taste","Pantry"),
        ("mustard",            "to taste","Pantry"),
    ],
    "pasta carbonara": [
        ("spaghetti",          "400 g",   "Pantry"),
        ("bacon",              "200 g",   "Meat"),
        ("eggs",               "4",       "Dairy"),
        ("parmesan",           "80 g",    "Dairy"),
        ("garlic",             "2 cloves","Produce"),
        ("black pepper",       "to taste","Pantry"),
        ("olive oil",          "1 tbsp",  "Pantry"),
    ],
    "soup": [
        ("onion",              "1 large", "Produce"),
        ("garlic",             "2 cloves","Produce"),
        ("carrot",             "3",       "Produce"),
        ("celery",             "3 stalks","Produce"),
        ("potato",             "3",       "Produce"),
        ("vegetable stock",    "1.5 L",   "Pantry"),
        ("olive oil",          "2 tbsp",  "Pantry"),
        ("bay leaves",         "2",       "Pantry"),
        ("cream",              "100 ml",  "Dairy"),
    ],
    "omelette": [
        ("eggs",               "3",       "Dairy"),
        ("milk",               "2 tbsp",  "Dairy"),
        ("butter",             "1 tbsp",  "Dairy"),
        ("cheddar cheese",     "40 g",    "Dairy"),
        ("mushrooms",          "100 g",   "Produce"),
        ("capsicum",           "1/2",     "Produce"),
        ("spinach",            "handful", "Produce"),
    ],
    "salmon": [
        ("salmon fillets",     "4",       "Meat"),
        ("lemon",              "2",       "Produce"),
        ("garlic",             "2 cloves","Produce"),
        ("asparagus",          "1 bunch", "Produce"),
        ("butter",             "30 g",    "Dairy"),
        ("dill",               "1 bunch", "Produce"),
        ("olive oil",          "2 tbsp",  "Pantry"),
        ("capers",             "2 tbsp",  "Pantry"),
    ],
    "risotto": [
        ("arborio rice",       "300 g",   "Pantry"),
        ("onion",              "1",       "Produce"),
        ("garlic",             "2 cloves","Produce"),
        ("vegetable stock",    "1.2 L",   "Pantry"),
        ("white wine",         "150 ml",  "Other"),
        ("parmesan",           "80 g",    "Dairy"),
        ("butter",             "60 g",    "Dairy"),
        ("mushrooms",          "250 g",   "Produce"),
        ("olive oil",          "2 tbsp",  "Pantry"),
        ("thyme",              "3 sprigs","Produce"),
    ],
    "chilli con carne": [
        ("beef mince",         "600 g",   "Meat"),
        ("kidney beans",       "2 cans",  "Pantry"),
        ("tinned tomatoes",    "2 cans",  "Pantry"),
        ("onion",              "1 large", "Produce"),
        ("garlic",             "3 cloves","Produce"),
        ("capsicum",           "1",       "Produce"),
        ("chilli powder",      "2 tsp",   "Pantry"),
        ("cumin",              "2 tsp",   "Pantry"),
        ("smoked paprika",     "1 tsp",   "Pantry"),
        ("tomato paste",       "2 tbsp",  "Pantry"),
        ("beef stock",         "200 ml",  "Pantry"),
        ("rice",               "300 g",   "Pantry"),
        ("sour cream",         "to serve","Dairy"),
        ("cheddar cheese",     "50 g",    "Dairy"),
        ("coriander",          "1 bunch", "Produce"),
    ],
}

CATEGORIES = ["Produce", "Meat", "Dairy", "Pantry", "Other"]
MEAL_PLAN_PATH = "/home/user/Test/meal_plan.json"


def load_meal_plan() -> dict | None:
    """Load and return the meal plan JSON, or None if not found."""
    if not os.path.exists(MEAL_PLAN_PATH):
        return None
    try:
        with open(MEAL_PLAN_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error reading meal plan: {exc}", file=sys.stderr)
        return None


def normalise(meal_name: str) -> str:
    """Lowercase-strip a meal name for DB lookup."""
    return meal_name.strip().lower()


def collect_ingredients(meal_names: list[str]) -> dict[str, list[tuple[str, str]]]:
    """
    Given a list of meal names, aggregate all ingredients grouped by category.
    Returns {category: [(ingredient, quantity), ...]}
    Quantities for duplicate ingredients are concatenated with '+'.
    """
    # Use a dict to track: (category, ingredient) -> list of quantities
    seen: dict[tuple[str, str], list[str]] = defaultdict(list)

    for name in meal_names:
        key = normalise(name)
        if key in INGREDIENT_DB:
            for ingredient, quantity, category in INGREDIENT_DB[key]:
                seen[(category, ingredient.lower())].append(quantity)

    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for (category, ingredient), quantities in seen.items():
        combined_qty = " + ".join(quantities)
        grouped[category].append((ingredient, combined_qty))

    # Sort ingredients within each category
    for cat in grouped:
        grouped[cat].sort(key=lambda x: x[0])

    return grouped


def print_shopping_list(grouped: dict[str, list[tuple[str, str]]], heading: str = "Shopping List") -> None:
    """Pretty-print the shopping list with ANSI colours."""
    print()
    print(yellow_bold(f"  ══  {heading}  ══"))
    print()

    found_any = False
    for category in CATEGORIES:
        items = grouped.get(category)
        if not items:
            continue
        found_any = True
        print(yellow_bold(f"  {category}"))
        for ingredient, qty in items:
            label = f"{ingredient.title()} — {qty}"
            print(f"    {green_check(label)}")
        print()

    if not found_any:
        print("  (no ingredients found)")
        print()


def cmd_default() -> None:
    """Read the meal plan and print a grouped shopping list."""
    plan = load_meal_plan()
    if plan is None:
        print()
        print(yellow_bold("  No meal plan found."))
        print(f"  Expected file: {MEAL_PLAN_PATH}")
        print()
        print("  Run meal_planner.py first to create a meal plan, or use:")
        print("    python shopping_list.py --add \"<meal name>\"")
        print("  to manually add a meal's ingredients.")
        print()
        return

    meal_names = []
    for day_data in plan.values():
        if isinstance(day_data, dict):
            meal = day_data.get("meal", "")
        else:
            meal = str(day_data)
        if meal:
            meal_names.append(meal)

    if not meal_names:
        print("The meal plan is empty — no meals to process.")
        return

    # Warn about unknown meals
    unknown = [m for m in meal_names if normalise(m) not in INGREDIENT_DB]
    if unknown:
        print()
        print(yellow_bold("  Note: the following meals are not in the ingredient database:"))
        for m in unknown:
            print(f"    • {m}")
        print("  Run with --unknown to see only this list.")
        print()

    grouped = collect_ingredients(meal_names)
    days = list(plan.keys())
    heading = f"Shopping List ({', '.join(days)})"
    print_shopping_list(grouped, heading)


def cmd_add(meal_name: str) -> None:
    """Manually add a meal's ingredients to the printed list."""
    key = normalise(meal_name)
    if key not in INGREDIENT_DB:
        print()
        print(f"  '{meal_name}' is not in the ingredient database.")
        print()
        print("  Known meals:")
        for m in sorted(INGREDIENT_DB):
            print(f"    • {m.title()}")
        print()
        sys.exit(1)

    grouped = collect_ingredients([meal_name])
    print_shopping_list(grouped, heading=f"Ingredients for: {meal_name.title()}")


def cmd_unknown() -> None:
    """List meals in the plan that aren't in the ingredient database."""
    plan = load_meal_plan()
    if plan is None:
        print()
        print(yellow_bold("  No meal plan found."))
        print(f"  Expected file: {MEAL_PLAN_PATH}")
        print()
        return

    unknown = []
    for day, day_data in plan.items():
        if isinstance(day_data, dict):
            meal = day_data.get("meal", "")
        else:
            meal = str(day_data)
        if meal and normalise(meal) not in INGREDIENT_DB:
            unknown.append((day, meal))

    print()
    if unknown:
        print(yellow_bold("  Meals not in the ingredient database:"))
        print()
        for day, meal in unknown:
            print(f"    {green_check(f'{day}: {meal}')}")
        print()
        print("  These meals will be skipped when generating the shopping list.")
    else:
        print(yellow_bold("  All meals in the plan are recognised. No unknowns found."))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a shopping list from a family meal plan.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python shopping_list.py\n"
            "  python shopping_list.py --add \"chicken curry\"\n"
            "  python shopping_list.py --unknown\n"
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--add",
        metavar="MEAL",
        help="manually add a meal's ingredients to the shopping list",
    )
    group.add_argument(
        "--unknown",
        action="store_true",
        help="list meals in the plan that aren't in the ingredient database",
    )

    args = parser.parse_args()

    if args.add:
        cmd_add(args.add)
    elif args.unknown:
        cmd_unknown()
    else:
        cmd_default()


if __name__ == "__main__":
    main()
