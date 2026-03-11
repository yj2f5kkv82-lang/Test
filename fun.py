#!/usr/bin/env python3
"""
fun.py - ASCII art banner + existential dread, served fresh
"""

import argparse
import random
import sys

# Simple 5x3 ASCII block font (uppercase letters + space)
FONT = {
    'A': ["###", "# #", "###", "# #", "# #"],
    'B': ["## ", "# #", "## ", "# #", "## "],
    'C': ["###", "#  ", "#  ", "#  ", "###"],
    'D': ["## ", "# #", "# #", "# #", "## "],
    'E': ["###", "#  ", "## ", "#  ", "###"],
    'F': ["###", "#  ", "## ", "#  ", "#  "],
    'G': ["###", "#  ", "# #", "# #", "###"],
    'H': ["# #", "# #", "###", "# #", "# #"],
    'I': ["###", " # ", " # ", " # ", "###"],
    'J': ["  #", "  #", "  #", "# #", "###"],
    'K': ["# #", "## ", "#  ", "## ", "# #"],
    'L': ["#  ", "#  ", "#  ", "#  ", "###"],
    'M': ["# #", "###", "# #", "# #", "# #"],
    'N': ["# #", "## ", "###", " ##", "# #"],
    'O': ["###", "# #", "# #", "# #", "###"],
    'P': ["###", "# #", "###", "#  ", "#  "],
    'Q': ["###", "# #", "# #", " ##", "  #"],
    'R': ["###", "# #", "## ", "# #", "# #"],
    'S': ["###", "#  ", "###", "  #", "###"],
    'T': ["###", " # ", " # ", " # ", " # "],
    'U': ["# #", "# #", "# #", "# #", "###"],
    'V': ["# #", "# #", "# #", " # ", " # "],
    'W': ["# #", "# #", "# #", "###", "# #"],
    'X': ["# #", " # ", " # ", " # ", "# #"],
    'Y': ["# #", "# #", "###", " # ", " # "],
    'Z': ["###", "  #", " # ", "#  ", "###"],
    '0': ["###", "# #", "# #", "# #", "###"],
    '1': [" # ", "## ", " # ", " # ", "###"],
    '2': ["###", "  #", "###", "#  ", "###"],
    '3': ["###", "  #", "###", "  #", "###"],
    '4': ["# #", "# #", "###", "  #", "  #"],
    '5': ["###", "#  ", "###", "  #", "###"],
    '6': ["###", "#  ", "###", "# #", "###"],
    '7': ["###", "  #", " # ", " # ", " # "],
    '8': ["###", "# #", "###", "# #", "###"],
    '9': ["###", "# #", "###", "  #", "###"],
    ' ': ["   ", "   ", "   ", "   ", "   "],
    '!': [" # ", " # ", " # ", "   ", " # "],
    '?': ["###", "  #", " ##", "   ", " # "],
    '.': ["   ", "   ", "   ", "   ", " # "],
}

JOKES = [
    "Free will is just determinism with extra cope.",
    "Therapy taught me to set boundaries. My therapist dropped me as a client.",
    "The good news: you are the main character. The bad news: it's a Kafka novel.",
    "Meritocracy is what people who got lucky call the system that made them lucky.",
    "I asked an AI to write my life story. It said 'insufficient data for meaningful output.'",
    "Consciousness is just the universe's way of being briefly annoyed at itself.",
    "My doctor said I need to reduce stress. I said that sounds like a lot of work.",
    "They say history is written by the victors. So is the code review.",
    "The most dangerous phrase in any language: 'we've always done it this way.'",
    "Self-improvement assumes the self is worth improving.",
    "The algorithm doesn't hate you. It's just utterly, cosmically indifferent.",
    "Stoicism: the ancient philosophy of pretending not to care so you actually stop caring.",
    "Progress: we replaced feudalism with landlords and called it freedom.",
    "Every generation thinks it discovered irony.",
    "The brain is a prediction machine. Mine mostly predicts doom.",
    "Optimism is just pessimism with better PR.",
    "You are not stuck in traffic. You ARE traffic.",
    "Rationality is a post-hoc story you tell yourself about your feelings.",
    "They say knowledge is power. Turns out mostly it's just anxiety.",
    "The self is an illusion. Unfortunately, so is the relief you feel on hearing that.",
]


def ascii_banner(text: str) -> str:
    text = text.upper()
    rows = [""] * 5
    for i, char in enumerate(text):
        glyph = FONT.get(char, FONT.get('?'))
        for row_idx in range(5):
            rows[row_idx] += glyph[row_idx]
            if i < len(text) - 1:
                rows[row_idx] += " "
    return "\n".join(rows)


def random_joke() -> str:
    return random.choice(JOKES)


def main():
    parser = argparse.ArgumentParser(
        description="ASCII art + existential dread, on demand."
    )
    parser.add_argument(
        "--banner",
        metavar="TEXT",
        help="Render TEXT as ASCII art (default: FUN)",
        default=None,
    )
    parser.add_argument(
        "--joke",
        action="store_true",
        help="Print a random joke and exit",
    )
    args = parser.parse_args()

    if args.joke and args.banner is None:
        print(random_joke())
        return

    banner_text = args.banner if args.banner is not None else "FUN"
    print(ascii_banner(banner_text))
    print()
    print(random_joke())


if __name__ == "__main__":
    main()
